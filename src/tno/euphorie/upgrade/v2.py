import logging
import transaction
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.schema import MetaData
from sqlalchemy.schema import Table
from z3c.saconfig import Session
from zope.sqlalchemy import datamanager
from euphorie.deployment.upgrade.utils import TableExists
from tno.euphorie.model import OdLink


log = logging.getLogger(__name__)


# Modified version of euphorie.deployment.upgarde.utils.ColumnExists which
# fixes the last argument to reflecttable.
def column_exists(session, table, column):
    connection = session.bind
    metadata = MetaData(connection)
    table = Table(table, metadata)
    try:
        connection.dialect.reflecttable(connection, table, None, [])
    except NoSuchTableError:
        return False
    return column in table.c


def add_od_table(context):
    session = Session()
    if not TableExists(session, OdLink.__tablename__):
        OdLink.__table__.create(session.bind)
        log.info("Added new 'od_link' table")


def add_od_version_column(context):
    session = Session()
    if column_exists(session, 'od_link', 'version'):
        return
    transaction.get().commit()
    session.execute('ALTER TABLE od_link ADD COLUMN version INT DEFAULT 0 NOT NULL')
    datamanager.mark_changed(session)
    transaction.get().commit()
    log.info("Added new column 'version' to table 'od_link'")
