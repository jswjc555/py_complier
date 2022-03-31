import input.syntax_config
from syntax.SyncTable import *
from lexer import lex_analyzer
from utils.FileReader import FileReader
from utils.Exception import *

class AnalysisList:
    def __init__(self):
        self.production = Production(input.syntax_config.production)
        self.synctable = SyncTable(self.production)
        self.filereader = None

    # 传入lexer的lex_analyzer对象，包含token列表
    # return:分析成功与否
    def analyse(self,lex_analyzer):
        try:
            self.filereader = FileReader(lex_analyzer.filepath)
        except Exception as e:
            print(e)
            raise FileReadException("语法analyse时读文件出错")
        yes_or_no = self.synctable.syncTokenList(lex_analyzer, ParserError(self.filereader))
        return yes_or_no



    # 打印根据语法生成的项目集族 DFA
    def printItemSetList(self):
        print(self.synctable.getItemSetList())

    # 打印生成的action goto表
    def printActionGotoTable(self):
        print(self.synctable.getAgList())

    # 打印分析栈
    def printAnalysisTable(self):
        for i in self.synctable.getAnalysisTable():
            print(i)
