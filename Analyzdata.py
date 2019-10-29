#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

import fileinput
import datetime
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

AnalzResultNameWithPath = '/home/libo/PycharmProjects/11xuanwu/analyzdata.result'


def write_analyz_result_to_file(str, filename_with_path=AnalzResultNameWithPath):
    print str
    file_obj = codecs.open(filename_with_path, 'a', 'utf-8')
    file_obj.write(str + '\n')
    file_obj.flush();
    file_obj.close()

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

def get_per_number_max_nohappened_times(oneday_results):
    max_times_array = [0] * 11
    tmp_times_array = [0] * 11

    all_numbers = set(["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"])
    for result in oneday_results:
        happen_numbers = set(result)
        nohappen_numbers = all_numbers - happen_numbers
        for element in happen_numbers:
            tmp_times_array[int(element)-1] = 0
        for element in nohappen_numbers:
            key = int(element) - 1
            tmp_times_array[key] = tmp_times_array[key] + 1
            if tmp_times_array[key] > max_times_array[key]:
                max_times_array[key] = tmp_times_array[key]
    return max_times_array



def get_oneday_hot_normal_cold_numbers(oneday_results):

    hot_times = 4
    cold_times = 6
    tmp_nohappen_times_array = [0] * 11
    tmp_happen_times_array = [0] * 11
    all_numbers = set(["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"])
    normal_numbers = set(["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"])
    hot_numbers = set([])
    cold_numbers = set([])
    for result in oneday_results[::-1]:
        happen_numbers = set(result)
        nohappen_numbers = all_numbers - happen_numbers
        for element in happen_numbers:
            key = int(element) - 1
            tmp_nohappen_times_array[key] = 0
            tmp_happen_times_array[key] += 1
            if tmp_happen_times_array[key] > hot_times:
                if element in normal_numbers:
                    normal_numbers.remove(element)
                    hot_numbers.add(element)
        for element in nohappen_numbers:
            key = int(element) - 1
            tmp_happen_times_array[key] = 0
            tmp_nohappen_times_array[key] += 1
            if tmp_nohappen_times_array[key] > cold_times:
                if element in normal_numbers:
                    normal_numbers.remove(element)
                    cold_numbers.add(element)
    return hot_numbers, normal_numbers, cold_numbers



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

def get_numbers_happen_times(oneday_results):
    numbers_happen_times = dict.fromkeys(["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"], 0)
    for result in oneday_results:
        happen_numbers = set(result)
        for element in happen_numbers:
            numbers_happen_times[element] += 1
    return sorted(numbers_happen_times.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)

def get_number_happen_times(number, oneday_results):
    for number_happen_times in get_numbers_happen_times(oneday_results):
        if number_happen_times[0] == number:
            return number_happen_times[1]

def get_next_buy_number_by_optionium_arg(oneday_results):
    optioninum_result = get_optinum_by_latest_day(oneday_results)
    hot_numbers, cold_numbers = get_hot_number_by_oneday_result(oneday_results)
    if hot_numbers == None:
        return None, None, None
    oneday_hot_numbers, oneday_normal_numbers, oneday_cold_numbers = get_oneday_hot_normal_cold_numbers(oneday_results)


    big_numbers = set(["01", "02", "03", "04", "05"])
    little_number = set(["06", "07", "08", "09", "10", "11"])
    even_number = set(["06", "02", "08", "04", "10"])
    odd_number = set(["01", "05", "03", "07", "05", "09", "11"])

    need_print = 0
    for result in optioninum_result:
        args = result[1].split(' ', 3)
        if int(args[0]) >= 0 and int(args[0]) < 3:
            if int(args[1])< 10 :
                select_set = set(result[0].split(' ', 2))
                if (select_set & big_numbers) and (select_set & little_number) \
                    and (select_set & even_number) and (select_set & odd_number) \
                    and select_set & hot_numbers and len(select_set & cold_numbers) == 0 \
                    and len(select_set & oneday_cold_numbers) == 0:
                        print result[0].split(' ', 2), result[1], 10 - int(args[1])
                        need_print = 1
        else:
            continue

    if need_print:
        print "---------------------------"
    for result in optioninum_result:
        args = result[1].split(' ', 3)
        if int(args[0]) >= 0 and int(args[0]) < 3:
            if int(args[1])< 10 :
                select_set = set(result[0].split(' ', 2))
                min = int(result[0].split(' ', 2)[0])
                max = int(result[0].split(' ', 2)[1])

                if min > max:
                    min = max
                    max = int(result[0].split(' ', 2)[0])

                number1_happen_time = get_number_happen_times(result[0].split(' ', 2)[0], oneday_results)
                number2_happen_time = get_number_happen_times(result[0].split(' ', 2)[1], oneday_results)
                if number2_happen_time != number1_happen_time and (max % min != 0 or min == 1) \
                    and (select_set & big_numbers) and (select_set & little_number) \
                    and (select_set & even_number) and (select_set & odd_number) \
                    and select_set & hot_numbers and len(select_set & cold_numbers) == 0 \
                    and len(select_set & oneday_cold_numbers) == 0:
                        if 10 - int(args[1]) < 5:
                            return result[0].split(' ', 2), result[1], 5
                        else:
                            return result[0].split(' ', 2), result[1], 10 - int(args[1])
        else:
            pass
    return None, None, None

def get_hot_number_by_oneday_result(ond_day_result):
    all_number_set = set(["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"])
    hot_number_set = all_number_set
    cold_number_set = set([]);

    for result in ond_day_result[-4:]:
        cold_number_set = cold_number_set | set(result)

    for result in ond_day_result[-3:]:
        hot_number_set = hot_number_set & set(result)

    return hot_number_set, all_number_set - cold_number_set

# buytimes = 4




def try_buy_numbers_use_optionium(oneday_results):

    buy_times = 10
    periord_times = 0
    continue_buy_times = buy_times
    total_bonus = 0
    next_buy_number = []

    times_with_bonus = 0
    times_without_bonus = 0
    skip_times = 0

    max_continue_buy_times = 0

    for oneday_result in oneday_results:
        periord_times = periord_times + 1
        if periord_times < 0:
            continue

        if continue_buy_times >= buy_times:
            new_next_buy_number, select_args, buy_times = get_next_buy_number_by_optionium_arg(oneday_results[:periord_times-1])
            next_buy_number = new_next_buy_number
            if next_buy_number == None:
                if periord_times == len(oneday_results) and 1:
                    write_analyz_result_to_file("Don't Buy, period_times = %s"%(periord_times))
                pass
            else:
                next_buy_number = set(next_buy_number)
                continue_buy_times = 0
                skip_times = 0

        if next_buy_number != None:
            oneday_hot_numbers, oneday_normal_numbers, oneday_cold_numbers = get_oneday_hot_normal_cold_numbers(
                oneday_results[:periord_times - 1])
            if next_buy_number & oneday_cold_numbers:
                continue_buy_times = buy_times;
                continue
            max_nohappen_times = get_per_number_max_nohappened_times(oneday_results[:periord_times-1])
            for tmp_number in next_buy_number:
                xx_key = int(tmp_number) - 1
                xx_buytimes = 15 - max_nohappen_times[xx_key]
                if xx_buytimes < 5:
                    xx_buytimes = 5
                if continue_buy_times > xx_buytimes:
                    continue_buy_times = buy_times;
                    continue

            bonus = next_buy_number.issubset(set(oneday_result))
            if bonus:
                if 1:
                    max_continue_buy_times = max_continue_buy_times + continue_buy_times
                    tmp_str = "Win: %s, period_times = %s, continue_buytimes = %s, max_continue_buy_times = %s, select_args = %s, buy_times = %s"\
                                %(list(next_buy_number),periord_times, continue_buy_times, max_continue_buy_times, select_args, buy_times)
                    write_analyz_result_to_file(str=tmp_str)

                    max_continue_buy_times = 0
                    if periord_times >= len(oneday_results):
                        temp_next_buy_number, temp_select_args, temp_buy_times = \
                            get_next_buy_number_by_optionium_arg(oneday_results)
                        if temp_next_buy_number:
                            tmp_str = "next_buy_number = %s, periord_times = %s, select_args = %s"%(list(temp_next_buy_number),periord_times, temp_select_args)
                        else:
                            tmp_str = "Don't Buy. period_times = %s"%(periord_times)

                        write_analyz_result_to_file(str=tmp_str)
                times_with_bonus += 1
                total_bonus += 2 ** (continue_buy_times - skip_times)

                continue_buy_times = buy_times;
            else:
                continue_buy_times += 1
                if periord_times >= len(oneday_results)  and 1:
                    tmp_str = "current_buy_number: %s, period_times = %s, continue_buytimes = %s, skip_times = %s, select_args = %s, buy_times = %s" \
                              % (list(next_buy_number), periord_times, continue_buy_times, skip_times,
                                 select_args, buy_times)
                    write_analyz_result_to_file(str=tmp_str)
                if continue_buy_times >= buy_times:
                    times_without_bonus += 1
                    max_continue_buy_times = max_continue_buy_times + buy_times

                    tmp_str = "Loss: %s, period_times = %s, continue_buytimes = %s, skip_times = %s, select_args = %s, buy_times = %s" \
                              % (list(next_buy_number), periord_times, continue_buy_times, skip_times,
                                 select_args, buy_times)
                    write_analyz_result_to_file(str=tmp_str)
                    total_bonus -= 2 ** (continue_buy_times - skip_times)
                    continue_buy_times = buy_times
                    skip_times = 0

    #print "Win " , times_with_bonus ,"   Loss "  , times_without_bonus
    return total_bonus, times_with_bonus, times_without_bonus

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

def get_today_buy_result():
    today_url = UrlSet.get_today_url("http://kjh.55128.cn/")
    print today_url
    total_bonus = 0
    save_filename_with_path = SaveUrlAsFile.get_and_save_url_as_file(today_url,"/home/libo/workspace/spider/wangyi/11xuan5/data/")
    result_filename_with_path = ParseData.filter_one_day_data_and_save(save_filename_with_path)
    oneday_results = analyz_data(result_filename_with_path)

    tmp_total_bonus, tmp_bonus_times, tmp_nobonus_times = try_buy_numbers_use_optionium(oneday_results)

    total_bonus += tmp_total_bonus

    analyz_result_str = ("oneday_results_len = %s, total_bonus = %s, Win %s, Loss %s"%( len(oneday_results), total_bonus, tmp_bonus_times, tmp_nobonus_times))
    write_analyz_result_to_file(analyz_result_str)

    print "oneday_results_len = ", len(oneday_results), "total_bonus = ", total_bonus

    results_len = len(oneday_results)

    next_buy_number, select_args,buy_times = get_next_buy_number_by_optionium_arg(oneday_results)
    for tempresult in oneday_results[-4:]:
        print ("last_four_result = %s"%(tempresult))
    analyz_result_str = ("next_buy_number = %s, select_args = %s, buy_times = %s"
          %(next_buy_number, select_args, buy_times))
    write_analyz_result_to_file(analyz_result_str)

    print "results_len = ", results_len
    print "next_buy_number = ", next_buy_number, "select_args = ", select_args, "buy_times = ", buy_times

def get_today_buy_result_humen():
    today_url = UrlSet.get_today_url("http://kjh.55128.cn/")
    print today_url
    total_bonus = 0
    #save_filename_with_path = SaveUrlAsFile.get_and_save_url_as_file(today_url,"/home/libo/workspace/spider/wangyi/11xuan5/data/")
    #result_filename_with_path = ParseData.filter_one_day_data_and_save(save_filename_with_path)
    result_filename_with_path = "/home/libo/workspace/spider/wangyi/11xuan5/result/test.txt"
    oneday_results = analyz_data(result_filename_with_path)

    tmp_total_bonus, tmp_bonus_times, tmp_nobonus_times = try_buy_numbers_use_optionium(oneday_results)

    total_bonus += tmp_total_bonus

    analyz_result_str = ("oneday_results_len = %s, total_bonus = %s, Win %s, Loss %s"%( len(oneday_results), total_bonus, tmp_bonus_times, tmp_nobonus_times))
    write_analyz_result_to_file(analyz_result_str)

    print "oneday_results_len = ", len(oneday_results), "total_bonus = ", total_bonus

    results_len = len(oneday_results)

    next_buy_number, select_args,buy_times = get_next_buy_number_by_optionium_arg(oneday_results)
    for tempresult in oneday_results[-4:]:
        print ("last_four_result = %s"%(tempresult))
    analyz_result_str = ("next_buy_number = %s, select_args = %s, buy_times = %s"
          %(next_buy_number, select_args, buy_times))
    write_analyz_result_to_file(analyz_result_str)

    print "results_len = ", results_len
    print "next_buy_number = ", next_buy_number, "select_args = ", select_args, "buy_times = ", buy_times

if __name__ == '__main__':
    #print get_any_two_number()

    today_date = datetime.datetime.now().strftime('%Y-%m-%d')

    path = "/home/libo/workspace/spider/wangyi/11xuan5/result/"
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


    if open_debug:
        all_urls = UrlSet.get_all_url("http://kjh.55128.cn/", '2017-11-21', today_date)
        for url in all_urls:
            total_bonus = 0
            print url
            save_filename_with_path = SaveUrlAsFile.get_and_save_url_as_file(url, "/home/libo/workspace/spider/wangyi/11xuan5/data/")
            #save_filename_with_path = '/home/libo/workspace/spider/wangyi/11xuan5/data/js11x5-kjjg-2017-11-12.htm'
            result_filename_with_path = ParseData.filter_one_day_data_and_save(save_filename_with_path)
            #result_filename_with_path = "/home/libo/workspace/spider/wangyi/11xuan5/result/2017-11-17.txt"
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
            total_bonus = try_buy_numbers_use_optionium(oneday_results)
            print "oneday_results_len = ", results_len, "total_bonus = ", total_bonus
    if 1:
        get_today_buy_result()
        #get_today_buy_result_humen()
