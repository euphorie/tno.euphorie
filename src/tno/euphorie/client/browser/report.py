# coding=utf-8
from euphorie.client.browser import report


def formatAddress(address, postal, city):
    output = []
    if address:
        output.append(address)
        if postal or city:
            output.append(u"\n")
    bits = filter(None, [postal, city])
    if bits:
        output.append(u" ".join(bits))
    return u"".join(output) if output else None


class ReportLanding(report.ReportLanding):
    """Custom report landing page.

    This replaces the standard online view of the report with a page
    offering the RTF and XLSX download options.
    """

    pass
