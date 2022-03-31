from utils.Exception import FileReadException


class FileReader(object):
    def __init__(self, filename):
        self.filename = filename
        self.readRow = []  # 读出来的文件内容
        self.rowIndex = 0  # 应该读的行数索引
        self.readFile2Row()

    def getrowIndex(self):
        return self.rowIndex

    def getIndRow(self,ind):
        try:
            return self.readRow[ind]
        except Exception as e:
            print(e)

    # 让self.readrow里面按照行读入代码windows-1252
    def readFile2Row(self):
        try:
            #print(1)
            reader = open(self.filename, encoding="utf-8")
            #print(2)
            codes = reader.readlines()
            #print(3)
            for line in codes:
                line = line.replace('\n', '')
                # if len(line)!= 0:
                self.readRow.append(line)
            # print(self.readRow)
        except Exception as e:
            print(e)
            raise FileReadException("readFile2Row出错啦")
        finally:
            reader.close()

    # 返回第ind行的代码
    def getRowbyIndex(self, ind):
        try:
            return self.readRow[ind]
        except Exception as e:
            return None

    # 读一行，self.rowIndex++
    def check_outofIndex(self):
        try:
            test = self.readRow[self.rowIndex]
            return True
        except:
            return None

    def currentRow(self):
        try:
            re = self.readRow[self.rowIndex]
            self.rowIndex = self.rowIndex + 1
            return re
        except Exception as e:
            return None
