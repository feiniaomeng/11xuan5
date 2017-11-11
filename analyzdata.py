#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

import fileinput
from itertools import combinations, permutations
import re
import os
import codecs

import SaveUrlAsFile
import ParseData

import pandas as pd
import UrlSet


OptiniumPath = '/Users/libo/workspace/spider/wangyi/11xuan5/optionium/'

open_debug = 0

def analyz_data(file_name_with_path):
    all_result_in_one_day = []
    for line in fileinput.input(file_name_with_path):
        if line:
            temp_result = re.split(" ", line.strip());
            if len(temp_result) == 5 :
                all_result_in_one_day.append(temp_result);
    if open_debug:
        print all_result_in_one_day
    return all_result_in_one_day

def get_any_two_number():
    any_two_number = list(combinations(["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"], 2))
    return any_two_number;


def calc_bonus_with_one_period(buy_numbers=[], result_numbers=[]):
    bonus = 0
    if open_debug:
        print "buy numbers = " , buy_numbers , "result_numbers " , result_numbers
    for i, val in enumerate(buy_numbers):
        if open_debug:
            print "cal value =", val, "result_numbers = ", result_numbers
        if val not in result_numbers:
            return 0;
    return 3;

def cal_next_cost(total_cost, bonus_percent):

    temp_cost = (total_cost*(1+bonus_percent))/(2)
    if  temp_cost < 2:
        return 2

    temp_cost = (int(temp_cost) / 2 + 1) * 2;

    return temp_cost

def get_per_number_max_nohappeded_times(oneday_result):
    max_time_array = [0] * 11
    tmp_time_array = [0] * 11

    all_numbers = set(['01', '02','03','04','05','06','07','08','09','10','11'])
    for result in oneday_result:
        happen_number = set(result)
        nohappen_number = all_numbers - happen_number

        for element in happen_number:
            tmp_time_array[int(element) - 1] = 0
        for element in nohappen_number:
            key = int(element) - 1
            tmp_time_array[key] += 1
            if tmp_time_array[key] > max_time_array[key]:
                max_time_array[key] = tmp_time_array[key]
    return max_time_array

def get_optinum_by_latest_day(one_day_results):
    optinums_result = {}
    buy_numbers = get_any_two_number();

    for buy_number in buy_numbers:
        #print buy_number, type(buy_number)
        buy_number = list(buy_number);
        #print buy_number
        times_from_last_happen = 0;
        times_happened = 0;
        is_occur = 0
        if open_debug:
            print buy_number;
        if open_debug:
            print one_day_results

        period_times = 0
        times_nobonus_big_ten = 0
        for result_per_time in one_day_results[::-1]:
            result_per_time = set(result_per_time);
            if set(buy_number).issubset(result_per_time) != True:
                period_times = period_times + 1

                if is_occur == 0:
                    times_from_last_happen = times_from_last_happen + 1;
            else:
                is_occur = 1;
                if period_times > 9:
                    times_nobonus_big_ten = times_nobonus_big_ten + 1
                period_times = 0
                times_happened = times_happened + 1;
        save_key = buy_number[0] + ' ' +  buy_number[1]
        save_value = str(times_nobonus_big_ten) + ' '  + str(times_from_last_happen) + ' ' + str(times_happened)
        optinums_result[save_key] = save_value
    return sorted(optinums_result.items(), lambda x, y: com_optinum_args(x[1], y[1]), reverse=True)

def com_optinum_args(optinum_arg1, optinum_arg2):
    list1 = optinum_arg1.split(' ', 3)
    list2 = optinum_arg2.split(' ', 3)
    if int(list1[0]) == int(list2[0]):
        if int(list1[1]) == int(list2[1]):
            if int(list1[2]) == int(list2[2]):
                return 0;
            elif int(list1[2] > int(list2[2])):
                return 1
            else:
                return -1
            return 0
        elif int(list1[1]) > int(list2[1]):
            return 1
        else:
            return -1
    elif int(list1[0]) > int(list2[0]):
        return 1
    else:
        return -1

def get_optinum_filepath_with_result_file(result_filename_with_path):
    base_filename = os.path.basename(result_filename_with_path)
    return OptiniumPath + base_filename



def write_the_optinums_in_file(filename_with_path, optinums_result):
    file_obj = codecs.open(filename_with_path, 'w', 'utf-8')
    file_obj.write('    buy_numbers    (upTen, utilLast, happened) \n')
    for values in optinums_result:
        values = list(values)
        file_obj.write('numbers=(' + values[0] + ') option_arg=(' + values[1] + ')\n')
    file_obj.flush();
    file_obj.close()

def buy_any_two_number(one_day_result, bonus_times_in_day_array, times_biger_than_ten_array, max_no_bonus_times_array, bonus_times_array):

    buy_numbers = get_any_two_number();

    for buy_number in buy_numbers:
        period_time = 0
        total_bonus = 0;
        max_no_bonus_times = 0
        max_buy_cost = 0
        max_no_bonus_times_per_numbers = 0
        times_biger_than_ten = 0
        last_all_cost_per_time = 0;
        cost_next_time = 2;
        no_bonus_times = 0;
        max_buy_cost_per_numbers = 0
        if open_debug:
            print "-----------------------------------------------------------------------------------------------"
            print "------------------------------BUY "+str(tuple(buy_number)) + "-------------------------------------------------"
            print "-----------------------------------------------------------------------------------------------"

        bonus_times_in_day = 0;
        for result_value in analyz_data(one_day_result):
            period_time += 1
            if open_debug:
                print "result_value = ", result_value
            return_bonus = calc_bonus_with_one_period(list(buy_number), result_value);
            if return_bonus == 0 :
                last_all_cost_per_time = last_all_cost_per_time + cost_next_time;
                cost_next_time = cal_next_cost(last_all_cost_per_time, 0.2)
                if open_debug:
                    print "(",cost_next_time, ",", last_all_cost_per_time, ")," ,

                no_bonus_times = no_bonus_times + 1

                if no_bonus_times > max_no_bonus_times_per_numbers:
                    max_no_bonus_times_per_numbers = no_bonus_times
                    max_buy_cost_per_numbers = cost_next_time + last_all_cost_per_time

                if no_bonus_times > max_no_bonus_times:
                    max_no_bonus_times = no_bonus_times;
                    max_buy_cost = last_all_cost_per_time + cost_next_time

            else:
                bonus_times_in_day = bonus_times_in_day + 1
                if open_debug:
                    print "result_value = ", result_value, "buy number = ", buy_number
                bonus_per_time = cost_next_time * 2 - last_all_cost_per_time;
                total_bonus += bonus_per_time
                if open_debug:
                    #print buy_number , result_value
                    print "cost_per_time= ", last_all_cost_per_time, "cost_next_time= ", cost_next_time,
                    print "bonus_per_time= ", bonus_per_time, "period_times= ", period_time, "no_bonus_times=", no_bonus_times,
                    print "total_bonus= ", total_bonus

                if no_bonus_times > 9:
                    times_biger_than_ten = times_biger_than_ten + 1

                if bonus_times_array.has_key(no_bonus_times):
                    bonus_times_array[no_bonus_times] += 1
                else:
                    bonus_times_array[no_bonus_times] = 1

                last_all_cost_per_time = 0;
                cost_next_time = 2;
                bonus_per_time = 0;
                no_bonus_times = 0;
        #if no_bonus_times:
        #    times_biger_than_ten += times_biger_than_ten
        total_bonus = total_bonus - last_all_cost_per_time
        #print "max_no_bonus_times_per_numbers= ", max_no_bonus_times_per_numbers, "max_buy_cost_per_numbers= ", max_buy_cost_per_numbers
        #print "bonus_times_in_day= ", bonus_times_in_day, "times_biger_than_ten= ", times_biger_than_ten, "totol_bonus= ", total_bonus, "max_buy_cost= ", max_buy_cost, "max_no_bonus_times= ", max_no_bonus_times

        if bonus_times_in_day_array.has_key(bonus_times_in_day):
            bonus_times_in_day_array[bonus_times_in_day] += 1
        else:
            bonus_times_in_day_array[bonus_times_in_day] = 1

        if max_no_bonus_times_array.has_key(max_no_bonus_times):
            max_no_bonus_times_array[max_no_bonus_times] += 1
        else:
            max_no_bonus_times_array[max_no_bonus_times] = 1

        if times_biger_than_ten_array.has_key(times_biger_than_ten):
            times_biger_than_ten_array[times_biger_than_ten] += 1
        else:
            times_biger_than_ten_array[times_biger_than_ten] = 1

        if open_debug:
            print "-----------------------------------------BUY "+str(tuple(buy_number)) + "---------------------------------------------------"



def normal_sorted_fun(x, y):
    if x > y:
        return 1
    elif x < y:
        return -1
    else:
        return 0

def get_next_buy_number_by_optionium_arg(optioninum_result, hot_number, cold_number):

    total_happen_times = {}
    average_happen_numbers = {}

    for result in optioninum_result:
        args = result[1].split(' ', 3)
        key = str(args[0]) + str(args[0])
        if total_happen_times.has_key(key):
            total_happen_times[key] += int(args[2])
            average_happen_numbers[key] += 1
        else:
            total_happen_times[key] = int(args[2])
            average_happen_numbers[key] = 1

    big_number = set(["06","07","08","09","10","11"])
    little_number = set(["01","02","03","04","05"])

    odd_number = set(["01","03","05","07","09","11"])
    even_number = set(["02","04","06","08","10"])

    for result in optioninum_result:
        args = result[1].split(' ', 3)
        if int(args[0]) >= 1 and int(args[0]) < 3:
            if int(args[1]) < 10 :
                select_set = set(result[0].split(' ', 2))
                if select_set & big_number and select_set & little_number \
                    and select_set & odd_number and select_set & even_number \
                    and select_set & hot_number and len(select_set & cold_number) == 0:
                    return result[0].split(' ', 2), result[1], 10 - int(args[1])
        else:
            pass
    return None, None, None


def get_hot_number_by_oneday_result(one_day_result):

    all_numbers = set(["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"])
    hot_numbers = all_numbers
    cold_numbers = set([])

    for result in one_day_result[-4:]:
        cold_numbers = cold_numbers | set(result)
    for result in one_day_result[-3:]:
        hot_numbers = hot_numbers & set(result)
    return hot_numbers, all_numbers - cold_numbers

def try_buy_numbers_use_optionium(oneday_results):

    buy_times = 10
    periord_times = 0
    continue_buy_times = buy_times
    total_bonus = 0
    next_buy_number = []

    times_with_bonus = 0
    times_without_bonus = 0

    for oneday_result in oneday_results:
        periord_times = periord_times + 1
        if periord_times < 0:
            continue;

        if continue_buy_times >= buy_times:
            optioninum_result = get_optinum_by_latest_day(oneday_results[:periord_times-1])
            hot_numbers, cold_numbers = get_hot_number_by_oneday_result(oneday_results[:periord_times-1])

            if hot_numbers == None:
                pass
            next_buy_number, select_args, buy_times = get_next_buy_number_by_optionium_arg(optioninum_result, hot_numbers, cold_numbers)
            if next_buy_number == None:
                #print "Don't Buy ", "periord_times= ", periord_times, "optioninum_result = ", optioninum_result
                pass
            else:
                next_buy_number = set(next_buy_number)
                continue_buy_times = 0
                #print "actualy buy with number " , list(next_buy_number), "periord_times= " , periord_times, "select_args = ", select_args

        if next_buy_number != None:
            max_nohappen_times = get_per_number_max_nohappeded_times(oneday_results[:periord_times - 1 ])
            for tmp_number in next_buy_number:
                tmp_key = int(tmp_number) - 1
                tmp_buy_times = 15 - max_nohappen_times[tmp_key]
                if tmp_buy_times < 5:
                    tmp_buy_times = 5
                if continue_buy_times > tmp_buy_times:
                    continue_buy_times = buy_times
                    continue

            bonus = next_buy_number.issubset(set(oneday_result))
            if bonus:
                if 1:
                    print "Win: " , list(next_buy_number) , " continue_buy_times= ", continue_buy_times, "periord_times= " ,periord_times, "select_args = ", select_args, "buy_times = ", buy_times, 'oneday_result= ', oneday_result
                    if periord_times >= len(oneday_results):
                        tem_optioninum_result = get_optinum_by_latest_day(oneday_results)
                        tmp_hot_numbers, tmp_cold_numbers = get_hot_number_by_oneday_result(oneday_results)
                        temp_next_buy_number, temp_select_args, temp_buy_times = get_next_buy_number_by_optionium_arg(
                            tem_optioninum_result,
                            tmp_hot_numbers,
                            tmp_cold_numbers)

                        if temp_next_buy_number:
                            print "temp_next_buy_number = ", list(temp_next_buy_number), "periord_times= ", periord_times, "temp_select_args = ", temp_select_args

                times_with_bonus += 1
                total_bonus += 2 ** continue_buy_times

                continue_buy_times = buy_times;
            else:
                continue_buy_times += 1
                if periord_times >= len(oneday_results) and 1:
                    print "current_buy_number = ", list(next_buy_number), "continue_buy_times= ", continue_buy_times, "periord_times= ", periord_times, "select_args = ", select_args, "buy_times = ", buy_times, 'oneday_result= ', oneday_result
                if continue_buy_times >= buy_times:
                    times_without_bonus += 1
                    if 1:
                        print "Loss: ", list(next_buy_number), " continue_buy_times= ", continue_buy_times, "periord_times= ", periord_times, "select_args = ", select_args, "buy_times = ", buy_times, 'oneday_result= ', oneday_result

                        print hot_numbers
                        if optioninum_result and open_debug:
                            for optioninum_result_tmp in optioninum_result:
                                print "optioninum_result_tmp = ", optioninum_result_tmp
                    total_bonus -= 2 ** continue_buy_times

    print "Win " , times_with_bonus ,"   Loss "  , times_without_bonus

    return total_bonus

def analyze_all_days_result():
    path = "/Users/libo/workspace/spider/wangyi/11xuan5/"
    files = os.listdir(path)
    for file in files:
        print file
        if re.search("result.txt", file):
            print "**********************************************************************************************"
            print "**************************The day of " + file + "*************************************************"
            buy_any_two_number(path + file)
            print "**********************************************************************************************"

if __name__ == '__main__':
    #print get_any_two_number()
    path = "/Users/libo/workspace/spider/wangyi/11xuan5/result/"
    if open_debug:
        files = os.listdir(path)

        bonus_times_in_day_array = {}
        times_biger_than_ten_array = {}
        max_no_bonus_times_array = {}
        nobonus_times_array = {}
        for file in files:
            print "**********************************************************************************************"
            print "**************************The day of "+ file + "*************************************************"
            buy_any_two_number(path + file, bonus_times_in_day_array, times_biger_than_ten_array, max_no_bonus_times_array, nobonus_times_array)
            print "**************************The day of "+ file + "**********************************************"

        bonus_times_in_day_array_items = sorted(bonus_times_in_day_array.items() , lambda x, y: normal_sorted_fun(x[1], y[1]), reverse=True)
        times_biger_than_ten_array_items = sorted(times_biger_than_ten_array.items(), lambda x, y: normal_sorted_fun(x[1], y[1]), reverse=True)
        max_no_bonus_times_array_items = sorted(max_no_bonus_times_array.items(), lambda x, y: normal_sorted_fun(x[1], y[1]), reverse=True)
        nobonus_times_array_items = sorted(nobonus_times_array.items(), lambda x, y: normal_sorted_fun(x[1], y[1]), reverse=True)


        nobonus_times_datafram_index = []
        nobonus_times_data = []
        for item in nobonus_times_array_items:
            nobonus_times_datafram_index.append(item[0])
            nobonus_times_data.append(item[1])

        nobonus_times_datafram = pd.DataFrame(nobonus_times_data, index=nobonus_times_datafram_index,
                                            columns=['nobonus_times'])
        nobonus_times_datafram['nobonus_times'] = nobonus_times_datafram['nobonus_times'] / nobonus_times_datafram[
            'nobonus_times'].sum()

        print nobonus_times_datafram

        bonus_times_dataframe_index = []
        bonus_times_data = []
        for item in bonus_times_in_day_array_items:
            bonus_times_dataframe_index.append(item[0])
            bonus_times_data.append(item[1])

        bonus_times_datafram = pd.DataFrame(bonus_times_data, index=bonus_times_dataframe_index, columns=['bonus_times'])
        bonus_times_datafram['bonus_times'] = bonus_times_datafram['bonus_times'] / bonus_times_datafram['bonus_times'].sum()

        print bonus_times_datafram

        timer_biger_dataframe_index = []
        timer_biger_dataframe_data = []
        for item in times_biger_than_ten_array_items:
            timer_biger_dataframe_index.append(item[0])
            timer_biger_dataframe_data.append(item[1])

        timer_biger_datafram = pd.DataFrame(timer_biger_dataframe_data, index=timer_biger_dataframe_index,
                                            columns=['timer_biger'])
        timer_biger_datafram['timer_biger'] = timer_biger_datafram['timer_biger'] / timer_biger_datafram[
            'timer_biger'].sum()

        print timer_biger_datafram

        max_no_bonus_dataframe_index = []
        max_no_bonus_dataframe_data = []

        for item in max_no_bonus_times_array_items:
            max_no_bonus_dataframe_index.append(item[0])
            max_no_bonus_dataframe_data.append(item[1])
        max_no_bonus_times_datafram = pd.DataFrame(max_no_bonus_dataframe_data, index=max_no_bonus_dataframe_index,
                                            columns=['max_no_bonus_times'])
        max_no_bonus_times_datafram['max_no_bonus_times'] = max_no_bonus_times_datafram['max_no_bonus_times'] / max_no_bonus_times_datafram[
            'max_no_bonus_times'].sum()

        print max_no_bonus_times_datafram


    if 1:
        all_urls = UrlSet.get_all_url("http://kjh.55128.cn/", "2017-11-11", "2017-11-11")
        for url in all_urls:
            total_bonus = 0
            print url
            #save_filename_with_path = SaveUrlAsFile.get_and_save_url_as_file(url, "/home/libo/workspace/spider/wangyi/11xuan5/data/")
            save_filename_with_path = '/home/libo/workspace/spider/wangyi/11xuan5/data/js11x5-kjjg-2017-11-11.htm'
            #result_filename_with_path = ParseData.filter_one_day_data_and_save(save_filename_with_path)
            result_filename_with_path = "/home/libo/workspace/spider/wangyi/11xuan5/result/2017-11-11.txt"
            print "result_name_with_path = ", result_filename_with_path
            oneday_results = analyz_data(result_filename_with_path)
            #oneday_results.append(["01", "08", "04", "05", "11"])
            results_len = len(oneday_results)
            total_bonus = try_buy_numbers_use_optionium(oneday_results) + total_bonus
            print "oneday_results_len = ", results_len, "total_bonus = " , total_bonus

    if open_debug:
        files = os.listdir(path)
        file_number = 1
        for file in files:
            #print file
            total_bonus = 0
            oneday_results = analyz_data(path + file)
            results_len = len(oneday_results)
            total_bonus = try_buy_numbers_use_optionium(oneday_results) + total_bonus
            print "oneday_results_len = ", results_len, "total_bonus = ", total_bonus
            #file_number -= 1
            #if file_number < 0:
            #    break
    if 1:
        today_url = "http://kjh.55128.cn/js11x5-kjjg-2017-11-10.htm"
        #save_filename_with_path = SaveUrlAsFile.get_and_save_url_as_file(today_url,"/home/libo/workspace/spider/wangyi/11xuan5/data/")
        result_filename_with_path = "/home/libo/workspace/spider/wangyi/11xuan5/result/2017-11-11.txt"
        #result_filename_with_path = ParseData.filter_one_day_data_and_save(save_filename_with_path)

        oneday_results = analyz_data(result_filename_with_path)
        #oneday_results.append(["01", "03", "04", "10", "07"])
        print result_filename_with_path, len(oneday_results)
        results_len = len(oneday_results)
        optioninum_result = get_optinum_by_latest_day(oneday_results)
        hot_numbers, cold_numbers = get_hot_number_by_oneday_result(oneday_results)
        next_buy_number, select_args,buy_times = get_next_buy_number_by_optionium_arg(optioninum_result,
                                                                                       hot_numbers, cold_numbers)

        for tempresult in oneday_results[-4:]:
            print tempresult

        print "results_len = ", results_len, "hot_numbers = ", hot_numbers
        print "next_buy_number = ", next_buy_number, "select_args = ", select_args, "buy_times = ", buy_times

    #buy_any_two_number("/Users/libo/workspace/spider/wangyi/11xuan5/20171021final.txt")

    #filename = "20171028.html"
    #url_path = "http://caipiao.163.com/award/11xuan5/"
    #save_path = "/Users/libo/workspace/spider/wangyi/11xuan5/"
    #full_url = url_path + filename
    #save_filename_with_path = SaveUrlAsFile.get_and_save_url_as_file(full_url, save_path)
    #result_filename_with_path = ParseData.filter_one_day_data_and_save(save_filename_with_path)
    #result_filename_with_path = "/Users/libo/workspace/spider/wangyi/11xuan5/result/2017-10-28.txt"
    #optinum_result = get_optinum_by_latest_day(result_filename_with_path)
    #print optinum_result
    #write_the_optinums_in_file(get_optinum_filepath_with_result_file(result_filename_with_path), optinum_result)
