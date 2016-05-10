#Experiment of Compilers Principles

##Lexical_analysis.py : 词法分析

input: 	*.pas

output:	*.dyd

###Usage:

	Lexical_analysis.py <input_file> <output_file>
	
	if input_file not specify, will use test.pas in current directory
	if output_file note specify, will write to test.dyd in current directory
	
--------------

##Syntactic_analysis.py : 语法分析

input: 	*.dyd

output:	*.dys *.var(变量名表) *.pro(过程名表) *.err(出错)

###Usage:

	Usage
	
--------------

##test.pas : 作为输入的待分析文件

该文件中没有任何注释
