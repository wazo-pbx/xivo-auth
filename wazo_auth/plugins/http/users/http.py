# -*- coding: utf-8 -*-
# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask import request
from wazo_auth import exceptions, http, schemas
from wazo_auth.flask_helpers import Tenant

from .schemas import ChangePasswordSchema, UserPostSchema, UserPutSchema


class BaseUserService(http.AuthResource):

    def __init__(self, user_service):
        self.user_service = user_service


class User(BaseUserService):

    @http.required_acl('auth.users.{user_uuid}.read')
    def get(self, user_uuid):
        return self.user_service.get_user(user_uuid)

    @http.required_acl('auth.users.{user_uuid}.delete')
    def delete(self, user_uuid):
        self.user_service.delete_user(user_uuid)
        return '', 204

    @http.required_acl('auth.users.{user_uuid}.edit')
    def put(self, user_uuid):
        args, errors = UserPutSchema().load(request.get_json())
        if errors:
            raise exceptions.UserParamException.from_errors(errors)

        result = self.user_service.update(user_uuid, **args)
        return result, 200


class UserPassword(BaseUserService):

    @http.required_acl('auth.users.{user_uuid}.password.edit')
    def put(self, user_uuid):
        args, errors = ChangePasswordSchema().load(request.get_json())
        if errors:
            raise exceptions.PasswordChangeException.from_errors(errors)
        self.user_service.change_password(user_uuid, **args)
        return '', 204


class Users(BaseUserService):

    # TODO: remove tokens and users
    def __init__(self, user_service, tokens, users):
        self.user_service = user_service
        self.tokens = tokens
        self.users = users

    @http.required_acl('auth.users.read')
    def get(self):
        tenants = Tenant.autodetect(many=True)
        ListSchema = schemas.new_list_schema('username')
        list_params, errors = ListSchema().load(request.args)
        if errors:
            raise exceptions.InvalidListParamException(errors)

        tenant_uuids = [tenant.uuid for tenant in tenants]
        users = self.user_service.list_users(tenant_uuids=tenant_uuids, **list_params)
        total = self.user_service.count_users(filtered=False, tenant_uuids=tenant_uuids, **list_params)
        filtered = self.user_service.count_users(filtered=True, tenant_uuids=tenant_uuids, **list_params)

        response = {
            'filtered': filtered,
            'total': total,
            'items': users,
        }

        return response, 200

    @http.required_acl('auth.users.create')
    def post(self):
        args, errors = UserPostSchema().load(request.get_json())
        tenant = Tenant.autodetect()
        if errors:
            raise exceptions.UserParamException.from_errors(errors)
        result = self.user_service.new_user(email_confirmed=True, tenant_uuid=tenant.uuid, **args)
        return result, 200
