from lexer.Tokener import Tokener


class lex_analyzer(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self.tokener = Tokener(filepath)

    def getTokens(self):
        return self.tokener.getTokens()

    def getFileName(self):
        return self.filepath

    # 打印输出token列表√
    def selfprint(self):
        for t in self.tokener.getTokens():
            print(t)

