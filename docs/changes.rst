Changelog
=========

9.0.1 (2021-08-22)
------------------

- Fixed the custom measures_overview to work with wkhtml2pdf

9.0.0 (2021-08-21)
------------------

This branch will prepare for the migration to Plone5.2 and ultimately to python3.
A big milestone will be the removal of Grok.

8.1.6 (unreleased)
------------------

- Nothing changed yet.


8.1.5 (2020-02-26)
------------------

- Add missing alembic upgrade step

8.1.4 (2020-02-25)
------------------

- Customize template for Start (Preparation), to keep old functionality


8.1.3 (2019-11-07)
------------------

- Fix brown-bag release

8.1.2 (2019-11-07)
------------------

- Start using alembic for keeping DB up to date
- Fix translation issue

8.1.1 (2019-09-03)
------------------

- Adapt to Euphorie 11.1 that uses deep-linking


8.1.0 (2019-08-20)
------------------

- Switch to Euphorie 11, with improved UI: the tool navigation
  is now part of the Phase navigation


8.0.3 (2019-03-29)
------------------

- Action plan: TNO's version has the specialty that top5 risks that have not
  yet been answered are NOT shown in the action plan. Fixed a bug in the
  navigtion that came from conflicting computation of affected risks and
  modules.


8.0.2 (2019-03-20)
------------------

- CMS: on error unauth page, fix link to reset PW form

8.0.1 (2019-02-28)
------------------

- Fix broken release 8.0.0

8.0.0 (2019-02-26)
------------------

- Upgrade to Plone5
- Switch to outputting .docx natively


7.0.0b3 (2018-10-25)
--------------------

- Nothing changed yet.


7.0.0b2 (2018-10-23)
--------------------

- Nothing changed yet.


7.0.0b1 (2018-10-23)
--------------------

- Switch to Plone5


6.0.15 (2018-07-13)
-------------------

- Bugfix for the "measures" report: Do not rely on the pre-computed
  list of modules, since this can fail for a scenario with 
  module->module->Optional module

6.0.14 (2017-11-01)
-------------------

- Another bugfix for the "measures" report. Correctly compute the
  future months

6.0.13 (2017-10-31)
-------------------

- Fix indentation in changelog, attempt another release

6.0.12 (2017-10-31)
-------------------

- Attempt another release, since 6.0.11 might not be working (?)

6.0.11 (2017-10-27)
-------------------

- Measures report: fix logic for calculating 1) which measures need to be shown,
  2) what class to assing (ongoing etc)


6.0.10 (2017-10-18)
-------------------

Changed:

- The measures_overview report has been customised from Euphorie to
  show not only the start of a measure, but their complete time span.
  A general design fix of theis report has taken place.
  NOTE: requires PrinceXML version 11!

6.0.9 (2017-09-04)
------------------

- Fix translation issue on report landing ("Use it to")
- Bump Euphorie to 9.0.23

6.0.8 (2017-08-23)
------------------

- Bump Euphorie to 9.0.22

6.0.7 (2017-05-11)
------------------

- Typo in Help text for 'Regelhulp Id'


6.0.6 (2017-04-20)
------------------

- Bump Euphorie to 9.0.12 to get the notification for outdated tools.
  #15240


6.0.5 (2017-03-30)
------------------

- Fix link for downloading list of all risks on report landing


6.0.4 (2017-03-17)
------------------

- More text changes / typos

6.0.3 (2017-03-13)
------------------

- Remove debug output from report landing page

6.0.2 (2017-03-13)
------------------

- Translation changes

6.0.1 (2017-02-02)
------------------

- Nothing changed yet.


6.0.0 (2017-01-31)
------------------

- Major change: upgrade to "OiRA 2.0" user interface

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
