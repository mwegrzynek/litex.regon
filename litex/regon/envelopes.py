# -*- coding: UTF-8 -*-
'''
SOAP Envelopes for REGON API
Created on 17 lip 2015

@author: Michał Węgrzynek
'''

LOGIN_ENVELOPE = '''\
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:ns="http://CIS/BIR/PUBL/2014/07">
<soap:Header xmlns:wsa="http://www.w3.org/2005/08/addressing">
<wsa:To>{api.service_url}</wsa:To>
<wsa:Action>http://CIS/BIR/PUBL/2014/07/IUslugaBIRzewnPubl/Zaloguj</wsa:Action>
</soap:Header>
   <soap:Body>
      <ns:Zaloguj>
         <ns:pKluczUzytkownika>{user_key}</ns:pKluczUzytkownika>
      </ns:Zaloguj>
   </soap:Body>
</soap:Envelope>
'''

LOGOUT_ENVELOPE = '''\
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:ns="http://CIS/BIR/PUBL/2014/07">
<soap:Header xmlns:wsa="http://www.w3.org/2005/08/addressing">
<wsa:To>{api.service_url}</wsa:To>
<wsa:Action>http://CIS/BIR/PUBL/2014/07/IUslugaBIRzewnPubl/Wyloguj</wsa:Action>
</soap:Header>
   <soap:Body>
      <ns:Wyloguj>
         <ns:pIdentyfikatorSesji>{api.sid}</ns:pIdentyfikatorSesji>
      </ns:Wyloguj>
   </soap:Body>
</soap:Envelope>
'''

GET_CAPTCHA_ENVELOPE = '''\
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:ns="http://CIS/BIR/2014/07">
<soap:Header xmlns:wsa="http://www.w3.org/2005/08/addressing">
<wsa:To>{api.service_url}</wsa:To>
<wsa:Action>http://CIS/BIR/2014/07/IUslugaBIR/PobierzCaptcha</wsa:Action>
</soap:Header>
   <soap:Body>
      <ns:PobierzCaptcha/>
   </soap:Body>
</soap:Envelope>
'''

CHECK_CAPTCHA_ENVELOPE = '''\
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:ns="http://CIS/BIR/2014/07">
<soap:Header xmlns:wsa="http://www.w3.org/2005/08/addressing">
<wsa:To>{api.service_url}</wsa:To>
<wsa:Action>http://CIS/BIR/2014/07/IUslugaBIR/SprawdzCaptcha</wsa:Action>
</soap:Header>
   <soap:Body>
      <ns:SprawdzCaptcha>
         <ns:pCaptcha>{captcha}</ns:pCaptcha>
      </ns:SprawdzCaptcha>
   </soap:Body>
</soap:Envelope>
'''

SEARCH_ENVELOPE = '''\
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:ns="http://CIS/BIR/PUBL/2014/07" xmlns:dat="http://CIS/BIR/PUBL/2014/07/DataContract">
<soap:Header xmlns:wsa="http://www.w3.org/2005/08/addressing">
<wsa:To>{api.service_url}</wsa:To>
<wsa:Action>http://CIS/BIR/PUBL/2014/07/IUslugaBIRzewnPubl/DaneSzukajPodmioty</wsa:Action>
</soap:Header>
   <soap:Body>
      <ns:DaneSzukajPodmioty>
         <ns:pParametryWyszukiwania>
            {param}
         </ns:pParametryWyszukiwania>
      </ns:DaneSzukajPodmioty>
   </soap:Body>
</soap:Envelope>
'''

FULL_REPORT_ENVELOPE = '''\
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:ns="http://CIS/BIR/PUBL/2014/07">
<soap:Header xmlns:wsa="http://www.w3.org/2005/08/addressing">
<wsa:To>{api.service_url}</wsa:To>
<wsa:Action>http://CIS/BIR/PUBL/2014/07/IUslugaBIRzewnPubl/DanePobierzPelnyRaport</wsa:Action>
</soap:Header>
  <soap:Body>
      <ns:DanePobierzPelnyRaport>
         <ns:pRegon>{regon}</ns:pRegon>
         <ns:pNazwaRaportu>{report_name}</ns:pNazwaRaportu>
      </ns:DanePobierzPelnyRaport>
   </soap:Body>
</soap:Envelope>
'''

SUMMARY_REPORT_ENVELOPE = '''\
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:ns="http://CIS/BIR/PUBL/2014/07">
<soap:Header xmlns:wsa="http://www.w3.org/2005/08/addressing">
<wsa:Action>http://CIS/BIR/PUBL/2014/07/IUslugaBIRzewnPubl/DanePobierzRaportZbiorczy</wsa:Action>
<wsa:To>{api.service_url}</wsa:To>
</soap:Header>
  <soap:Body>
    <ns:DanePobierzRaportZbiorczy>
      <ns:pDataRaportu>{date}</ns:pDataRaportu>
      <ns:pNazwaRaportu>{report_name}</ns:pNazwaRaportu>
    </ns:DanePobierzRaportZbiorczy>
  </soap:Body>
</soap:Envelope>
'''

GET_VALUE_ENVELOPE = '''\
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:ns="http://CIS/BIR/2014/07">
<soap:Header xmlns:wsa="http://www.w3.org/2005/08/addressing">
<wsa:To>{api.service_url}</wsa:To>
<wsa:Action>http://CIS/BIR/2014/07/IUslugaBIR/GetValue</wsa:Action>
</soap:Header>
  <soap:Body>
    <ns:GetValue>
      <ns:pNazwaParametru>{param}</ns:pNazwaParametru>
    </ns:GetValue>
  </soap:Body>
</soap:Envelope>
'''
