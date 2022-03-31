from nose.tools import *
from lexer.Token import Token
from lexer.lex_analyzer import lex_analyzer
from lexer.re2nfa import *
from input import lexer_config
from syntax.AnalysisList import AnalysisList
import os
import re

'''
测试文件运行方法：在项目总目录下命令行运行
nosetests   (-s -v) -s：打印函数运行中的print，-v：现实测试函数名称
或者
python -m ‘nose’ (-s -v)
即可
'''


def readfile_test():
    filepath = os.getcwd() + "\\input\\test.txt"
    reader = open(filepath, encoding='windows-1252')
    # codes = reader.readlines()
    # for line in codes:
    #     print(line)
    assert_equal(1, 1)


def re_test():
    pass
    # id_re = re.compile(config.ID)
    # constant_re = re.compile(config.Constant)
    # print(id_re.match("asdf"))
    # res = constant_re.match("truefff")
    # # if(res != None):
    # #     print(res)
    # #     print(res.start())
    # #     print(res.string[res.start():res.end()])
    #
    # print(constant_re.match("falsefff"))
    # print(constant_re.match("12"))
    # print(constant_re.match("0.314E+1"))
    # print(constant_re.match("12.34E+1.2"))
    # print(constant_re.match("12.34E"))
    # print(constant_re.match("10.23+12.43i"))


def test():
    projectlocation = os.getcwd()
    filepath = projectlocation + "/input/test.txt"
    test_filepath ="S:\py\python_compiler/input/test.txt"
    # 词法分析
    lexer = lex_analyzer(test_filepath)
    # 打印token表
    lexer.selfprint()

    # 语法分析 check
    analysisList = AnalysisList()
    # # 打印项目集族 check
    # analysisList.printItemSetList()
    # # 打印goto表 check
    # analysisList.printActionGotoTable()
    # 是否分析成功，不成功会报错 自动终止，并且输出出错原因
    analyseOK = analysisList.analyse(lexer)
    # 打印分析栈
    analysisList.printAnalysisTable()

def re2nfa_test():
    pass
    # a = pre2suffix(config.constant)
    # c = pre2suffix(config.id)
    # t = Nfa_Maker(c.suffix)
    # tt = Nfa_Maker(a.suffix)
    # print(tt.match("function int test(int a,double b){"))
    # print((t.match("function int test(int a,double b){")))


