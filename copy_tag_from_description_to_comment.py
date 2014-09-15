#!/usr/bin/env python3

# The MIT License (MIT)
#
# Copyright (c) 2014 Keita Kita
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

#
# Copies description tag to comment tag in MP3 file.
#

from mutagenx.id3 import ID3, COMM

import argparse
import logging
import os.path
import sys

logging.basicConfig(level=logging.INFO)

def require_directory(directory):
    if not os.path.isdir(directory):
        sys.exit('%s is not directory.' % (directory))


def get_comment_tag(id3):
    return id3.getall('COMM')


def get_description_text(id3):
    description = id3.getall('TXXX:DESCRIPTION')

    if description:
        return description[0]
    else:
        return None


def create_comment_tag(text):
    return COMM(encoding=3, lang='eng', desc='', text=[text])


def log_file(filepath):
    logging.debug('Processing "%s"' % (filepath))


def log_comment_tag_available():
    logging.debug('\tComment tag is available. Skip.')


def log_tag_copied():
    logging.debug('\tCopied text from description to comment tag.')


def copy_tag_from_description_to_comment(filepath):
    log_file(filepath)

    id3 = ID3(filepath)

    if get_comment_tag(id3):
        log_comment_tag_available()
        return

    description_text = get_description_text(id3)

    if description_text:
        id3.add(create_comment_tag(description_text))
        id3.save()
        log_tag_copied()


def copy_tag_from_description_to_comment_in_directory(root_directory):
    require_directory(root_directory)

    for root, _, files in os.walk(root_directory,):
        [copy_tag_from_description_to_comment(os.path.join(root, filename))
            for filename in files if filename.lower().endswith('.mp3')]


def create_argument_parser():
    parser = argparse.ArgumentParser(
        description='Copies description tag to comment tag in MP3 file.')

    parser.add_argument(
        'root_directory', help='Directory path of search root.')

    return parser


def copy_tag_from_description_to_comment_from_commandline():
    parser = create_argument_parser()

    arguments = parser.parse_args()

    copy_tag_from_description_to_comment_in_directory(arguments.root_directory)


if __name__ == '__main__':
    copy_tag_from_description_to_comment_from_commandline()
