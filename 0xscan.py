#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 0xScan v1.0
# Coded By: Abdullah AlZahrani (0xAbdullah)

import urllib, urllib2, requests
import lxml.html
import socket
import os, sys, re, argparse
import threading
from BeautifulSoup import BeautifulSoup



print '''
    0xScan v1.0 Coded By: Abdullah AlZahrani
   ___           ____     ____      _      _   _
  / _ \  __  __ / ___|   / ___|    / \    | \ | |
 | | | | \ \/ / \___ \  | |       / _ \   |  \| |
 | |_| |  >  <   ___) | | |___   / ___ \  | |\  |
  \___/  /_/\_\ |____/   \____| /_/   \_\ |_| \_|
    Twitter: @0xAbdullah | GitHub.com/0xAbdullah'''

if len(sys.argv) == 1:
        print "\n\n\033[1;33m[!] Usage: python 0xscan.py -s example.com\033[1;m"
        sys.exit(1)

parser = argparse.ArgumentParser(description="0xScan is website scanner")
parser.add_argument( '-s', required=True, default=None, help='target domain')
args = vars(parser.parse_args())

target = args['s']

if target.startswith("http"):
    print "\n\n\033[1;33m[!] Enter Just Domain // ex: example.com\033[1;m"
    sys.exit()
headers = { 'User-Agent' : 'Mozilla/5.0' }

IP = socket.gethostbyname(target)

r = requests.get("http://"+target, headers = headers)
print "\n[-] ./HTTP Headers"
print "[--] IP: %s" % (IP)
print "[--] Domain: %s" % (target)
print "[--] Webserver: %s" % (r.headers["server"])
try:
    print "[--] X-Powered: %s" % (r.headers["X-Powered-By"])
    print "[--] Content-Encoding: %s" % (r.headers["Content-Encoding"])
    print "[--] Connection: %s" % (r.headers["Connection"])
    print "[--] Transfer-Encoding: %s" % (r.headers["Transfer-Encoding"])
    print "[--] Link: %s" % (r.headers["Link"])
except:
    pass

########### ./Start DEC ###########
print "\n[-] ./Directory Exists Check"
FEcheck = open("data/Directory", "r")

def DEC():
    """thread DFC function"""
    for Path in FEcheck:
        Path = Path.strip()
        try:
            check = requests.head("http://"+target+"/"+Path)
            if check.status_code == 200:
                print "[--] http://%s/%s" % (target, Path)
        except:
            pass
    return

threads = []
for i in range(99):
    t = threading.Thread(target=DEC)
    threads.append(t)
    t.start()
t.join()
########### ./End DEC ###########

########### ./Start FEC ###########
print "\n[-] ./File Exists Check"
FEcheck = open("data/Files", "r")

def FEC():
    """thread DFC function"""
    for Path in FEcheck:
        Path = Path.strip()
        try:
            check = requests.head("http://"+target+"/"+Path)
            if check.status_code == 200:
                print "[--] http://%s/%s" % (target, Path)
        except:
            pass
    return

threads = []
for i in range(99):
    t = threading.Thread(target=FEC)
    threads.append(t)
    t.start()
t.join()
########### ./End FEC ###########

########### ./Start FAP ###########
print "\n[-] ./Find Admin Page"
FEcheck = open("data/Admin", "r")

def FAP():
    """thread FAP function"""
    for Path in FEcheck:
        Path = Path.strip()
        try:
            check = requests.head("http://"+target+"/"+Path)
            if check.status_code == 200:
                print "[--] http://%s/%s" % (target, Path)
        except:
            pass
    return

threads = []
for i in range(50):
    t = threading.Thread(target=FAP)
    threads.append(t)
    t.start()
t.join()
########### ./End FAP ###########

########### ./Start ELP ###########
print "\n[-] ./Extract Links from Page"
try:
    req = urllib2.Request('http://'+target, None, headers)
    html_page = urllib2.urlopen(req)
    soup = BeautifulSoup(html_page)
    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        print "[--] "+link.get('href')
except:
    print "[--] Not Found!"
########### ./End ELP ###########


print "\n[-] ./SQL Injection Scan"
Found = 0
connection = urllib.urlopen("https://www.bing.com/search?q=ip:"+IP+" php?id=", None, headers)
dom =  lxml.html.fromstring(connection.read())
for url in dom.xpath('//a/@href'):
    url = url.strip()
    BlackList = "https://go.microsoft", "http://go.microsoft", "http://www.microsofttranslator.com"
    if url.startswith(BlackList):
        pass
    elif not url.startswith('http://') or url.startswith('https://') or url.startswith('www.'):
        pass
    elif not "=" in url:
        pass
    else:
        check = "'"
        checker = requests.post(url+check)
        if "MySQL" in checker.text:
            print "[--] Found > %s" % (url)
            Found = 1
        elif "native client" in checker.text:
            print "[--] Found > %s" % (url)
            Found = 1
        elif "syntax error" in checker.text:
            print "[--] Found > %s" % (url)
            Found = 1
        elif "ORA" in checker.text:
            print "[--] Found > %s" % (url)
            Found = 1
        elif "MariaDB" in checker.text:
            print "[--] Found > %s" % (url)
            Found = 1
        elif "You have an error in your SQL syntax;" in checker.text:
            print "[--] Found > %s" % (url)
            Found = 1
        else:
            pass
if Found == 0:
    print "[--] SQL Injection Not Found!"
else:
    pass

print "\n[-] ./Port Scan"
def PortsScan():
    """thread Ports Scan function"""
    for port in range(1, 1025):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.2)
        result = sock.connect_ex((IP, port))
        if result == 0:
            print("[--] Port %s: Open" % (port))
        sock.close()

threads = []
t = threading.Thread(target=PortsScan)
threads.append(t)
t.start()
