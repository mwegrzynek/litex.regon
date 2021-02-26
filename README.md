litex.regon - a frontend for Polish REGON database
==================================================

Simple, pythonic wrapper for REGON database (web frontend is reachable at
https://wyszukiwarkaregon.stat.gov.pl/appBIR/index.aspx). To access its SOAP
API, one needs an USER_KEY issued by REGON administrators available at
Regon_Bir@stat.gov.pl.

Usage example below:

```python
>>> from litex.regon import REGONAPI
```

REGONAPI accepts one argument: service URL (provided by REGON Administrators).

```python
>>> api = REGONAPI(SERVICE_URL)
```

First, one needs to log in (using provided user key)

```python
>>> api.login(USER_KEY)
```

After login, one can start querying the database. The search method
accepts the following parameters:

 - `regon` - single REGON number (either 9 or 14 digits long)
 - `krs` - single 10 digit KRS number
 - `nip` - single NIP (10 digits string)
 - `regons` - a collection of REGONs (all of them have to be either 14 or 9 digits long)
 - `krss` - a collection of KRSs
 - `nips` - a collection of NIPs

Only one parameter is used in the query. If multiple ones are passed, first
from the above list is taken into account.

Additionally, a `detailed` parameter can be passed: `detailed=True` causes search method to
fetch default detailed report.

```python
>>> entities = api.search(nip='9999999999')
```

`entities` is a list of LXML objectify objects wrapping the search results (up to 100).
If search was called with `detailed=True`, the full report is available as the `detailed` attribute.

If one knows the REGON of a business entity and an detailed report name, a full report can be fetched
directly:

```python
>>> detailed_report = api.full_report('99999999', 'PublDaneRaportFizycznaOsoba')
```

Summary report with a list of REGONs for the given criteria can be fetched by:

```python
>>> summary_report = api.summary_report(
        '2020-01-01', 
        'BIR11NowePodmiotyPrawneOrazDzialalnosciOsFizycznych'
    )
```

Report names can be found in the documentation provided by REGON admins.

Changes
=======
1.0.6
-----

- more meaningful error messages in search method (thanks @m-ganko)
- summary reports (also kudos to @m-ganko)


1.0.5
-----
 - reworked REGON cleanup logic (in search function, when fetching detailed report)
 - search method now uses DaneSzukajPodmioty (API version 1.1) call instead of DaneSzukaj
   (thanks to @kicaj for pull request)


1.0.4
-----
 - migration from nose to py.test
 - tox configuration for Python 2 and 3 testing
 - improved handling of detailed reports (thanks to @miloszsobiczewski for logging an issue)

1.0.3
-----
 - Python 3.6 compatibility (thanks to Mariusz Witek)

1.0.2
-----
 - CAPTCHA removal -- no longer needed in current API

1.0.1
-----
 - detailed report fetching logic reworked

1.0.0
-----
 - initial release
