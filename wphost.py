#!/usr/bin/env python3

import argparse
import sys
import re

parser = argparse.ArgumentParser()
parser.add_argument('current_host_name')
parser.add_argument('new_host_name')
parser.add_argument('input_file', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
parser.add_argument('output_file', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
parser.add_argument('-v', '--verbose', action='store_true', help='show the number of replacements made')
parser.add_argument('-m', '--mode', choices=['link', 'email', 'both'], default='link')

args = parser.parse_args()

f_in = args.input_file
f_out = args.output_file
from_host = args.current_host_name
to_host = args.new_host_name
mode = args.mode

host_escaped = re.escape(from_host);

prefixes = {'link': 'https?://', 'email':'@', 'both': 'https?://|@'}
prefix = prefixes[mode]

host_re = re.compile('('+prefix+')('+host_escaped+')')
serialized_re = re.compile('s:([0-9]+):"([^"]*(?:'+prefix+'))('+host_escaped+')([^"]*)"')

diff_len = len(to_host) - len(from_host)

def replace_host(match):
    return '{suffix}{host}'.format(suffix=match.group(1), host=to_host)

def replace_serialized_host(match):
    new_len = int(match.group(1)) + diff_len
    result = 's:{length}:"{prefix}{host}{suffix}"'
    return result.format(length=new_len,
                         host=to_host,
                         prefix=match.group(2),
                         suffix = match.group(4))

normal_subs = 0
serialized_subs = 0
total_subs = 0

try:
    for line in f_in:
        line, num_subs = serialized_re.subn(replace_serialized_host, line)
        serialized_subs += num_subs
        total_subs += num_subs

        line, num_subs = host_re.subn(replace_host, line)
        normal_subs += num_subs
        total_subs += num_subs
        f_out.write(line)
except OSError as e:
    sys.stderr.write("Error({0}): {1}\n".format(e.errno, e.strerror))

if (args.verbose):
    info = "Replacements: {total} ({n} normal, {s} serialized)"
    print(info.format(total=total_subs, n=normal_subs, s=serialized_subs))

