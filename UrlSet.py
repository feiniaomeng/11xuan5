#!/usr/bin/env python
# -*- coding: utf-8 -*-

' create the all set of url module'

__author__ = 'Helios Lee'

import datetime
import SaveUrlAsFile
def get_all_date(start_day, end_day):
    all_days = []
    start = datetime.datetime.strptime(start_day, '%Y-%m-%d')
    end = datetime.datetime.strptime(end_day, '%Y-%m-%d')

    while start <= end:
        all_days.append(start.strftime('%Y-%m-%d'))
        start += datetime.timedelta(days=1)
        #print start.strftime('%Y-%m-%d')

    return all_days;

def get_all_url(url_site, start_day, end_day):
    request_urls = []
    all_days = get_all_date(start_day, end_day);
    while len(all_days) > 0:
        temp_url = url_site + 'js11x5-kjjg-' + all_days.pop() + ".htm";
        #print temp_url
        request_urls.append(temp_url);
    return request_urls;

if __name__ == '__main__':
    all_request_urls = get_all_url("http://kjh.55128.cn/", "2016-10-21", "2017-10-28")

    for i in all_request_urls:
        print i
        #print ("序号：%s   值：%s" % (all_request_urls.index(i) + 1, i))
        SaveUrlAsFile.get_and_save_url_as_file(i,
                                               "/home/libo/workspace/spider/wangyi/11xuan5/")
    SaveUrlAsFile.get_and_save_url_as_file("http://kjh.55128.cn/js11x5-kjjg-2017-10-23.htm", "/home/libo/workspace/spider/wangyi/11xuan5/")




