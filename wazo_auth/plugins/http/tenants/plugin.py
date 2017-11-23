# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from . import http


class Plugin(object):

    def load(self, dependencies):
        api = dependencies['api']
        args = (dependencies['tenant_service'],)

        api.add_resource(http.Tenants, '/tenants', resource_class_args=args)
        api.add_resource(http.Tenant, '/tenants/<string:tenant_uuid>', resource_class_args=args)