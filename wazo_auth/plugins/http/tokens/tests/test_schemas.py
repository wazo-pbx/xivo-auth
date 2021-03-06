# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest import TestCase

from marshmallow.exceptions import ValidationError

from hamcrest import assert_that, calling, has_properties, has_item, not_
from xivo_test_helpers.hamcrest.raises import raises

from ..schemas import TokenRequestSchema


class TestTokenRequestSchema(TestCase):
    def setUp(self):
        self.schema = TokenRequestSchema()

    def test_invalid_expiration(self):
        invalid_values = [None, True, False, 'foobar', 0]

        for value in invalid_values:
            body = {'expiration': value}
            assert_that(
                calling(self.schema.load).with_args(body),
                raises(ValidationError).matching(
                    has_properties(field_names=has_item('expiration'))
                ),
            )

    def test_minimal_body(self):
        body = {}
        assert_that(calling(self.schema.load).with_args(body), not_(raises(Exception)))

    def test_that_acces_type_offline_requires_a_client_id(self):
        body = {'access_type': 'offline'}

        assert_that(
            calling(self.schema.load).with_args(body),
            raises(ValidationError).matching(
                has_properties(field_names=has_item('_schema'))
            ),
        )

    def test_that_the_access_type_is_online_when_using_a_refresh_token(self):
        body = {'refresh_token': 'foobar', 'client_id': 'x'}

        assert_that(calling(self.schema.load).with_args(body), not_(raises(Exception)))

        assert_that(
            calling(self.schema.load).with_args(dict(access_type='online', **body)),
            not_(raises(Exception)),
        )

        assert_that(
            calling(self.schema.load).with_args(dict(access_type='offline', **body)),
            raises(ValidationError).matching(
                has_properties(field_names=has_item('_schema'))
            ),
        )

    def test_that_a_refresh_token_requires_a_client_id(self):
        body = {'refresh_token': 'the-token'}

        assert_that(
            calling(self.schema.load).with_args(dict(client_id='x', **body)),
            not_(raises(Exception)),
        )

        assert_that(
            calling(self.schema.load).with_args(body),
            raises(ValidationError).matching(
                has_properties(field_names=has_item('_schema'))
            ),
        )
