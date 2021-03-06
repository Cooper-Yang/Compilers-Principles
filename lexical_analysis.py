# -*- coding: utf-8 -*-
'''
	读文件
	去除多余的空格、CR LF符号（不过在用read方法的时候\r没有显示出来，只有\n，或许这是python的机制）
'''
import os
import sys

SCRIPT_PATH = os.getcwd()

#这张表中的内容的顺序是按照实验要求设置的,其中第10个是标识符，第11个是常数，第0个只在这里起填充作用
WORD_TABLE = [' ', 'begin', 'end', 'integer', 'if', 'then', 'else', 'function', 'read', 'write', '', '', '=', '<>', '<=', '<', '>=', '>', '-', '*', ':=', '(', ')', ';']

class CurrentWord(object):
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
	def reset(self):
		'''
		重置自身所有属性
		'''
		self.word = ''
		self.lastletter = self.word[-1:]
		self.type = 0
		self.division = 0
	#获取所属类别
	def get_type(self):
		'''
		获取当前词组的属性，是能接受字母和数字、只能接收数字、只能再接收一个字符、还是不能再接收字符
		'''
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
		#否则为6，即不接受任何新字符输入
		else:
			self.type = 6
		return self.type
	def get_division(self):
		'''
		获取当前单词所属的种别，返回在WORD_TABLE中的相应序号
		'''
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
	def format_out(self):
		'''
		输出
		'''
		out = self.word.rjust(16)+' '+str(self.get_division()).rjust(2)+'\n'
		return out

def main_func(input_argv=None):
	'''
	主函数
	'''
	#若定义了输入文件名
	if len(input_argv) > 1:
		#获取绝对路径
		input_path = os.path.abspath(input_argv[1])
	else:
		input_path = os.path.abspath('./test.pas')
	#若定义了输出文件名
	if len(input_argv) > 2:
		output_path = os.path.abspath(input_argv[2])
	else:
		output_path = os.path.abspath('./test.dyd')
	#打开文件
	input_file = open(input_path, 'r')
	output_file = open(output_path, 'w')
	error_path = os.path.abspath('./test.err')
	err_file = open(error_path, 'w')

	#进行处理，并将处理结果写入文件
	input_str = input_file.read()
	output_str = lexical_analysis(input_str)
	output_file.writelines(output_str)

	#关闭文件
	input_file.close()
	output_file.close()
	err_file.close()

	#print sys.argv
	print '\n finished \n'
	return

#进行词法分析
def lexical_analysis(input_line=None):
	'''
	output_line是最终返回的list
	对于输入的input_line，一个字符一个字符进行处理
	'''
	output_line = []
	current_input_word = CurrentWord()
	for input_letter in input_line:
		#若到行末尾，将current_input_word重置，并在输出添加一个行结尾
		#如果current_input_word不为空，将其内容输出
		if input_letter == '\n':
			if current_input_word.word != '':
				output_line.append(current_input_word.format_out())
			current_input_word.reset()
			output_line.append(str('EOLN').rjust(16)+' '+'24'+'\n')
			continue
		else:
			#若current_input_word为空，移进
			if current_input_word.type == 0:
				current_input_word.reset()
				current_input_word.word = current_input_word.word + input_letter
				current_input_word.type = current_input_word.get_type()
			#处理字符+数字
			elif current_input_word.type == 1:
				if input_letter.isalnum() is True:
					current_input_word.word = current_input_word.word + input_letter
				else:
					output_line.append(current_input_word.format_out())
					current_input_word.reset()
					current_input_word.word = current_input_word.word + input_letter
					current_input_word.type = current_input_word.get_type()
			#处理数字
			elif current_input_word.type == 2:
				if input_letter.isdigit() is True:
					current_input_word.word = current_input_word.word + input_letter
				else:
					output_line.append(current_input_word.format_out())
					current_input_word.reset()
					current_input_word.word = current_input_word.word + input_letter
					current_input_word.type = current_input_word.get_type()
			#处理运算符，若输入符合，先移进再输出，否则先输出再移进
			elif current_input_word.type == 3:
				if input_letter == '=' or input_letter == '>':
					current_input_word.word = current_input_word.word + input_letter
					output_line.append(current_input_word.format_out())
					current_input_word.reset()
				else:
					output_line.append(current_input_word.format_out())
					current_input_word.reset()
					current_input_word.word = current_input_word.word + input_letter
					current_input_word.type = current_input_word.get_type()
			elif current_input_word.type == 4:
				if input_letter == '=':
					current_input_word.word = current_input_word.word + input_letter
					output_line.append(current_input_word.format_out())
					current_input_word.reset()
				else:
					output_line.append(current_input_word.format_out())
					current_input_word.reset()
					current_input_word.word = current_input_word.word + input_letter
					current_input_word.type = current_input_word.get_type()
			elif current_input_word.type == 5:
				if input_letter == '=':
					current_input_word.word = current_input_word.word + input_letter
					output_line.append(current_input_word.format_out())
					current_input_word.reset()
				else:
					output_line.append(current_input_word.format_out())
					current_input_word.reset()
					current_input_word.word = current_input_word.word + input_letter
					current_input_word.type = current_input_word.get_type()
			#如果以上情况都不符合，则认为该输入属于只有一个字符的类型
			elif current_input_word.type == 6:
				output_line.append(current_input_word.format_out())
				current_input_word.reset()
				current_input_word.word = current_input_word.word + input_letter
				current_input_word.type = current_input_word.get_type()
	#到达文件结尾，若current_input_word不为空，则输出，否则输出文件结尾符号
	if current_input_word.type != 0:
		output_line.append(current_input_word.format_out())
	output_line.append(str('EOF').rjust(16)+' '+'25')
	return output_line

if __name__ == "__main__":
	#调用主函数
	main_func(sys.argv)
