# -*- coding: UTF-8 -*-
from tno.euphorie.upgrade.utils import alembic_upgrade_to


def alembic_upgrade(context):
    alembic_upgrade_to("210")

