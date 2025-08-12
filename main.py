#!/bin/python
import pandas as pd  
import sys
import Delete_row
import texttoNum
import replaceNA

def chosing_path(file_path):
    print("Welcome TO tachfile data\n")
    print("1.thay đổi biến")
    print("2.chuyển từ dạng text sang num")
    print("3.Xóa hàng với từng biến được chọn")

    chosen = int(input("bạn muốn được thực hiện những gì?\n"))    
    if chosen == 1:
        return replaceNA
    elif chosen == 2:
        return texttoNum
    elif chosen == 3:
        return Delete_row
    else:
        print("Unvalid task")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <file_path> <output_directory>")
    else:
        chosing_path(sys.argv[1])             
