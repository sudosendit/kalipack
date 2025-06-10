#!/usr/bin/python3
import urllib.request
import urllib.error


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
