#!/usr/bin/env python3

import sys
import re

fname = sys.argv[1]
from_host = sys.argv[2]
to_host = sys.argv[3]

host_escaped = re.escape(from_host);

host_re = re.compile('(https?://|@)('+host_escaped+')')
serialized_re = re.compile('s:([0-9]+):"([^"]*(?:https?://|@))('+host_escaped+')([^"]*)"')

diff_len = len(to_host) - len(from_host)

def replace_host(match):
    return match.group(1)+to_host

def replace_serialized_host(match):
    new_len = int(match.group(1)) + diff_len
    result = 's:{length}:"{prefix}{host}{suffix}"'
    return result.format(length=str(new_len),
                         host=to_host,
                         prefix=match.group(2),
                         suffix = match.group(4))

with open(fname, encoding='utf-8') as fp:
    for line in fp:
        line = serialized_re.sub(replace_serialized_host, line)
        line = host_re.sub(replace_host, line)
        print(line, end='')

