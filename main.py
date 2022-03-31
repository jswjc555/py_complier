from lexer.lex_analyzer import lex_analyzer
from syntax.AnalysisList import AnalysisList
import os



# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    try:
        projectlocation = os.getcwd()
        filepath = projectlocation + "/input/test.txt"
        # 词法分析
        lexer = lex_analyzer(filepath)
        # 打印token表
        lexer.selfprint()

        # 语法分析 check
        analysisList = AnalysisList()
        # 打印项目集族 check
        analysisList.printItemSetList()
        # 打印goto表 check
        analysisList.printActionGotoTable()
        # 是否分析成功，不成功会报错 自动终止，并且输出出错原因
        analyseOK = analysisList.analyse(lexer)
        # 打印分析栈
        analysisList.printAnalysisTable()

    except BaseException as e:
        print(e)