# -*- coding: utf-8 -*-
#
# Copyright 2015-2017 The Wazo Authors  (see the AUTHORS file)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>


from xivo_dao import admin_dao
from xivo_dao.helpers.exception import NotFoundError
from xivo_dao.helpers.db_utils import session_scope

from wazo_auth import BaseAuthenticationBackend, ACLRenderingBackend
from wazo_auth.exceptions import AuthenticationFailedException


class XiVOAdmin(BaseAuthenticationBackend, ACLRenderingBackend):

    def get_acls(self, login, args):
        acl_templates = args.get('acl_templates', [])
        return self.render_acl(acl_templates, self.get_admin_data, username=login)

    def get_admin_data(self, username):
        with session_scope():
            entity = admin_dao.get_admin_entity(username)

        return {'entity': entity}

    def get_ids(self, username, args):
        with session_scope():
            try:
                auth_id = admin_dao.get_admin_uuid(username)
            except NotFoundError:
                raise AuthenticationFailedException()

        user_uuid = None
        return auth_id, user_uuid

    def verify_password(self, login, password, args):
        with session_scope():
            return admin_dao.check_username_password(login, password)