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

    def forget_friend(self, friend):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM friend WHERE id = %s;', friend['id'])
        self.connection.commit()
        cursor.close()
