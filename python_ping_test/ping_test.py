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

import subprocess

import click
import os


@click.command()
@click.option("-i", "--input_type", help="input type file or list", type=str, default=lambda: os.environ.get('input_type', ''))
@click.option("-f", "--file_name", help="read list from file", type=str, default=lambda: os.environ.get('file_namne', ''))
@click.option("-l", "--url_list", help="url list to ping", type=str, default=lambda: os.environ.get('url_list', ''))
def cli(input_type, file_name, url_list):
    """
    using a list of URLs or IP address to run ping and capture min/avg/max rtt
    input can be a file or user entered values
    :param input_type: either file or list as data source
    :param file_name: if type=file use this file containing the URL list
    :param url_list: if type=list use manually entered comma-separated list of URLs
    :return: None
    """

    # if type=file read the file and generate a list of URLs to ping
    # assumes file is a simple text file with one URL per row
    if input_type == 'file':
        ping_list = []
        with open(file_name) as f:
            print(f'\nreading target list from fle {file_name}\n')
            for line in f.readlines():
                ping_list.append(line.rstrip())

    # if type=list read in the user-entered list of values
    elif input_type == 'list':
        ping_list = url_list.split(',')
        print('\n')

    # type must be file or list. exit if other value
    else:
        print('input type unknown. Type must be file or list')
        exit()

    for target in ping_list:
        # iterate through the list values and ping the target
        # using harcoded 5 ping attempts
        try:
            response = subprocess.run(
                ['ping', '-c', '5', target],
                stdout=subprocess.PIPE,  # get all output
                stderr=subprocess.PIPE
            )

        except subprocess.CalledProcessError:
            response = None

        # convert the response output to a string to get the min/avg/max values
        response_output = str(response)
        print(f'{target}')

        # return code 0 = successful ping
        if response.returncode == 0:
            response_rtt = {}
            # this is a manual parse of the ping response message getting the min/avg/max output
            # there may be dependencies on the output view based on OS
            # first split is the summary results, second removes the ' ms' at the end
            # third split parses out the min/avg/max values to add to the dict
            response_rtt['min'] = (response_output.split(' = ')[1].split(' '))[0].split('/')[0]
            response_rtt['avg'] = (response_output.split(' = ')[1].split(' '))[0].split('/')[1]
            response_rtt['max'] = (response_output.split(' = ')[1].split(' '))[0].split('/')[2]

            print(f"  min rtt is: {response_rtt['min']} ms")
            print(f"  avg rtt is: {response_rtt['avg']} ms")
            print(f"  max rtt is: {response_rtt['max']} ms\n")

        # return code 2 returned if ping timeouts occur due to slow network or unreachable IP address
        elif response.returncode == 2:
            print('  Error: ping request timeouts occurred')

        # return code 68 is based on DNS lookup error: cannot resolve address
        elif response.returncode == 68:
            print(f'  {response.stderr.decode()}')

        # any other error condition lands here with a catch-all message
        else:
            print(' Error processing pings. Check inputs')


if __name__ == '__main__':
    cli()
