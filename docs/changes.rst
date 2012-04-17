Changelog
=========

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
  `TNO ticket 152 <http://code.simplon.biz/tracker/tno-euphorie/ticket/163>`_.
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

