# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import os
import sys

py3 = sys.version_info >= (3,)


USER_KEY = os.environ.get('LR_USER_KEY')
SERVICE_URL = os.environ.get('LR_SERVICE_URL')
TEST_NIP_SP = os.environ.get('LR_TEST_NIP_SP')
TEST_REGON_SP = int(os.environ.get('LR_TEST_REGON_SP'))
TEST_NAME_SP = os.environ.get('LR_TEST_NAME_SP')
TEST_NIP_CP = os.environ.get('LR_TEST_NIP_CP')
TEST_REGON_CP = int(os.environ.get('LR_TEST_REGON_CP'))
TEST_NAME_CP = os.environ.get('LR_TEST_NAME_CP')

if not py3:
    TEST_NAME_CP = unicode(TEST_NAME_CP, 'UTF-8')
