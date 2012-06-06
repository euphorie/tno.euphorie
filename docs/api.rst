Client API support
==================

Euphorie implements a `REST API
<http://euphorie.readthedocs.org/en/latest/api.html>`_ for its client.
tno.euphorie modifies this API in two ways:

1. the company methods are updated to use the company data used in the
   Dutch RI&E site instead of the standard Euphorie company data.
2. the flow through the action plan phase followed the RI&E standard
   instead of the standard Euphorie flow.

The second change is completely transparent and does not require any
changes to API clients. Clients do need to be updated to handle the
different company data. Clients can detect which company is data used
by looking at the ``type`` key: tno.euphorie sets this to ``dutch-company``.


View company details
~~~~~~~~~~~~~~~~~~~~


+------+-----------------------------------------------+------------------------------+
| Verb | URI                                           | Description                  |
+======+===============================================+==============================+
| GET  | /users/<userid>/sessions/<session id>/company | Request company information  |
+------+-----------------------------------------------+------------------------------+

This interface will return information about the company to which this survey
session applies. The response is returned in the form of a JSON object
containing all known information about the company. The type field for the
response will be set to ``dutch-company``. The possible fields are:

+-------------------------+---------------+----------+--------------------------------+
|  Field                  | Type          | Required |                                |
+=========================+===============+==========+================================+
| ``title``               | string        | No       | Company title.                .|
+-------------------------+---------------+----------+--------------------------------+
| ``visit-address``       | object        | No       | Visitors address. This is an   |
|                         |               |          | object with three string       |
|                         |               |          | fields: ``address``, ``city``  |
|                         |               |          | and ``postal``.                |
+-------------------------+---------------+----------+--------------------------------+
| ``postal-address``      | object        | No       | Postal address. This is an     |
|                         |               |          | object with three string       |
|                         |               |          | fields: ``address``, ``city``  |
|                         |               |          | and ``postal``.                |
+-------------------------+---------------+----------+--------------------------------+
| ``email``               | string        | No       | Contact email address.         |
+-------------------------+---------------+----------+--------------------------------+
| ``phone``               | string        | No       | Contact phone number.          |
+-------------------------+---------------+----------+--------------------------------+
| ``activity``            | string        | No       | Company activity.              |
+-------------------------+---------------+----------+--------------------------------+
| ``department``          | string        | No       | Company department.            |
+-------------------------+---------------+----------+--------------------------------+
| ``location``            | string        | No       | Location of the department.    |
|                         |               |          | This is necessary if there are |
|                         |               |          | multiple locations/buildings   |
|                         |               |          | at the same address.           |
+-------------------------+---------------+----------+--------------------------------+
| ``employees``           | string        | No       | The number of employees.       |
+-------------------------+---------------+----------+--------------------------------+
| ``employees-options``   | string        | No       | A list of allowed options for  |
|                         |               |          | for the employees field. Each  |
|                         |               |          | entry is an object with two    |
|                         |               |          | string keys: ``value`` and     |
|                         |               |          | ``title``.                     |
+-------------------------+---------------+----------+--------------------------------+
| ``absentee-percentage`` | integer       | No       | Absentee percentage.           |
+-------------------------+---------------+----------+--------------------------------+
| ``accidentens``         | integer       | No       | Total number of accidents for  |
|                         |               |          | the last year.                 |
+-------------------------+---------------+----------+--------------------------------+
| ``incapacitated-        | integer       | No       | Total number of incapacitated  |
| workers``               |               |          | (WIA) workers last year.       |
+-------------------------+---------------+----------+--------------------------------+
| ``submitter``           | object        | No       | The person who is submitting   |
|                         |               |          | the survey. This is an object  |
|                         |               |          | with two string keys: ``name`` |
|                         |               |          | and ``function``.              |
+-------------------------+---------------+----------+--------------------------------+
| ``submitted``           | string with   | No       | The date when the data for the |
|                         | ISO-formatted |          | survey was collected.          |
|                         | date          |          | survey was collected.          |
+-------------------------+---------------+----------+--------------------------------+
| ``arbo-expert``         | string        | No       | Name of health & safety        |
|                         |               |          | department or expert.          |
+-------------------------+---------------+----------+--------------------------------+
| ``works-council-        | string with   | No       | The date on which the work     |
| approval``              | ISO-formatted |          | council approved the survey.   |
+-------------------------+---------------+----------+--------------------------------+


Update company details
~~~~~~~~~~~~~~~~~~~~~~

+------+-----------------------------------------------+------------------------------+
| Verb | URI                                           | Description                  |
+======+===============================================+==============================+
| PUT  | /users/<userid>/sessions/<session id>/company | Update company details.      |
+------+-----------------------------------------------+------------------------------+

This interface will update the company information for a survey session.
See the `View company details`_ section for the supported fields.
