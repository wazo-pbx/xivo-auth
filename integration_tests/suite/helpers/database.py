# Copyright 2018-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import sqlalchemy as sa

logger = logging.getLogger(__name__)


class Database:
    @classmethod
    def build(cls, user, password, host, port, db):
        uri = f"postgresql://{user}:{password}@{host}:{port}"
        return cls(uri, db)

    def __init__(self, uri, db):
        self.uri = uri
        self.db = db
        self._engine = self.create_engine()

    def is_up(self):
        try:
            self.connect()
            return True
        except Exception as e:
            logger.debug('Database is down: %s', e)
            return False

    def create_engine(self, db=None, isolate=False):
        db = db or self.db
        uri = "{}/{}".format(self.uri, db)
        if isolate:
            return sa.create_engine(uri, isolation_level='AUTOCOMMIT')
        return sa.create_engine(uri)

    def connect(self, db=None):
        return self._engine.connect()

    def recreate(self):
        engine = self.create_engine("postgres", isolate=True)
        connection = engine.connect()
        connection.execute(
            """
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{db}'
            AND pid <> pg_backend_pid()
            """.format(
                db=self.db
            )
        )
        connection.execute("DROP DATABASE IF EXISTS {db}".format(db=self.db))
        connection.execute(
            "CREATE DATABASE {db} TEMPLATE {template}".format(
                db=self.db, template=self.TEMPLATE
            )
        )
        connection.close()
