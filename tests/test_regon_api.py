# -*- coding: UTF-8 -*-
'''
Basic tests of REGON API

Created on 17 lip 2015

@author: Michał Wegrzynek <mwegrzynek@litex.pl>
'''
from __future__ import unicode_literals
import datetime
import os
import sys


import pytest
from lxml import etree


from litex.regon import REGONAPIError, REGONAPI


py3 = sys.version_info >= (3,)


USER_KEY = os.environ.get('LR_USER_KEY')
SERVICE_URL = os.environ.get('LR_SERVICE_URL')
TEST_NIP_SP = os.environ.get('LR_TEST_NIP_SP')
TEST_REGON_SP = int(os.environ.get('LR_TEST_REGON_SP'))
TEST_NAME_SP = os.environ.get('LR_TEST_NAME_SP')
TEST_PKD_SP = os.environ.get('LR_TEST_PKD_SP')
TEST_NIP_CP = os.environ.get('LR_TEST_NIP_CP')
TEST_REGON_CP = int(os.environ.get('LR_TEST_REGON_CP'))
TEST_NAME_CP = os.environ.get('LR_TEST_NAME_CP')
TEST_PKD_CP = os.environ.get('LR_TEST_PKD_CP')
if not py3:
    TEST_NAME_SP = unicode(TEST_NAME_SP, 'UTF-8')
    TEST_NAME_CP = unicode(TEST_NAME_CP, 'UTF-8')


@pytest.fixture
def api():
    return REGONAPI(SERVICE_URL)


@pytest.fixture
def li_api(api):
    '''Logged in API'''
    api.login(USER_KEY)
    return api


def test_login_correct_user_key(api):
    sid = api.login(USER_KEY)
    assert len(sid) == 20


def test_login_incorrect_user_key(api):
    with pytest.raises(REGONAPIError):
        api.login('dummykey')


def test_logout(api):
    api.login(USER_KEY)
    api.logout()


def test_search_no_params(li_api):
    with pytest.raises(REGONAPIError):
        li_api.search()


def test_search_sole_proprietorship(li_api):
    result = li_api.search(nip=TEST_NIP_SP)
    assert result[0].Regon == TEST_REGON_SP
    assert result[0].Nazwa == TEST_NAME_SP
    li_api.logout()


def test_search_sole_proprietorship_detailed(li_api):
    result = li_api.search(nip=TEST_NIP_SP, detailed=True)[0]
    assert result[0].Regon == TEST_REGON_SP
    assert str(result[0].detailed.fiz_nip) == TEST_NIP_SP
    assert getattr(
        result.detailed,
        'fiz_adSiedzNumerNieruchomosci'
    ) is not None
    li_api.logout()


def test_search_corporation(li_api):
    result = li_api.search(nip=TEST_NIP_CP)
    assert result[0].Regon == TEST_REGON_CP
    assert result[0].Nazwa == TEST_NAME_CP
    li_api.logout()


def test_search_corporation_detailed(li_api):
    result = li_api.search(nip=TEST_NIP_CP, detailed=True)[0]
    assert result.Regon == TEST_REGON_CP
    assert getattr(
        result.detailed,
        'praw_adSiedzNumerNieruchomosci'
    ) is not None
    li_api.logout()


def test_search_multiple_nips(li_api):
    result = li_api.search(nips=[TEST_NIP_CP, TEST_NIP_SP])
    assert len(result) >= 2
    assert result[0].Regon == TEST_REGON_CP
    assert result[1].Regon == TEST_REGON_SP
    li_api.logout()


def test_issue_3_charities(li_api):
    result = li_api.search(
        regons=[
            '01210292600037',
            '01210292600051',
            '01210292600076'
        ],
        detailed=True
    )

    assert len(result) == 3

    for res in result:
        assert res.detailed.lokpraw_regon14 == res.Regon

    li_api.logout()


def test_get_value(li_api):
    assert li_api.get_value('KomunikatKod') == '0'

    try:
        li_api.search(nip='wrong_nip')
    except REGONAPIError:
        pass

    assert li_api.get_value('KomunikatKod') == '4'


def test_no_session_exception_message(api):    
    with pytest.raises(REGONAPIError) as e_info:
        api.search(nip=TEST_NIP_SP)

    assert e_info.value.message == 'No response received. Are you logged in?'


def test_entity_not_found_exception_message(li_api):    
    with pytest.raises(REGONAPIError) as e_info:
        res = li_api.search(nips=['7964627448', '1184627375'])

    assert e_info.value.message == 'No data found for the specified search criteria.'
    assert e_info.value.code == 4
    li_api.logout()


def test_summary_report(li_api):
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    
    date = yesterday.strftime('%Y-%m-%d')
    
    summary_rep_name = 'BIR11NowePodmiotyPrawneOrazDzialalnosciOsFizycznych'
    report = li_api.summary_report(date, summary_rep_name)
    
    assert report[0].tag == 'dane'

    li_api.logout()


def test_full_report_error_handling(li_api):
    with pytest.raises(REGONAPIError) as excinfo:
        li_api.full_report('wrong_regon', 'PublDaneRaportPrawna')

    assert excinfo.value.code == 4

    li_api.logout()

def test_full_report_sole_proprietorship_pkd(li_api):
    report_name = 'BIR11OsFizycznaPkd'
    result = li_api.full_report(TEST_REGON_SP, report_name)

    assert result is not None
    assert hasattr(result[0], 'fiz_pkd_Kod')
    assert hasattr(result[0], 'fiz_pkd_Nazwa')

    main_pkd = next(filter(lambda x: getattr(x, 'fiz_pkd_Przewazajace', 0) == 1, result), None)
    assert main_pkd is not None, 'No PKD record with fiz_pkd_Przewazajace = 1 found'

    pkd_code = getattr(main_pkd, 'fiz_pkd_Kod', None)
    assert pkd_code is not None, 'Missing fiz_pkd_Kod for main PKD entry'

    assert pkd_code == TEST_PKD_SP, 'Main PKD code does not match expected value'

    li_api.logout()

def test_full_report_corporation_pkd(li_api):
    report_name = 'BIR11OsPrawnaPkd'
    result = li_api.full_report(TEST_REGON_CP, report_name)

    assert result is not None
    assert hasattr(result[0], 'praw_pkdKod')
    assert hasattr(result[0], 'praw_pkdNazwa')

    main_pkd = next(filter(lambda x: getattr(x, 'praw_pkdPrzewazajace', 0) == 1, result), None)
    assert main_pkd is not None, 'No PKD record with praw_pkdPrzewazajace = 1 found'

    pkd_code = getattr(main_pkd, 'praw_pkdKod', None)
    assert pkd_code is not None, 'Missing praw_pkdKod for main PKD entry'

    assert pkd_code == TEST_PKD_CP, 'Main PKD code does not match expected value'

    li_api.logout()
