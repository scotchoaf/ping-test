#!/usr/bin/env python3
# Copyright (c) 2018, Palo Alto Networks
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# Authors: Scott Shoaf, Kenny Welshons

import click
import subprocess


@click.command()
@click.option("-i", "--input_type", help="input type file or list", type=str, default='file')
@click.option("-f", "--file_name", help="read list from file", type=str, default=None)
@click.option("-l", "--url_list", help="url list to ping", type=str, default=None)

def cli(input_type, file_name, url_list):
    """
    process a list of url or ip targets and get ping results
    """

    if input_type == 'file':
        ping_list = []
        with open(file_name) as f:
            print(f'\nreading target list from fle {file_name}\n')
            for line in f.readlines():
                ping_list.append(line.rstrip())
    else:
        ping_list = url_list.split(',')
        print('\n')

    for target in ping_list:
        try:
            response = subprocess.run(
                ['ping', '-c', '5', target],
                stdout=subprocess.PIPE,  # get all output
                stderr=subprocess.PIPE
            )

        except subprocess.CalledProcessError:
            response = None

        response_output = str(response)
        print(f'{target}')

        if response.returncode == 0:
            response_rtt = {}
            # this is a manual parse of the ping response message getting the min/avg/max output
            # there may be dependencies on the output view based on OS
            response_rtt['min'] = (response_output.split(' = ')[1].split(' '))[0].split('/')[0]
            response_rtt['avg'] = (response_output.split(' = ')[1].split(' '))[0].split('/')[1]
            response_rtt['max'] = (response_output.split(' = ')[1].split(' '))[0].split('/')[2]

            print(f"  min rtt is: {response_rtt['min']} ms")
            print(f"  avg rtt is: {response_rtt['avg']} ms")
            print(f"  max rtt is: {response_rtt['max']} ms\n")

        elif response.returncode == 2:
            print('  Error: ping request timeouts occurred')

        elif response.returncode == 68:
            print(f'  {response.stderr.decode()}')

        else:
            print(' Error processing pings. Check inputs')


if __name__ == '__main__':
    cli()