from lexer.Token import Token
import sys


class FileReadException(Exception):
    def __init__(self, errorInfo):
        Exception.__init__(self)
        self.errorInfo = errorInfo

    def __str__(self):
        return "文件读取出现错误,可能原因是：" + self.errorInfo


class TokenTypeError(Exception):
    def __init__(self, errorInfo):
        Exception.__init__(self)
        self.errorInfo = errorInfo

    def __str__(self):
        return "词法分类出现type异常"


class RegularExpressionError(Exception):
    def __init__(self, errorInfo):
        Exception.__init__(self)
        self.errorInfo = errorInfo

    def __str__(self):
        return "正则表达式格式错误" + self.errorInfo


class GrammarException(Exception):
    remind_exception = "语法分析出错"

    def __init__(self, keys, t):
        Exception.__init__(self)
        self.keys = keys
        self.t = t
        print(GrammarException.remind_exception)

    def __str__(self):
        if isinstance(self.t, Token):
            return "GrammarException{" + \
                "row=" + str(self.t.row) + \
                ", col=" + str(self.t.col) + \
                ", error=" + GrammarException.remind_exception + \
                ", expect=" + str(self.keys) + \
                ", get:'" + str(self.t.value) + \
                "'}"
        elif isinstance(self.t, type(1)):
            return "GrammarException{" +\
                "row=" + str(self.t) +\
                ", error=" + GrammarException.remind_exception +\
                ", expect=" + str(self.keys) +\
                ", get=null" +\
                "}"


class ParserError:

    def __init__(self, fileReader):
        self.fileReader = fileReader

    def checkGrammar(self, keys, token):
        if self.fileReader is None:
            if token is None:
                raise GrammarException(keys, 0)
            else:
                raise GrammarException(keys, token)
        else:
            codesize = len(self.fileReader.readRow)
            if token is None:
                i = max(codesize, 0)
                while i < codesize:
                    print(self.fileReader.getIndRow(i))
                    i += 1
                print("在Exception.py的" + str(sys._getframe().f_lineno))
                raise GrammarException(keys, codesize)
            else:
                codeRow = token.row
                codeCol = token.col
                if codeRow == 1:
                    sss = self.fileReader.getIndRow(0)
                    for i in range(len(sss)):
                        if i == codeCol - 1:
                            print("^",end='')
                        print(sss[i],end='')
                else:
                    print(self.fileReader.getIndRow(codeRow - 2))
                    sss = self.fileReader.getIndRow(codeRow - 1)
                    for i in range(len(sss)):
                        if i == codeCol - 1:
                            print("^" ,end='')
                        print(sss[i],end='')
                    print()
                if codeRow < codeCol:
                    print(self.fileReader.getIndRow(codeRow))
                raise GrammarException(keys, token)
