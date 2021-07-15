# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import UserPassesTestMixin


class OnlyAdminsMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff
