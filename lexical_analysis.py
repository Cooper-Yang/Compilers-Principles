# -*- coding: utf-8 -*-
'''
	读文件
	去除多余的空格、CR LF符号（不过在用readline的时候\r没有显示出来，只有\n，或许这是python的机制）
'''
import os
import sys

SCRIPT_PATH = os.getcwd()

#主函数
def main_func(input_argv = None):
	#若定义了输入文件名
	if len(input_argv) > 1:
		#获取绝对路径
		INPUT_PATH = os.path.abspath(input_argv[1])
	else:
		INPUT_PATH = os.path.abspath('./test.pas')
	#若定义了输出文件名
	if len(input_argv) > 2:
		OUTPUT_PATH = os.path.abspath(input_argv[2])
	else:
		OUTPUT_PATH = os.path.abspath('./test.dyd')
	
	#打开文件
	input_file = open(INPUT_PATH, 'r')
	output_file = open(OUTPUT_PATH, 'w')
	#按行处理
	for line in input_file:
		lexical_analysis(line)
	#关闭文件
	input_file.close()
	output_file.close()
	
	print sys.argv
	print '\n finished \n'
	return

#进行词法分析
def lexical_analysis(input_line = None):
	pass

if __name__ == "__main__":
	#调用主函数
	main_func(sys.argv)