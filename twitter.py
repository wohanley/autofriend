#!/usr/bin/env python2
# -*- coding: utf-8 -*- #

import core
import cv2
import FaceRecognizer
from functools import partial
import requests
from twitterbot import TwitterBot


def get_photos_from_tweet(tweet):
    return [requests.get(m["media_url"])
            for m in tweet.entities.get("media", [])
            if m.get("type", None) == "photo"]


class Autofriend(TwitterBot):

    def bot_init(self):

        ############################
        # REQUIRED: LOGIN DETAILS! #
        ############################
        self.config['api_key'] = ''
        self.config['api_secret'] = ''
        self.config['access_key'] = ''
        self.config['access_secret'] = ''

        ######################################
        # SEMI-OPTIONAL: OTHER CONFIG STUFF! #
        ######################################

        # how often to tweet, in seconds
        self.config['tweet_interval'] = 30 * 60     # default: 30 minutes

        # only include bot followers (and original tweeter) in @-replies
        self.config['reply_followers_only'] = True

        # fav any tweets that mention this bot?
        self.config['autofav_mentions'] = True

        # fav any tweets containing these keywords?
        self.config['autofav_keywords'] = ["selfie"]

        # follow back all followers?
        self.config['autofollow'] = True

        ###########################################
        # CUSTOM: your bot's own state variables! #
        ###########################################

        self.face_regions = partial(
            core.face_regions,
            core.load_face_detector())

        self.face_recognizer = FaceRecognizer()

        # If you'd like to save variables with the bot's state, use the
        # self.state dictionary. These will only be initialized if the bot is
        # not loading a previous saved state.

        # self.state['butt_counter'] = 0

        # You can also add custom functions that run at regular intervals
        # using self.register_custom_handler(function, interval).
        #
        # For instance, if your normal timeline tweet interval is every 30
        # minutes, but you'd also like to post something different every 24
        # hours, you would implement self.my_function and add the following
        # line here:
        
        # self.register_custom_handler(self.my_function, 60 * 60 * 24)

    def on_scheduled_tweet(self):
        pass

    def on_mention(self, tweet, prefix):

        photos = get_photos_from_tweet(tweet)

        prepared_images = [cv2.imdecode(photo, cv2.CV_LOAD_IMAGE_GRAYSCALE)
                           for photo in photos]

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
        # text = function_that_returns_a_string_goes_here()
        # prefixed_text = prefix + ' ' + text
        # self.post_tweet(prefix + ' ' + text, reply_to=tweet)

        # call this to fav the tweet!
        # if something:
        #     self.favorite_tweet(tweet)

        photos = get_photos_from_tweet(tweet)

        face_regions = core.flatten(
            [self.face_regions(photo) for photo in photos])

        recognitions = [self.recognizer.recognize_face(region)
                        for region in face_regions]

        likely_recognitions = filter(
            lambda (_, probability): probability > 75,
            recognitions)

        recognized_labels = set([label for (label, _) in likely_recognitions])


if __name__ == '__main__':
    Autofriend().run()
