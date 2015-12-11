#!/usr/bin/env python3

import re


class LineProcessor:

    prefixes = {'link': 'https?://', 'email':'@', 'both': 'https?://|@'}

    def __init__(self, from_host, to_host, mode='link'):
        self.__from_host = from_host
        self.__to_host = to_host

        host_escaped = re.escape(from_host)
        prefix = __class__.prefixes[mode]
        self.__host_re = re.compile('('+prefix+')('+host_escaped+')')
        self.__serialized_re = re.compile('s:([0-9]+):(\\\\?")([^"\\\\]*(?:'+prefix+'))('+host_escaped+')([^"\\\\]*)(\\\\?")')
        self.__diff_len = len(to_host) - len(from_host)

    def __replace_host(self, match):
        return '{suffix}{host}'.format(suffix=match.group(1), host=self.__to_host)

    def __replace_serialized_host(self, match):
        new_len = int(match.group(1)) + self.__diff_len
        result = 's:{length}:{q1}{prefix}{host}{suffix}{q2}'
        return result.format(length=new_len,
                             host=self.__to_host,
                             q1 = match.group(2),
                             prefix=match.group(3),
                             suffix = match.group(5),
                             q2 = match.group(6))

    def process(self, line):
        line, serialized_subs = self.__serialized_re.subn(self.__replace_serialized_host, line)
        line, normal_subs = self.__host_re.subn(self.__replace_host, line)
        return line, normal_subs, serialized_subs



if __name__ == '__main__':

    import sys
    import argparse

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

    lp = LineProcessor(from_host, to_host, mode)

    normal_subs = 0
    serialized_subs = 0

    try:
        for line in f_in:
            line, subs1, subs2 = lp.process(line)
            f_out.write(line)
            normal_subs += subs1
            serialized_subs += subs2

    except OSError as e:
        sys.stderr.write("Error({0}): {1}\n".format(e.errno, e.strerror))

    if (args.verbose):
        info = "Replacements: {total} ({n} normal, {s} serialized)"
        total_subs = normal_subs + serialized_subs
        print(info.format(total=total_subs, n=normal_subs, s=serialized_subs))

