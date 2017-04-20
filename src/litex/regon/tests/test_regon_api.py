# -*- coding: UTF-8 -*-
'''
Basic tests of REGON API

Created on 17 lip 2015

@author: Michał Wegrzynek <mwegrzynek@litex.pl>
'''
from nose.tools import eq_, ok_, raises


from . import (
    USER_KEY,
    SERVICE_URL,
    TEST_NIP_SP,
    TEST_REGON_SP,
    TEST_NAME_SP,
    TEST_NIP_CP,
    TEST_REGON_CP,
    TEST_NAME_CP
)
from .. import REGONAPIError, REGONAPI


def test_login_correct_user_key():
    api = REGONAPI(SERVICE_URL)
    sid = api.login(USER_KEY)

    eq_(len(sid), 20)


@raises(REGONAPIError)
def test_login_incorrect_user_key():
    api = REGONAPI(SERVICE_URL)
    api.login('dummykey')


@raises(REGONAPIError)
def test_logout_without_login():
    api = REGONAPI(SERVICE_URL)
    api.logout()


def test_logout():
    api = REGONAPI(SERVICE_URL)
    api.login(USER_KEY)
    api.logout()


@raises(REGONAPIError)
def test_search_no_params():
    api = REGONAPI(SERVICE_URL)
    api.search()


def test_search_sole_proprietorship():
    api = REGONAPI(SERVICE_URL)
    api.login(USER_KEY)
    result = api.search(nip=TEST_NIP_SP)
    eq_(str(result[0].Regon), TEST_REGON_SP)
    eq_(str(result[0].Nazwa), TEST_NAME_SP)
    api.logout()


def test_search_sole_proprietorship_detailed():
    api = REGONAPI(SERVICE_URL)
    api.login(USER_KEY)
    result = api.search(nip=TEST_NIP_SP, detailed=True)[0]
    eq_(str(result[0].Regon), TEST_REGON_SP)
    eq_(str(result[0].detailed.fiz_nip), TEST_NIP_SP)
    ok_(getattr(result.detailed, 'fiz_adSiedzNumerNieruchomosci') is not None)
    api.logout()


def test_search_corporation():
    api = REGONAPI(SERVICE_URL)
    api.login(USER_KEY)
    result = api.search(nip=TEST_NIP_CP)
    eq_(str(result[0].Regon), TEST_REGON_CP)
    eq_(str(result[0].Nazwa), TEST_NAME_CP)
    api.logout()


def test_search_corporation_detailed():
    api = REGONAPI(SERVICE_URL)
    api.login(USER_KEY)
    result = api.search(nip=TEST_NIP_CP, detailed=True)[0]
    eq_(str(result.Regon), TEST_REGON_CP)
    ok_(getattr(result.detailed, 'praw_adSiedzNumerNieruchomosci') is not None)
    api.logout()


def test_search_multiple_nips():
    api = REGONAPI(SERVICE_URL)
    api.login(USER_KEY)
    result = api.search(nips=[TEST_NIP_CP, TEST_NIP_SP])
    assert len(result) >= 2
    eq_(str(result[-1].Regon), TEST_REGON_CP)
    eq_(str(result[0].Regon), TEST_REGON_SP)
    api.logout()
