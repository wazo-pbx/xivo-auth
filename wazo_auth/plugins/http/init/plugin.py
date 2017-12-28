# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from . import http


class Plugin(object):

    def load(self, dependencies):
        api = dependencies['api']
        config = dependencies['config']
        args = (
            dependencies['policy_service'],
            dependencies['user_service'],
            config,
        )

        api.add_resource(http.Init, '/init', resource_class_args=args)