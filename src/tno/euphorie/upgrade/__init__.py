try:
    from plone.app.upgrade.bbb import ITinyMCE  # noqa: F401
except ImportError:
    from . import bbb
    from plone.app.upgrade.utils import alias_module

    alias_module("plone.app.upgrade.bbb", bbb)
