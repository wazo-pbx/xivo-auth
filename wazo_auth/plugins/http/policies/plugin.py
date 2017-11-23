# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from . import http


class Plugin(object):

    def load(self, dependencies):
        api = dependencies['api']
        args = (dependencies['policy_service'],)

        api.add_resource(http.Policies, '/policies', resource_class_args=args)
        api.add_resource(http.Policy, '/policies/<string:policy_uuid>', resource_class_args=args)
        api.add_resource(http.PolicyTemplate, '/policies/<string:policy_uuid>/acl_templates/<template>',
                         resource_class_args=args)