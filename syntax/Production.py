class Production:
    def __init__(self,production):
        # 产生式的非终结符
        self.nonTerminal = set()
        # 产生式的终结符
        self.terminal = set()
        # 产生式列表
        self.productionList = []
        # 所有符号first集合
        self.firsrset = {}
        #产生式，快速获取产生式
        self.mplist = {}
        self.setProduction(production)

    def getFirstSet(self):
        return self.firsrset

    def getproductionList(self):
        return self.productionList

    # 从confi生成产生式
    def setProduction(self,production):
        for o in production:
            self.productionList.append(ProductinAtom(o["left"],o["right"]))
        self.genNonTerminalTerminal()
        self.genFirstSet()

    # 生成终结符，非终结符，map查找
    def genNonTerminalTerminal(self):
        for Atom in self.productionList:
            self.nonTerminal.add(Atom.getleft())
            for i in Atom.getright():
                self.terminal.add(i)
        self.terminal.difference_update(self.nonTerminal)

        for s in self.nonTerminal:
            pro = []
            for t in self.productionList:
                if t.getleft() == s:
                    pro.append(t)
            self.mplist[s] = pro

    # 生成first集合
    def genFirstSet(self):
        for str in self.terminal:
            self.getFirstData(str)
        for str in self.nonTerminal:
            self.getFirstData(str)

    def getLeftMplist(self,left):
        return self.mplist.get(left)

    # 对某一个符号，生成first集合
    def getFirstData(self,str):
        d = FirstSetData()
        if self.firsrset.get(str) != None:
            return self.firsrset.get(str)

        self.firsrset[str] = d
        # 是终结符
        if str in self.terminal:
            d.add(str)
            d.endToken = False
        else:
            canGetEnd = False
            for p in self.mplist.get(str):
                tmpRight = p.getright()
                if len(tmpRight) == 0:
                    canGetEnd = True
                else:
                    for tmpstr in tmpRight:
                        if tmpstr in self.terminal:
                            d.add(tmpstr)
                            break
                        else:
                            firstData = self.getFirstData(tmpstr)
                            d.add(firstData)
                            if not firstData.isEndToken():
                                break
                        if tmpstr == tmpRight[len(tmpRight)-1]:
                            canGetEnd = True
            d.endToken = canGetEnd
        return d


    # 打印
    def __str__(self):
        pass

# done
class ProductinAtom:
    def __init__(self,left=None,right =None):
        self.left = left
        self.right = right

    def getleft(self):
        return self.left

    def getright(self):
        return self.right

    def __str__(self):
        return "ProductionAtom{" +\
                "left='" + self.left + '\'' +\
                ", right=" + '['+','.join(self.right) + ']'\
                "}"

    def __eq__(self, other):
        if not isinstance(other,ProductinAtom):
            return False
        else:
            return self.left.__eq__(other.left) and self.right.__eq__(other.right)


class FirstSetData:
    def __init__(self,endToken = False):
        self.data  = set()
        self.endToken = endToken

    # str:添加的fitst集
    def add(self,str):
        if isinstance(str,FirstSetData):
            self.data = self.data.union(str.data)
        else:
            self.data.add(str)

    def getData(self):
        return self.data

    # str：移除的first集
    def remove(self):
        self.data.remove(str)

    def clear(self):
        self.data.clear()

    def isEndToken(self):
        return self.endToken

    def __str__(self):
        return "FirstSetData{" +\
                "data=[" + ','.join(self.data) +\
                "], endToken=" + str(self.endToken) +\
                '}'

    def __eq__(self, other):
        if not isinstance(other,FirstSetData):
            return False
        if self.endToken == other.endToken and self.data == other.data:
            return True
        if len(self.data) != len(other.data):
            return False
        return self.endToken == other.endToken and self.data.issuperset(other.data)
