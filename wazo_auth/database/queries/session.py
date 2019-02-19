# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from sqlalchemy import text, and_

from .base import BaseDAO, PaginatorMixin
from ..models import (
    Session,
    Token,
)


class SessionDAO(PaginatorMixin, BaseDAO):

    column_map = {'mobile': Session.mobile}

    def list_(self, tenant_uuids=None, **kwargs):
        filter_ = text('true')
        if tenant_uuids is not None:
            if not tenant_uuids:
                return []

            filter_ = Session.tenant_uuid.in_(tenant_uuids)

        with self.new_session() as s:
            query = s.query(Session, Token).join(Token).filter(filter_)
            query = self._paginator.update_query(query, **kwargs)

            return [{
                'uuid': result.Session.uuid,
                'mobile': result.Session.mobile,
                'tenant_uuid': result.Session.tenant_uuid,
                'user_uuid': result.Token.auth_id,
            } for result in query.all()]

    def count(self, tenant_uuids=None, **kwargs):
        filter_ = text('true')

        if tenant_uuids is not None:
            if not tenant_uuids:
                return 0
            filter_ = and_(filter_, Session.tenant_uuid.in_(tenant_uuids))

        with self.new_session() as s:
            return s.query(Session).join(Token).filter(filter_).count()