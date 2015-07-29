import logging

log = logging.getLogger(__name__)


def updateAbsenteePercentage(context):
    from z3c.saconfig import Session
    from euphorie.deployment.upgrade.utils import ColumnType
    from zope.sqlalchemy import datamanager

    session=Session()
    if ColumnType(session, "dutch_company", "absentee_percentage")=="numeric(5,2)":
        return

    log.info("Changing type for dutch_company.absentee_percentage to NUMERIC(5,2)")
    session.execute("ALTER TABLE dutch_company ALTER COLUMN absentee_percentage TYPE NUMERIC(5,2);")
    datamanager.mark_changed(session)
