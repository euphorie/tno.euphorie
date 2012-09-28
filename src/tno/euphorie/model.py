from sqlalchemy import orm
from sqlalchemy.sql import functions
from sqlalchemy import schema
from sqlalchemy import types
from euphorie.client.model import BaseObject
from euphorie.client.enum import Enum


class DutchCompany(BaseObject):
    """Information about a Dutch company."""
    __tablename__ = "dutch_company"

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    session_id = schema.Column(types.Integer(),
        schema.ForeignKey("session.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False, index=True)
    session = orm.relation("SurveySession",
            cascade="all,delete-orphan", single_parent=True,
            backref=orm.backref("dutch_company", uselist=False, cascade="all"))

    title = schema.Column(types.Unicode(128))
    address_visit_address = schema.Column(types.UnicodeText())
    address_visit_postal = schema.Column(types.Unicode(16))
    address_visit_city = schema.Column(types.Unicode(64))
    address_postal_address = schema.Column(types.UnicodeText())
    address_postal_postal = schema.Column(types.Unicode(16))
    address_postal_city = schema.Column(types.Unicode(64))
    email = schema.Column(types.String(128))
    phone = schema.Column(types.String(32))
    activity = schema.Column(types.Unicode(64))
    submitter_name = schema.Column(types.Unicode(64))
    submitter_function = schema.Column(types.Unicode(64))
    department = schema.Column(types.Unicode(64))
    location = schema.Column(types.Unicode(64))
    submit_date = schema.Column(types.Date(), default=functions.now())
    employees = schema.Column(Enum([None, "40h", "max25", "over25"]))
    absentee_percentage = schema.Column(types.Numeric(precision=5, scale=2))
    accidents = schema.Column(types.Integer())
    incapacitated_workers = schema.Column(types.Integer())
    arbo_expert = schema.Column(types.Unicode(128))
    works_council_approval = schema.Column(types.Date())


_instrumented = False
if not _instrumented:
    from sqlalchemy.ext import declarative
    from euphorie.client import model
    declarative.instrument_declarative(DutchCompany, model.metadata._decl_registry, model.metadata)
    _instrumented = True
