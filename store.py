import hashlib
import os
import psycopg2 as pg
from psycopg2.extras import DictCursor


class Store():

    def __init__(self):

        db_user = os.environ.get('OPENSHIFT_POSTGRESQL_DB_USERNAME',
                                 'postgres')
        db_pass = os.environ.get('OPENSHIFT_POSTGRESQL_DB_PASSWORD')

        self.connection = pg.connect(dbname='autofriend',
                                     user=db_user,
                                     password=db_pass,
                                     cursor_factory=DictCursor)

    def get_friend(self, friend_id):

        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM friend WHERE id = %s;', (friend_id,))
        friend = cursor.fetchone()
        cursor.close()

        return friend

    def get_twitter_friend(self, twitter_id):

        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM friend WHERE twitter_id = %s;',
                       (twitter_id,))
        friend = cursor.fetchone()
        cursor.close()

        return friend

    def save_friend(self, friend):
        cursor = self.connection.cursor()
        cursor.execute(
            'INSERT INTO friend (twitter_id) VALUES (%s) RETURNING *;',
            friend)
        self.connection.commit()
        inserted = cursor.fetchone()
        cursor.close()

        return inserted

    def get_or_create_twitter_friend(self, twitter_id):

        existing = self.get_twitter_friend(twitter_id)

        if existing:
            return existing
        else:
            return self.save_friend((twitter_id,))

    def forget_friend(self, friend):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM friend WHERE id = %s;', friend['id'])
        self.connection.commit()
        cursor.close()

    def _hash_file(self, file_name):
        with open(file_name, 'rb') as f:
            hasher = hashlib.md5()
            while True:
                data = f.read(8192)
                if not data:
                    break
                hasher.update(data)
            return hasher.hexdigest()

    def remember_photo(self, photo):

        cursor = self.connection.cursor()
        cursor.execute(
            'INSERT INTO photo_seen (hash) VALUES (%s) RETURNING *;',
            (self._hash_file(photo),))

        self.connection.commit()
        result = cursor.fetchone()
        cursor.close()

        return result

    def photo_seen(self, photo):

        cursor = self.connection.cursor()
        cursor.execute(
            'SELECT * FROM photo_seen WHERE hash = %s;',
            (self._hash_file(photo),))

        seen = cursor.fetchone() is not None
        cursor.close()

        return seen
