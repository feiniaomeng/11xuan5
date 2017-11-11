#!/usr/bin/env python
# -*- coding: utf-8 -*-

' get_and_save_url module'

__author__ = 'Helios Lee'

import os
import urllib2
import gzip
import codecs
import StringIO
import zlib

def loadData(url):
    print url
    request = urllib2.Request(url)
    request.add_header('Accept-encoding', 'gzip,deflate')
    response = urllib2.urlopen(request)
    content = response.read()
    encoding = response.info().get('Content-Encoding')
    if encoding == 'gzip':
        content = gzip_decode(content)
    elif encoding == 'deflate':
        content = deflate(content)
    return content.decode("utf-8")

def gzip_decode(data):
    buffer = StringIO.StringIO(data)
    f = gzip.GzipFile(fileobj=buffer)
    return f.read()

def deflate(data):
    try:
        return zlib.decompress(data, -zlib.MAX_WBITS)
    except zlib.error:
        return zlib.decompress(data)


def get_and_save_url_as_file(url, path):
    if os.path.exists(path) == False:
        os.mkdir(path);

    pos = url.rfind("/")
    pos = pos + 1
    file_name = url[pos:]
    f = codecs.open(path + file_name, 'wb', "utf-8");
    f.write(loadData(url));
    f.flush();
    f.close();

    return path + file_name

if __name__ == '__main__':

    get_and_save_url_as_file("http://www.cailele.com/static/info/201709/show_10543454.shtmll", "/home/libo/workspace/spider/wangyi/11xuan5/");