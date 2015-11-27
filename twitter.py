#!/usr/bin/env python2
# -*- coding: utf-8 -*- #

import compliments
import core
import cv2
from facerec import FaceRecognizer
from functools import partial
import logging
import os
import psycopg2 as pg
import requests
from store import Store
from twitterbot import TwitterBot
import uuid


def get_photos(tweet):

    if hasattr(tweet, 'extended_entities'):
        entities = tweet.extended_entities
    else:
        entities = tweet.entities

    return filter(
        lambda media: media.get('type', None) == 'photo',
        entities.get('media', []))


def get_photo_url(media_item):
    return media_item['media_url'] + ':large'


def download_file(url):
    fileName = 'temp-' + str(uuid.uuid4())
    with open(fileName, 'wb') as f:
        for chunk in requests.get(url).iter_content():
            f.write(chunk)
    return fileName


class DownloadedFile():

    def __init__(self, url):
        self.url = url

    def __enter__(self):
        self._fileName = download_file(self.url)
        return self._fileName

    def __exit__(self, exc_type, exc_value, traceback):
        os.remove(self._fileName)


def get_photos_from_tweet(tweet):

    photos = []

    for url in [get_photo_url(photo) for photo in get_photos(tweet)]:
        with DownloadedFile(url) as downloaded:
            photos.append(cv2.imread(downloaded, cv2.CV_LOAD_IMAGE_GRAYSCALE))

    return photos


class Autofriend(TwitterBot):

    def bot_init(self):

        ############################
        # REQUIRED: LOGIN DETAILS! #
        ############################

        self.config['api_key'] = os.environ['TWITTER_API_KEY']
        self.config['api_secret'] = os.environ['TWITTER_API_SECRET']
        self.config['access_key'] = os.environ['TWITTER_ACCESS_KEY']
        self.config['access_secret'] = os.environ['TWITTER_ACCESS_SECRET']

        ######################################
        # SEMI-OPTIONAL: OTHER CONFIG STUFF! #
        ######################################

        # how often to tweet, in seconds
        self.config['tweet_interval'] = 30 * 60     # default: 30 minutes

        # only include bot followers (and original tweeter) in @-replies
        self.config['reply_followers_only'] = True

        # fav any tweets that mention this bot?
        self.config['autofav_mentions'] = False

        # fav any tweets containing these keywords?
        self.config['autofav_keywords'] = []

        # follow back all followers?
        self.config['autofollow'] = True

        ###########################################
        # CUSTOM: your bot's own state variables! #
        ###########################################

        self.face_regions = partial(
            core.face_regions,
            core.load_face_detector())

        self.face_recognizer = FaceRecognizer()

        self.store = Store()

    def get_confidence(self):
        return float(os.environ.get('AUTOFRIEND_CONFIDENCE') or 50)

    def on_scheduled_tweet(self):
        pass

    def on_follow(self, follower_id):

        TwitterBot.on_follow(self, follower_id)

        try:
            self.store.save_friend((follower_id,))
        except pg.IntegrityError:
            # aborting is harmless, most likely an unfollow/refollow
            self.log("tried to add duplicate twitter friend %s" % follower_id)

    def _process_photo(self, friend_id, url):
        with DownloadedFile(url) as downloaded:
            if not self.store.photo_seen(downloaded):
                face_regions = self.face_regions(
                    core.prepare_image(downloaded))
                self.face_recognizer.update(
                    [(face_region, friend_id)
                     for face_region in face_regions])
                self.store.remember_photo(downloaded)

    def on_direct_message(self, dm):

        media = dm.entities.get('media', [])
        photo = media[0] if len(media) > 0 else None

        if photo:
            self._process_photo(dm.sender_id, get_photo_url(photo))

        self.send_direct_message(dm.sender, compliments.get_compliment())

    def on_mention(self, tweet, prefix):

        if 'PLEASE FORGET ME' in tweet.text.upper():
            self.store.forget_friend(
                self.store.get_twitter_friend(tweet.author.id))
            self.api.destroy_friendship(tweet.author.id)
        else:

            friend_id = self.store.get_or_create_twitter_friend(
                tweet.author.id)['id']

            photo_urls = [get_photo_url(photo) for photo in get_photos(tweet)]

            for url in photo_urls:
                self._process_photo(friend_id, url)

        self.favorite_tweet(tweet)

    def on_timeline(self, tweet, prefix):
        """
        Defines actions to take on a timeline tweet.

        tweet - a tweepy.Status object. You can access the text with
        tweet.text

        prefix - the @-mentions for this reply. No need to include this in the
        reply string; it's provided so you can use it to make sure the value
        you return is within the 140 character limit with this.

        It's up to you to ensure that the prefix and tweet are less than 140
        characters.

        When calling post_tweet, you MUST include reply_to=tweet, or
        Twitter won't count it as a reply.
        """

        photos = get_photos_from_tweet(tweet)

        face_regions = core.flatten(
            [self.face_regions(photo) for photo in photos])

        recognitions = []
        for region in face_regions:
            try:
                recognitions.append(
                    self.face_recognizer.recognize_face(region))
            except cv2.error as e:
                logging.error("Error recognizing face region: " + e.message)

        likely_recognitions = filter(
            lambda (_, margin): margin < self.get_confidence(),
            recognitions)

        recognized_labels = set([label for (label, _) in likely_recognitions])

        for label in recognized_labels:
            recognized = self.store.get_friend(label)
            # it's possible someone is in the model but not in the database,
            # e.g. people that asked to be forgotten
            if recognized and recognized.get('twitter_id', None):
                twitter_friend = self.api.get_user(recognized['twitter_id'])
                self.favorite_tweet(tweet)
                self.post_tweet(
                    prefix +
                    ' ' + compliments.get_compliment() + ' ' +
                    '@' + twitter_friend.screen_name,
                    reply_to=tweet)


if __name__ == '__main__':
    Autofriend().run()
