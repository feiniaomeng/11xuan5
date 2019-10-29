
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
