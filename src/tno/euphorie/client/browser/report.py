# coding=utf-8


def formatAddress(address, postal, city):
    output = []
    if address:
        output.append(address)
        if postal or city:
            output.append("\n")
    bits = tuple(filter(None, [postal, city]))
    if bits:
        output.append(" ".join(bits))
    return "".join(output) if output else None
