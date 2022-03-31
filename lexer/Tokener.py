from lexer import JudgeType, Token
from input import lexer_config
from lexer.JudgeType import JudgeType
from lexer.re2nfa import *
from utils.FileReader import FileReader
from lexer.Token import Token
from utils.Exception import TokenTypeError
import sys


class Tokener(object):
    def __init__(self, filepath):
        self.jp = JudgeType()
        self.codeRow = FileReader(filepath)
        self.tokens = []
        self.genTokens()
        self.cheekToken()

    def getTokens(self):
        return self.tokens

    # 生成tokens*****
    def genTokens(self):
        code = ""
        isNoteState = False
        while self.codeRow.check_outofIndex() != None:
            code = self.codeRow.currentRow()
            # print(code)
            word = ""
            at = 0
            while at < len(code):
                while self.is_Blank(code[at]) and at < len(code):
                    at += 1
                if at < len(code):
                    c = code[at]
                # 注释处理
                if isNoteState == False and at < len(code) - 1 and c == '/' and code[at + 1] == '*':
                    # print("at = " + str(at) + "c ==" + c + "code[at+1]=" + code[at + 1] + "len(code)-1=" + str(len(
                    # code) - 1) + "code=" + code+"word="+word)
                    isNoteState = True
                    at += 1
                    if len(word) != 0:
                        self.tokens.append(Token(self.codeRow.getrowIndex(), at, self.jp.getTokenType(word), word))
                        print("token_append" + str(sys._getframe().f_lineno))
                        word = ""
                    break
                if isNoteState:
                    if at < len(code) - 1 and c == "*" and code[at + 1] == '/':
                        isNoteState = False
                        break
                    else:
                        at += 1
                        continue
                if at < len(code) and c == '/' and code[at + 1] == '/':
                    if len(word) != 0:
                        self.tokens.append(Token(self.codeRow.getrowIndex(), at, self.jp.getTokenType(word), word))
                        # print("token_append"+str(sys._getframe().f_lineno))
                    break
                flag = True
                tmplist = [self.jp.getConstant(), self.jp.getID()]
                for tmpp in tmplist:
                    strstart, strend = self.patternLastIndex(tmpp, code[at:])
                    # print("at= "+str(at)+"  strend= "+str(strend)+"  code[i:]= "+code[at:])
                    if strend != 0:
                        flag = False
                        tmpstr = code[at:at + strend]
                        # print(code[strstart:strend]+"    "+str(i))
                        self.tokens.append(
                            Token(self.codeRow.getrowIndex(), at + 1, self.jp.getTokenType(tmpstr), tmpstr))
                        # print("token_append" + str(sys._getframe().f_lineno)+tmpstr)
                        at = at + strend - 1
                        if len(word) != 0:
                            self.tokens.append(
                                Token(self.codeRow.getrowIndex(), at + 1, self.jp.getTokenType(word), word))
                            # print("token_append" + str(sys._getframe().f_lineno))
                            word = ""
                        break
                if flag:
                    word = word + c
                    if at < len(code) - 1 and word + code[at + 1] in self.jp.getOperator():
                        self.tokens.append(
                            Token(self.codeRow.getrowIndex(), at + 1, self.jp.getTokenType(word + code[at + 1]),
                                  word + code[at + 1]))
                        # print("token_append" + str(sys._getframe().f_lineno))
                        at += 1
                    else:
                        self.tokens.append(Token(self.codeRow.getrowIndex(), at + 1, self.jp.getTokenType(word), word))
                        # print("token_append" + str(sys._getframe().f_lineno))
                    word = ""
                at = at + 1

    # 匹配得到的结果
    # str:待识别的字符串
    # pattern:正则表达式
    # return: 识别的位置
    def patternLastIndex(self, pattern, str):
        match = pattern.match(str)
        if match != (0, 0):
            return match[0], match[1]
        else:
            return 0, 0

    # 判断c是否是空字符
    def is_Blank(self, c):
        if c == ' ' or c == '\t' or c == '\n':
            return True
        else:
            return False

    def cheekToken(self):
        for t in self.tokens:
            if t.type == "ErrorType":
                print(t)
                raise TokenTypeError("cheekToken出错")
