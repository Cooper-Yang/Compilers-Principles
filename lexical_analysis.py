# -*- coding: utf-8 -*-
'''
	读文件
	去除多余的空格、CR LF符号（不过在用read方法的时候\r没有显示出来，只有\n，或许这是python的机制）
'''
import os
import sys

SCRIPT_PATH = os.getcwd()

#这张表中的内容的顺序是按照实验要求设置的,其中第10个是标识符，第11个是常数，第0个只在这里起填充作用
WORD_TABLE = [' ','begin','end','integer','if','then','else','function','read','write','','','=','<>','<=','<','>=','>','-','*',':=','(',')',';']

class CURRENT_WORD:
	'''
	当前正在处理的单词
	属性包括单词内容、最后一个字符、所属类别（字符串、数字、运算符），所属种别（begin、end、else等等）
	方法包括重置所有属性、获取最后一个字符、判断所属种别、按格式输出
	'''
	#初始化
	def __init__(self):
		self.word = ''
		self.lastletter = self.word[-1:]
		self.type = 0
		self.division = 0
	#重置
	def reset(self):
		self.word = ''
		self.lastletter = self.word[-1:]
		self.type = 0
		self.division = 0
	#获取所属类别
	def GetType(self):
		#若为空或只有空格，则为0
		if len(self.word) == 0 or self.word.isspace() is True:
			self.type = 0
		#若以字母开头且只有数字和字母，则为1
		elif self.word.isalnum() is True and self.word[0].isalpha() is True:
			self.type = 1
		#若只有数字，则为2
		elif self.word.isdigit() is True:
			self.type = 2
		#以下的<、>、:的特征都是它们还能接受一个字符输入
		elif self.word == '<':
			self.type = 3
		elif self.word == '>':
			self.type = 4
		elif self.word == ':':
			self.type = 5
		#否则为6
		else:
			self.type = 6
		return self.type
	#获取所属种别
	def GetDivision(self):
		try:
			temp = WORD_TABLE.index(self.word)
			return temp
		except ValueError:
			if self.type == 1:
					return 10
			elif self.type == 2:
					return 11
			else:
					return 0
	#输出
	def FormatOut(self):
		out = self.word.rjust(16)+' '+str(self.GetDivision()).rjust(2)+'\n'
		return out

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
	
	#进行处理，并将处理结果写入文件
	input_str = input_file.read()
	output_str = lexical_analysis(input_str)
	output_file.writelines(output_str)
	
	#关闭文件
	input_file.close()
	output_file.close()
	
	#print sys.argv
	print '\n finished \n'
	return

#进行词法分析
def lexical_analysis(input_line = None):
	'''
	output_line是最终返回的list
	对于输入的input_line，一个字符一个字符进行处理
	'''
	output_line = []
	middle_place = CURRENT_WORD()
	for input_letter in input_line:
		#若到行末尾，将middle_place重置，并在输出添加一个行结尾
		#如果middle_place不为空，将其内容输出
		if input_letter == '\n':
			if middle_place != 0:
				output_line.append(middle_place.FormatOut())
			middle_place.reset()
			output_line.append(str('EOLN').rjust(16)+' '+'24'+'\n')
			continue
		else:
			#若middle_place为空，移进
			if middle_place.type == 0:
				middle_place.reset()
				middle_place.word = middle_place.word + input_letter
				middle_place.type = middle_place.GetType()
			#处理字符+数字
			elif middle_place.type == 1:
				if input_letter.isalnum() is True:
					middle_place.word = middle_place.word + input_letter
				else:
					output_line.append(middle_place.FormatOut())
					middle_place.reset()
					middle_place.word = middle_place.word + input_letter
					middle_place.type = middle_place.GetType()
			#处理数字
			elif middle_place.type == 2:
				if input_letter.isdigit() is True:
					middle_place.word = middle_place.word + input_letter
				else:
					output_line.append(middle_place.FormatOut())
					middle_place.reset()
					middle_place.word = middle_place.word + input_letter
					middle_place.type = middle_place.GetType()
			#处理运算符，若输入符合，先移进再输出，否则先输出再移进
			elif middle_place.type == 3:
				if input_letter == '=' or input_letter == '>':
					middle_place.word = middle_place.word + input_letter
					output_line.append(middle_place.FormatOut())
					middle_place.reset()
				else:
					output_line.append(middle_place.FormatOut())
					middle_place.reset()
					middle_place.word = middle_place.word + input_letter
					middle_place.type = middle_place.GetType()
			elif middle_place.type == 4:
				if input_letter == '=':
					middle_place.word = middle_place.word + input_letter
					output_line.append(middle_place.FormatOut())
					middle_place.reset()
				else:
					output_line.append(middle_place.FormatOut())
					middle_place.reset()
					middle_place.word = middle_place.word + input_letter
					middle_place.type = middle_place.GetType()
			elif middle_place.type == 5:
				if input_letter == '=':
					middle_place.word = middle_place.word + input_letter
					output_line.append(middle_place.FormatOut())
					middle_place.reset()
				else:
					output_line.append(middle_place.FormatOut())
					middle_place.reset()
					middle_place.word = middle_place.word + input_letter
					middle_place.type = middle_place.GetType()
			#如果以上情况都不符合，则认为该输入属于只有一个字符的类型
			elif middle_place.type == 6:
				output_line.append(middle_place.FormatOut())
				middle_place.reset()
				middle_place.word = middle_place.word + input_letter
				middle_place.type = middle_place.GetType()
	#到达文件结尾，若middle_place不为空，则输出，否则输出文件结尾符号
	if middle_place.type != 0:
		output_line.append(middle_place.FormatOut())
	output_line.append(str('EOF').rjust(16)+' '+'25')
	return output_line

if __name__ == "__main__":
	#调用主函数
	main_func(sys.argv)