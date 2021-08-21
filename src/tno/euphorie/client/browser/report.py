# coding=utf-8


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
