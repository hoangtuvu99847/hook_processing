from typing import Dict, Tuple


def bytes_to_human(n: float) -> str:
    # http://code.activestate.com/recipes/578019
    # >>> bytes_to_human(10000)
    # '9.8K'
    # >>> bytes_to_human(100001221)
    # '95.4M'
    symbols: Tuple[str, ...] = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix: Dict = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n
