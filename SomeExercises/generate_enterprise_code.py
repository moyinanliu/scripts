# encoding: utf-8

"""Generate Enterprise COde"""

from view import menu

import os
import random
import tkinter.messagebox


six_number_code_save = "./SixCode.txt"
nine_number_code_save = "./NineCode.txt"
twenty_five_code_save = "./TwentyFiveCode.txt"


def check_file_exist(path):
    """
    判断传入的文件路径是否存在，不存在就创建
    :param path: 文件路径
    :return:
    """
    if not os.path.isfile(path):
        f = open(path, "w", encoding="utf-8")
        f.close()


def go_on():
    """
    功能结束时
    :return:
    """
    while True:
        goon = input("")
        if goon == "":
            return select_function()
        else:
            continue


def generate_sum():
    """
    生成数量
    :return:
    """
    generate_code_sum = 0

    while True:
        num = input("输入要生成的数量：\t")
        if num.isdigit():
            if int(num) > 0:
                generate_code_sum = int(num)
                break
            else:
                print("请输入正整数")
                continue
        else:
            print("请输入正整数")
            continue

    return generate_code_sum


def tip(path, title="提示", message="文件保存在:"):
    """
    消息框提示
    :param title:
    :param message:
    :param path: 文件的绝对路径
    :return:
    """
    message += path
    tkinter.messagebox.showinfo(title=title, message=message)


def generate_six_number_code():
    """
    生成六位数字的防伪编码
    :return:
    """
    generate_code_sum = generate_sum()
    for y in range(0, generate_code_sum):
        generate_result = ""
        for x in range(0, 6):
            generate_result += str(random.choice(range(0, 10)))
        print(generate_result)
        generate_result += "\n"
        with open(six_number_code_save, "a", encoding="utf-8") as f:
            f.write(generate_result)
    tip(os.path.abspath(six_number_code_save))

    return go_on()


def generate_series_code():
    """
    生成九位数字系列产品的防伪编码(778-123124型)
    :return:
    """
    # 系列号
    series_num = ""
    while True:
        series = input("请输入产品系列号,三位数：\t")
        if series.isdigit():
            if len(series) == 3:
                series_num = series
                break
            else:
                print("位数不对，重新输入")
                continue
        else:
            print("请正确输入，eg:213, 882")
            continue

    # 数量
    generate_code_sum = generate_sum()

    for y in range(0, generate_code_sum):
        # 六位随机数
        generate_result = ""
        for x in range(0, 6):
            generate_result += str(random.choice(range(0, 10)))
        print("%s-%s" % (series_num, generate_result))
        # 与系列号拼接
        generate_result = "%s-%s\n" % (series_num, generate_result)
        with open(nine_number_code_save, "a", encoding="utf-8") as f:
            f.write(generate_result)
    tip(os.path.abspath(nine_number_code_save))

    return go_on()


def generate_twenty_five_code():
    """
    生成25位混合码
    :return:
    """
    generate_code_sum = generate_sum()

    return go_on()


def select_function():
    """
    功能选择
    :return:
    """
    print(menu)
    function_number = 0
    while True:
        function_select = input("请选择功能：\t")
        if function_select.isdigit():
            if 0 <= int(function_select) < 10:
                function_number = int(function_select)
                break
            else:
                print("请重新输入，数字0-9")
                continue
        else:
            print("请重新输入，数字0-9")
            continue
    return function_number


def main():
    check_file_exist(six_number_code_save)
    check_file_exist(nine_number_code_save)
    function_number = select_function()
    while True:
        if function_number == 0:
            exit("退出系统")
        elif function_number == 1:
            function_number = generate_six_number_code()
        elif function_number == 2:
            function_number = generate_series_code()
        elif function_number == 3:
            function_number = generate_twenty_five_code()
        elif function_number == 4:
            print(4)
        elif function_number == 5:
            print(5)
        elif function_number == 6:
            print(6)
        elif function_number == 7:
            print(7)
        elif function_number == 8:
            print(8)
        elif function_number == 9:
            print(9)


if __name__ == '__main__':
    main()
