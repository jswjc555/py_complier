from input import lexer_config
import re
from lexer.re2nfa import *


class JudgeType(object):  # 设置判断准则并对输入字符串判断匹配返回类别
    def __init__(self):
        self.Key_word = lexer_config.Key_word
        # self.Constant = re.compile(config.Constant)
        # self.ID = re.compile(config.ID)
        self.Constant = Nfa_Maker(pre2suffix(lexer_config.constant).suffix)
        self.ID = Nfa_Maker(pre2suffix(lexer_config.id).suffix)
        self.Symble = lexer_config.Symble
        self.Operator = lexer_config.Operator
        pass  # 初始化不同类别
        # Key_word的判断准则
        # Operator的判断准则
        # Symble的判断准则
        # ID的判断准则  （nfa）
        # Constant的判断准则（nfa）

    def getConstant(self):
        return self.Constant

    def getID(self):
        return self.ID

    def getOperator(self):
        return self.Operator

    # 输入分割的词，判断并返回Token
    def getTokenType(self, str):

        if (str in self.Key_word):
            return "Key_word"
        elif (str in self.Operator):
            return "Operator"
        elif (str in self.Symble):
            return "Symble"
        # elif(self.ID.match(str)!=None):
        #     return "ID"
        # elif(self.Constant.match(str)!=None):
        #     return "Constant"
        elif self.ID.match(str) != (0, 0):
            return "ID"
        elif self.Constant.match(str) != (0, 0):
            return "Constant"

        return "ErrorType"

    # 自定义打印
    def selfprint(self):
        print("JudgeType{"
              "Key_word=" + self.Key_word +
              ",Operator=" + self.Operator +
              ",Constant=" + self.Constant +
              ",ID=" + self.ID +
              ",Symble" + self.Symble
              )
