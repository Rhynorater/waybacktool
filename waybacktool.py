#!/usr/bin/env python
import requests
import sys
import json
import argparse
import warnings
import sys
import urlparse
import socket
import multiprocessing

warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser(description='Tool for parsing WayBack URLs.')

parser.add_argument('function', help="`pull` or `check`. `pull` will gather the urls from the WayBack API. `check` will ensure the response code is positive (200,301,302,307).")
parser.add_argument('--host', help='The host whose URLs should be retrieved.')
parser.add_argument('--with-subs', help='`yes` or `no`. Retrieve urls from subdomains of the host.', default=False)
parser.add_argument('--threads',help='The number of threads to use when checking endpoints', default=10, type=int)
parser.add_argument('--loadfile', help='Location of file from which urls should be checked.')
parser.add_argument('--outputfile', help='Location of the file to which checked urls should be reported')

args = parser.parse_args()


def waybackurls(host, with_subs):
    if with_subs:
        url = 'http://web.archive.org/cdx/search/cdx?url=*.%s/*&output=list&fl=original&collapse=urlkey' % host
    else:
        url = 'http://web.archive.org/cdx/search/cdx?url=%s/*&output=list&fl=original&collapse=urlkey' % host
    
    print r.text.strip()
    

def check(data, f):
    noResolve = []
    for url in data:
        url = url.strip("\r").strip().strip('"').strip("'").replace(":80/","/").replace(":443/", "/")
        if url == "":
            continue
        if not url.startswith("http"):
            url = "http://"+url
        parsedUrl = urlparse.urlparse(url)
        domain = parsedUrl.netloc
        if domain in noResolve:
            continue
        try:
            socket.gethostbyname(domain)
        except:
            noResolve.append(domain)
            continue
        try:
            req = requests.head(url, verify=False, timeout=.25)
        except requests.exceptions.Timeout:
            noResolve.append(domain)
            continue
        if str(req.status_code)[0] == "3" and url.startswith("http://") and req.headers['Location'].startswith("https://"):
            try:
                req = requests.head("https"+url[4:], verify=False, timeout=.25)
            except requests.exceptions.Timeout:
                continue
        status_code = req.status_code
        if status_code == 404:
            return 
        if "Content-Length" in req.headers.keys():
            cLength = req.headers["Content-Length"]
        else:
            cLength = "Unknown"
        if  "Content-Type" in req.headers.keys():
            cType = req.headers["Content-Type"]
        else:
            cType = "Unknown"
        if str(status_code)[0] == "3":
            rUrl = req.headers["Location"]
            print ", ".join([url, str(status_code), cLength, cType, rUrl])
            if f:
                f.write(", ".join([url, str(status_code), cLength, cType, rUrl])+"\n")
        else:
            print ", ".join([url, str(status_code), cLength, cType])

if args.function == "pull":
    if args.host:
        waybackurls(args.host, args.with_subs)
    elif args.loadfile:
        for line in open(args.loadfile).readlines():
            waybackurls(line.strip(), args.with_subs)
elif args.function == "check":
    if args.loadfile:
        try:
            if args.outputfile:
                check(open(args.loadfile).readlines(), open(args.outputfile, "w"))
            else:
                check(open(args.loadfile).readlines(), False)
            endpoints = open(args.loadfile).readlines()
            pool = multiprocessing.Pool(args.threads)
            pool.map(check, endpoints)
        except IOError as e:
            print "[-] File not found!"
            exit()
    elif not sys.stdin.isatty():
        if args.outputfile:
            check(sys.stdin.readlines(), open(args.outputfile, "w"))
        else:
            check(sys.stdin.readlines(), False)
        endpoints = sys.stdin.readlines()
        pool = multiprocessing.Pool(args.threads)
        pool.map(check, endpoints)
    else:
        print "[-] Please either specify a file using --loadfile or pipe some data in!"
        exit()
