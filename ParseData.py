
# coding=utf-8

from bs4 import BeautifulSoup
import sys
import os
import re
import codecs


ResultPrefix = "result"
ResultPath = '/home/libo/workspace/spider/wangyi/11xuan5/'

def filter_one_day_data(filename_with_path):
    temp_buf = codecs.open(filename_with_path, 'r', "utf-8");
    bf = BeautifulSoup(temp_buf, 'html.parser')
    one_day_results = {}
    for c in bf.find_all('tr', {'class': re.compile(r'|bg_grey')}):
        if c != None and len(c.contents) and c.contents[0].string and len(c.contents[0].string):
            period_time = int(c.contents[0].string)
            if period_time < 1 or period_time > 82:
                continue
            #print "peroid_time = ", period_time
            period_result = ''
            for d in c.find_all('li', {'class': 'ball wred-24'}):
                #print d
                if len(period_result):
                    period_result += ' '
                period_result = period_result +  d.string
                one_day_results[period_time] = period_result
    temp_buf.close()
    return one_day_results

def write_result_to_file(filename_with_path, one_day_results):
    file_obj = codecs.open(filename_with_path, 'w', 'utf-8')
    for per_time_result in one_day_results.values():
        file_obj.write(per_time_result + '\n')
    file_obj.flush();
    file_obj.close()
    print filename_with_path

def filter_one_day_data_and_save(filename_with_path):

    basename_string = os.path.basename(filename_with_path)
    pos = basename_string.find('.')
    splitstrings = basename_string[:pos].split('-', 5)

    if len(splitstrings) < 5:
        return None

    result_filename_with_path = ResultPath + ResultPrefix + '/' + splitstrings[2] + '-' + splitstrings[3] + '-' + splitstrings[4] + '.txt'

    write_result_to_file(result_filename_with_path, filter_one_day_data(filename_with_path))
    return result_filename_with_path

def get_days_result_path():
    pass

def filter_data(path):
    if os.path.exists(path) == False:
        print "No data need to be filter."
        sys.exit(2);
    filter_data("/Users/libo/workspace/spider/wangyi/11xuan5/data/")

#
#filter_one_day_data_and_save('/Users/libo/workspace/spider/wangyi/11xuan5/data/js11x5-kjjg-2017-11-02.htm')