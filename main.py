#!/bin/python
import pandas as pd  
import sys
import Delete_row
import texttoNum
import replaceNA

def output_path(chosen_outputpath):
    if chosen_outputpath == "":
        print("You have not chosen a path, the file will be saved in the current directory.")
    else:
        print(f"The file will be saved at: {chosen_outputpath}")
        return chosen_outputpath


def chosing_path(file_path):
    chosen_outputpath = input("path you want to save at:")
    output_path(chosen_outputpath)

    print("Welcome TO tachfile data\n")
    print("1.thay đổi biến")
    print("2.chuyển từ dạng text sang num")
    print("3.Xóa hàng với từng biến được chọn")

    chosen = int(input("bạn muốn được thực hiện những gì?\n"))    
    if chosen == 1:
        return replaceNA.replace_na_with_blank(sys.argv[1])
    elif chosen == 2:
        return texttoNum.convert_text_to_number(sys.argv[1])
    elif chosen == 3:
        return Delete_row.delete_rows_with_blank_columns(ays.argv[1])
    else:
        print("Unvalid task")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:  python main.py <excel_file_path>")
    else:
        chosing_path(sys.argv[1])             
