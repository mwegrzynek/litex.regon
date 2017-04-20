# -*- coding: UTF-8 -*-
'''
Simple modułe for fetching data from Polish REGON database.
As all Python SOAP libraries I know have problem accessing this service,
I reimplemented querying with plain requests.

Created on 17 lip 2015

@author: Michał Węgrzynek
'''
from __future__ import unicode_literals
import logging
import email


import requests
from lxml import etree, objectify


from .envelopes import (
    LOGIN_ENVELOPE,
    LOGOUT_ENVELOPE,
    SEARCH_ENVELOPE,
    FULL_REPORT_ENVELOPE,
    GET_CAPTCHA_ENVELOPE,
    CHECK_CAPTCHA_ENVELOPE
)


log = logging.getLogger(__name__)


namespaces = {
    'bir': 'http://CIS/BIR/PUBL/2014/07',
    'pb': 'http://CIS/BIR/2014/07'
}


detailed_report_names_map = {
    '6': 'PublDaneRaportPrawna',
    '1': 'PublDaneRaportDzialalnoscFizycznejCeidg',
    '2': 'PublDaneRaportDzialalnoscFizycznejRolnicza',
    '3': 'PublDaneRaportDzialalnoscFizycznejPozostala',
    '4': 'PublDaneRaportDzialalnoscFizycznejWKrupgn'
}


def get_message_element(message, payload_num, path):
    resp = message.get_payload(payload_num).get_payload()
    return etree.fromstring(resp).xpath(path, namespaces=namespaces)


class REGONAPIError(RuntimeError):
    pass


class REGONAPI(object):

    def __init__(self, service_url):
        self.service_url = service_url
        self.sid = None

    def call(self, envelope, **args):
        '''
        Calls an API's method (descibed by the envelope)
        '''
        data = envelope.format(api=self, **args)
        log.debug('Data to be posted: %s', data)
        res = requests.post(
            self.service_url,
            stream=True,
            data=data,
            headers={
                'Content-Type': 'application/soap+xml; charset=utf-8',
                'sid': self.sid if self.sid else None
            }
        )
        mimemsg = '\r\n'.join(
            '{0}: {1}'.format(key, val) for key, val in res.headers.items()
        )
        mimemsg += '\r\n' + res.text

        mesg = email.message_from_string(mimemsg)
        assert mesg.is_multipart, 'Response is not multipart.'

        return mesg

    def login(self, user_key):
        '''
        Logs in to the REGON API Service
        (uses API key provided by the REGON administrators)
        '''
        mesg = self.call(LOGIN_ENVELOPE, user_key=user_key)

        result = get_message_element(mesg, 0, '//bir:ZalogujResult/text()')
        if not result:
            self.sid = None
            raise REGONAPIError('Login failed.')

        self.sid = result[0]

        return self.sid

    def logout(self):
        '''
        Ends API session
        '''
        if not self.sid:
            raise REGONAPIError('Not logged in.')

        mesg = self.call(LOGOUT_ENVELOPE)
        result = get_message_element(mesg, 0, '//bir:WylogujResult/text()')

        if not result or result[0] != 'true':
            raise REGONAPIError('Logout failed.')

        return True

    def get_captcha(self):
        '''
        Gets CAPTCHA for human verification;
        Returns decoded image data or false, if showing CAPTCHA is not needed
        '''
        mesg = self.call(GET_CAPTCHA_ENVELOPE)
        result = get_message_element(
            mesg,
            0,
            '//pb:PobierzCaptchaResult/text()'
        )
        if not result:
            raise REGONAPIError('Getting CAPTCHA failed.')

        resp = result[0]
        return resp if resp else False

    def check_captcha(self, captcha):
        '''
        Sends the human recognized CAPTCHA string for verification
        '''
        mesg = self.call(CHECK_CAPTCHA_ENVELOPE, captcha=captcha)
        result = get_message_element(
            mesg,
            0,
            '//pb:SprawdzCaptchaResult/text()'
        )
        if not result:
            raise REGONAPIError('Checking CAPTCHA failed.')

        resp = result[0]
        return resp == 'true'

    def search(
        self,
        nip=None,
        regon=None,
        krs=None,
        nips=None,
        regons=None,
        krss=None,
        detailed=False
    ):
        if not (regon or nip or krs or regons or nips or krss):
            raise REGONAPIError(
                'You have to pass at least one of: '
                'nip(s), regon(s) or krs(s) parameters.'
            )

        param = ''
        if nip:
            param += '<dat:Nip>{0}</dat:Nip>'.format(nip)

        if regon:
            param += '<dat:Regon>{0}</dat:Regon>'.format(regon)

        if krs:
            param += '<dat:Krs>{0}</dat:Krs>'.format(krs)

        if nips:
            nip_str = ''.join(nips)
            assert len(nip_str) % 10 == 0, \
                'All NIPs should be 10 character strings.'

            param += '<dat:Nipy>{0}</dat:Nipy>'.format(nip_str)

        if krss:
            krs_str = ''.join(krss)
            assert len(krs_str) % 10 == 0, \
                'All KRSs should be 10 character strings.'
            param += '<dat:Krsy>{0}</dat:Krsy>'.format(krs_str)

        if regons:
            regons_str = ''.join(regons)
            rl = len(regons_str)

            if rl % 9 == 0:
                param += '<dat:Regony9zn>{0}</dat:Regony9zn>'.format(
                    regons_str
                )
            elif rl % 14 == 0:
                param += '<dat:Regony14zn>{0}</dat:Regony14zn>'.format(
                    regons_str
                )
            else:
                raise AssertionError(
                    'All REGONs should be either 9 or 14 character strings.'
                )

        mesg = self.call(SEARCH_ENVELOPE, param=param)
        result = get_message_element(mesg, 0, '//bir:DaneSzukajResult/text()')
        if not result:
            raise REGONAPIError('Search failed.')

        search_results = list(objectify.fromstring(result[0]).dane)

        if not detailed:
            return search_results
        else:
            detailed_data = []
            for rs in search_results:

                # Sometimes the leading zeros get lost
                correct_regon = '{0:014}'.format(int(rs.Regon)) \
                    if len(str(rs.Regon)) not in (9, 14) else rs.Regon

                correct_report_name = detailed_report_names_map.get(
                    str(rs.SilosID)
                )
                rs.detailed = self.full_report(
                    correct_regon,
                    correct_report_name
                )

                if rs.Typ == 'F':
                    # Data from sole proprietorhsips has to be extended
                    # by an additional report
                    sp_data = self.full_report(
                        correct_regon,
                        'PublDaneRaportFizycznaOsoba'
                    )
                    rs.detailed.extend(sp_data.getchildren())

                detailed_data.append(rs)

            return detailed_data

    def full_report(self, regon, report_name):
        mesg = self.call(
            FULL_REPORT_ENVELOPE,
            regon=regon,
            report_name=report_name
        )
        result = objectify.fromstring(
            get_message_element(
                mesg,
                0,
                '//bir:DanePobierzPelnyRaportResult/text()'
            )[0]
        )

        if not len(result):
            raise REGONAPIError('Getting full report failed.')

        return result[0].dane
