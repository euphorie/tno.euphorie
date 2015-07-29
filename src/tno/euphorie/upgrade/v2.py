import logging
from z3c.saconfig import Session
from euphorie.deployment.upgrade.utils import TableExists
from euphorie.client import model
from tno.euphorie.model import OdLink


log = logging.getLogger(__name__)


def addOdTables(context):
    session = Session()
    if not TableExists(session, OdLink.__tablename__):
        OdLink.__table__.create(session.bind)
        log.info("Added new 'od_link' table")
