#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pro5_interpreter.Interpreter import Interpreter

what_to_execute = {
    "instructions": [("LOAD_VALUE", 0),  # 第一个数
                     ("LOAD_VALUE", 1),  # 第二个数
                     ("ADD_TWO_VALUES", None),
                     ("PRINT_ANSWER", None)],
    "numbers": [7, 5]}

what_to_execute2 = {
    "instructions": [("LOAD_VALUE", 0),
                     ("LOAD_VALUE", 1),
                     ("ADD_TWO_VALUES", None),
                     ("LOAD_VALUE", 2),
                     ("ADD_TWO_VALUES", None),
                     ("PRINT_ANSWER", None)],
    "numbers": [7, 5, 8]}


# 源代码
# def s():
#     a = 1
#     b = 2
#     print(a + b)
# 编译后的字节码
what_to_execute_s = {
    "instructions": [("LOAD_VALUE", 0),
                     ("STORE_NAME", 0),
                     ("LOAD_VALUE", 1),
                     ("STORE_NAME", 1),
                     ("LOAD_NAME", 0),
                     ("LOAD_NAME", 1),
                     ("ADD_TWO_VALUES", None),
                     ("PRINT_ANSWER", None)],
    "numbers": [1, 2],
    "names": ["a", "b"]}

if __name__ == '__main__':
    interpreter = Interpreter()
    interpreter.run_code(what_to_execute)
    interpreter.run_code(what_to_execute2)
    interpreter.run_code(what_to_execute_s)
    interpreter.execute(what_to_execute_s)
