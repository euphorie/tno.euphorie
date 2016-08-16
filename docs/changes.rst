Changelog
=========

5.0.5 (2016-08-16)
------------------

- Upgrade to Plone 4.3.10

5.0.4 (2016-05-31)
------------------
- Do not escape characters of the password in the reminder email (Syslab #13579)
- Don't choke in case an image scale can't be fetched. (Syslab #13623)
- Allow Sectors, Surveys and Surveygroups to be renamed


5.0.3 - March 4, 2016
---------------------
- Expose "obsolete" flag in survey edit form. #106
- Better visibility for password policy and errors on sector settings
form (Syslab #13310)

5.0.2 - October 13, 2015
------------------------

- Fix creation and update of non-Ondernemingsdossier sessions.


5.0.1 - September 28, 2015
--------------------------

- Fix last bad spellings for Ondernemingsdossier.


5.0 - September 15, 2015
------------------------

- Several small textual changes for Ondernemingsdossier-related text.


5.0rc1 - September 11, 2015
---------------------------

- Fix error in CMS survey view for surveys that do not have a regelhulp id set.

- Include session ZODB path in OD link search. This allows for multiple
  different surveys for a single OD user.

- Various Ondernemingsdossier-related text changes.


5.0b3 - August 12, 2015
-----------------------

- Fix another upgrade error.


5.0b2 - August 12, 2015
-----------------------

- Fix an upgrade error.


5.0b1 - August 11, 2015
-----------------------

- Complete support for Ondernemingsdossier


5.0a1 - July 30, 2015
---------------------

- Start integration support of Ondernemingsdossier


4.4 - March 29, 2015
--------------------


- Include Top-5 risks in the online action plan report. This fixes
  `TNO ticket 252 <https://code.simplon.biz/tracker/tno-euphorie/ticket/252>`_.

- Explicitly do not render widgets when we try to use widget instances in the
  report form. This fixes compatibility with current versions of Euphorie 7
  and its underlying software stack.


4.3 - January 14, 2014
----------------------

- Update templates to support CSS changes in Euphorie 6.3.0.

- Add `rel=download` to report download links to faciliate tracking downloads
  in Google Analytics (this requires Euphorie 6.3 or later).


4.2 - December 19, 2013
-----------------------

- Do not restrict absentee percentage to two characters. This fixes
  `TNO ticket 246 <https://code.simplon.biz/tracker/tno-euphorie/ticket/246>`_.


4.1 - October 30, 2013
----------------------

- Support obsolete survey list from Euphorie 6.1


4.0 - May 1, 2013
-----------------

- Adjust code for navigation tree related fixed in Euphorie 6. This is part
  of the fix for 
  `TNO ticket 236 <https://code.simplon.biz/tracker/tno-euphorie/ticket/236>`_.

- Fix loading of ZCML in tests. This fixes problems running tests in current
  Plone versions which update zope.component.


3.1 - December 12, 2012
-----------------------

- Remove extra space after risk severity in action plan report. This fixes
  `TNO ticket 215 <https://code.simplon.biz/tracker/tno-euphorie/ticket/215>`_.

- Improve survey matcher for old survey session importer:  never use survey
  previews, and it multiple surveys are found with the same RI&E id use the
  oldest published survey on the assumption that this is the original survey.
  This fixes part of `TNO ticket 231
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/231>`_.

- Update old survey session importer to detect surveys that can be found but
  where the contents differ so much no survey tree can be build. This fixes
  part of `TNO ticket 231`_.


3.0.1 - November 28, 2012
-------------------------

- Remove debugging leftover in risk action plan form.


3.0 - November 22, 2012
------------------------

- Synchronize with Euphorie 5.

- Add link to identification report to introduction for action plan report.
  This fixes `TNO ticket 228
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/228>`_.


2.1 - September 28, 2012
------------------------

- Client API fix: fix handling of absentee percentage in company data.
  [wichert]

- Client API fix: do not copy address field to postal code field on
  update of company data..
  [wichert]


2.0 - June 18, 2012
-------------------

- Setup Sphinx-based documentation.
  [wichert]

- Update to support the client API introduced in Euphorie 4. Euphorie 4
  is now a minimal requirement.
  [wichert]


1.15 - May 20, 2012
-------------------

- Prepare for client API changes in Euphorie 4.
  [wichert]

- Do not list present risk as warnings in the action plan report. This
  fixes `TNO ticket 219
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/219>`_.
  [wichert]

- Update actionplan report footnote to reflect current behaviour of top-5
  risks. This fixes `TNO ticket 217
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/217>`_.
  [wichert]

- If a module has no description skip it in the client. This fixes the
  tno.euphorie part of `TNO ticket 213
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/213>`_.
  [wichert]

- Really make priority dropdown for top-5 and policy risks readonly.
  Apparently the select HTML element does not support the readonly
  attribute, so use disabled instead. This fixes `TNO ticket 221
  <https://code.simplon.biz/tracker/tno-euphorie/ticket/221>`_.
  [wichert]

- Remove warning-icon for risks with a problem description in the action plan
  report. Since this report only contains present risks the icon was not
  useful. This fixes `TNO ticket 219`_.
  [wichert]


1.14 - April 17, 2012
---------------------

- Skip policy and top-5 risks in action plan phase if they are not
  present.
  [wichert]

- Do not allow changing the priority for top5 and policy risks: they always
  get a high priority.
  [wichert]


1.13 - December 28, 2011
------------------------

- Update MANIFEST to include missing zcml files.
  [wichert]


1.12 - December 28, 2011
------------------------

- Add timeline report option for actionplan report. This requires Euphorie 3.
  [wichert]


1.11 - April 7, 2011
--------------------

- Add note that arbo experts will not automatically receive reports. This fixes
  `TNO ticket 181 <http://code.simplon.biz/tracker/tno-euphorie/ticket/181>`_.
  [wichert]

- Fix SQLAlchemy 0.6 compatibility.
  [wichert]

- Update templates for new account settings tab from Euphorie 2.6.
  [wichert]

- Limit the number of characters for postal code and city fields in the
  company details form, preventing illegal input. This fixes `TNO ticket
  180 <http://code.simplon.biz/tracker/tno-euphorie/ticket/180>`_.
  [wichert]


1.10 - January 25, 2011
-----------------------

- Add local `z3c.appconfig <http://pypi.python.org/pypi/z3c.appconfig>`_
  configuration to disable the terms-and-condtions feature from Euphorie.
  [wichert]

- Update markup for absentee percentage field to hint that it is a percentage.
  This is related to `TNO ticket 167`_.
  [cornae,wichert]


1.9 - January 13, 2011
----------------------

- Update error text for invalid absentee percentage. This fixes 
  `TNO ticket 167 <http://code.simplon.biz/tracker/tno-euphorie/ticket/167>`_.
  [wichert]

- Fix display of absentee in the company data form. This fixes
  `TNO ticket 166 <http://code.simplon.biz/tracker/tno-euphorie/ticket/166>`_.
  [wichert]


1.8 - January 11, 2011
----------------------

- Use the new homelink METAL macro to render the logo and site URL. This is part
  of `TNO ticket 12 <http://code.simplon.biz/tracker/tno-euphorie/ticket/12>`_.
  [wichert]

- Do not accidentily check the *akkoort OR/medewerkersvertegenwoordiging* flag
  after a validation error elsewhere on the company form. This fixes
  `TNO ticket 163 <http://code.simplon.biz/tracker/tno-euphorie/ticket/163>`_.
  [wichert]


1.7 - December 7, 2010
----------------------

Bugfixes
~~~~~~~~

- Do not use (now missing) translations for texts specific to this package. This
  fixes `TNO ticket 152 <http://code.simplon.biz/tracker/tno-euphorie/ticket/152>`_.
  [wichert]

- Show decimals for absentee percentages. This employes a workaround for a
  `zope.i18n bug 686058 <https://bugs.launchpad.net/zope.i18n/+bug/686058>`_.
  This fixes `TNO ticket 162
  <http://code.simplon.biz/tracker/tno-euphorie/ticket/162>`_.
  [wichert]

- Fix display of current number of employees in the company data form. This fixes
  `TNO ticket 151 <http://code.simplon.biz/tracker/tno-euphorie/ticket/151>`_.
  [wichert]



1.6 - November 6, 2010
----------------------

Bugfixes
~~~~~~~~

- Rewrite company form to use z3c.form as form toolkit. This should
  improve form robustness greatly. Fixes `TNO ticket 145
  <http://code.simplon.biz/tracker/tno-euphorie/ticket/145>`_.
  [wichert]

- Correct reStructuredText syntax errors in the changelog.
  [wichert]


1.5 - October 22, 2010
----------------------

Upgrade notes
~~~~~~~~~~~~~

This release updates the profile version to *101*. Please use the upgrade
feature in portal_setup to upgrade the ``tno.euphorie:default`` profile to
this version.

Features
~~~~~~~~

* Allow non-integer absentee percentages in company data. This fixes
  `TNO ticket 142 <http://code.simplon.biz/tracker/tno-euphorie/ticket/142>`_.
  [wichert]


Bugfixes
~~~~~~~~

* Improve check for valid years in company edit form. This fixes
  `TNO ticket 138 <http://code.simplon.biz/tracker/tno-euphorie/ticket/138>`_.
  [wichert]

* Override action plan report download as well. This fixes 
  `TNO ticket 143 <http://code.simplon.biz/tracker/tno-euphorie/ticket/143>`_.
  [wichert]

* Add base infrastructure to run tests for `tno.euphorie`.
  [wichert]

* Update RI&E session loader to update ``dutch_company`` instead of
  ``company``. This fixes `TNO ticket 140
  <http://code.simplon.biz/tracker/tno-euphorie/ticket/140>`_.
  [wichert]


1.4 - October 7, 2010
---------------------

Bugfixes
~~~~~~~~

* Do not treat 0 as not-filled-in when rendering the action plan report.
  This fixes `TNO ticket 130
  <http://code.simplon.biz/tracker/tno-euphorie/ticket/130>`_.
  [wichert]

* Small robustness improvement in id-mapping logic: continue processing a
  module even if it has no external id itself.
  [wichert]

1.3 - October 5, 2010
---------------------

Bugfixes
~~~~~~~~

* Copy the company details handling in the client from euphorie.client here in
  preparation for changes in Euphorie.
  [wichert]


1.2 - September 29, 2010
------------------------

Bugfixes
~~~~~~~~

* Handle missing action plan measure data. This fixes part of `TNO ticket 122
  <http://code.simplon.biz/tracker/tno-euphorie/ticket/114>`_.
  [wichert]


1.1 - September 23, 2010
------------------------

Features
~~~~~~~~

* Configure email settings for real site.
  [wichert]

Bugfixes
~~~~~~~~

* Correct test for existence of profile questions when parsing a session file.
  This fixes part of `TNO ticket 114
  <http://code.simplon.biz/tracker/tno-euphorie/ticket/114>`_.
  [wichert]

* Gracefully handle risks listed in a session file which no longer exist in the
  system. This fixes part of `TNO ticket 114
  <http://code.simplon.biz/tracker/tno-euphorie/ticket/114>`_.
  [wichert]


1.0 - September 17, 2010
------------------------

* Initial release
  [wichert]
