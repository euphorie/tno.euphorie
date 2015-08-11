import logging
import transaction
from z3c.saconfig import Session
from zope.sqlalchemy import datamanager
from euphorie.deployment.upgrade.utils import TableExists
from euphorie.deployment.upgrade.utils import ColumnExists
from tno.euphorie.model import OdLink


log = logging.getLogger(__name__)


def add_od_table(context):
    session = Session()
    if not TableExists(session, OdLink.__tablename__):
        OdLink.__table__.create(session.bind)
        log.info("Added new 'od_link' table")


def add_od_version_column(context):
    session = Session()
    if ColumnExists(session, 'od_link', 'version'):
        return
    transaction.egt().commit()
    session.execute('ALTER TABLE od_link ADD COLUMN version INT DEFAULT 0 NOT NULL')
    datamanager.mark_changed(session)
    transaction.get().commit()
    log.info("Added new column 'version' to table 'od_link'")
