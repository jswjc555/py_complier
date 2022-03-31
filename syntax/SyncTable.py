from syntax.SynctreeNode import SyncTreeNode
from syntax.Production import *


class ActionGoto:
    def __init__(self, id):
        self.id = id
        self.op = {}

    def getId(self):
        return self.id

    # key：传入符号，return 动作
    def get(self, key):
        return self.op.get(key)

    # return :期望符号
    def getKeys(self):
        return set(self.op.keys())

    # key传入符号，a：动作
    def put(self, key, a):
        if isinstance(a, type(1)) or isinstance(a, ProductinAtom):
            self.op[key] = a

    def putKeys(self, keys, a):
        if isinstance(a, type(1)) or isinstance(a, ProductinAtom):
            for k in keys:
                self.op[k] = a

    def putAll(self, shiftItem):
        for i in shiftItem:
            self.op[i] = shiftItem[i]

    def replace(self, key, a):
        if isinstance(a, type(1) or isinstance(a, ProductinAtom)):
            self.op[key] = a

    def __str__(self):
        sss = "ActionGoto{" + \
              "id=" + str(self.id) + \
              ", op={"
        for i in self.op:
            sss = sss + " " + str(i) + ":" + str(self.op[i]) + " "
        sss += "}"
        return sss


class Item:
    def __init__(self, p, index=0, forward=None):
        self.index = index
        self.p = p
        self.forward = forward

    def __str__(self):
        return "Item{" + \
               "index=" + str(self.index) + \
               ", p=" + str(self.p) + \
               ", forward=" + str(self.forward) + \
               "}\n"

    def __eq__(self, other):
        if not isinstance(other, Item):
            return False
        if self.index != other.index:
            return False
        isEqual = (self.p == other.p or self.p.__eq__(other.p))
        if self.forward == other.forward:
            return isEqual
        if self.forward != None and other.forward != None:
            return isEqual and self.forward.__eq__(other.forward)
        else:
            return False


class ItemSet:
    itemSetCnt = 0

    def __init__(self):
        # print("-------------"+str(ItemSet.itemSetCnt))
        self.id = ItemSet.itemSetCnt
        ItemSet.itemSetCnt += 1
        self.shiftItem = {}
        self.itemList = []

    def add(self, i):
        self.itemList.append(i)

    def __str__(self):
        ss = "ItemSet{" + \
             "id=" + str(self.id) + \
             ", shiftItem=" + str(self.shiftItem) + \
             ", itemList="
        for i in self.itemList:
            ss += str(i)
        ss += "]}"
        return ss

    def __eq__(self, other):
        if not isinstance(other, ItemSet):
            return False
        if self.itemList == other.itemList:
            return True
        if len(self.itemList) != len(other.itemList):
            return False
        return self.itemList == other.itemList


class SyncTable:
    def __init__(self, production, start_of_grammar="START"):
        self.start_of_grammar = start_of_grammar
        self.production = production
        self.itemSetList = []
        self.agList = []
        self.analysisTable = []
        self.syncTreeNode = SyncTreeNode()
        self.genItemSetList()
        self.genActionGotoList()

    # return 项目集族 string
    def getItemSetList(self):
        str = ""
        for i in self.itemSetList:
            str += i.__str__() + "\n"
        return str

    # return action goto 表 string
    def getAgList(self):
        sss = ""
        for a in self.agList:
            sss += str(a)
            sss += '\n'
        return sss

    def getAnalysisTable(self):
        return self.analysisTable

    # lexer输入，返回是否符合语法 期间打印输出分析栈
    def syncTokenList(self, lexer, parserError):
        # 状态栈
        state = []
        # 符号栈
        symble = []
        # 语法树
        synTreeNodes = []
        # 输入符号
        tokens = lexer.getTokens()
        # 状态栈初始化
        state.append(0)
        tokenInd = 0
        while 0 <= tokenInd < len(tokens):
            t = tokens[tokenInd]
            if len(state) == 0:
                parserError.checkGrammar(None, t)  ########
                return False
            index = state[-1]
            actionGoto = self.agList[index]
            val = ""
            if t.type == "ID":
                val = "ID"
            elif t.type == "Constant":
                val = "CONSTANT"
            else:
                val = t.value
            self.addStateAndSymbol(state, symble, val)
            # 根据actionGoto表，要么移进，要么规约
            o = actionGoto.get(val)
            if o is None:
                # actiongoto表没有的话，看能否规约
                o = actionGoto.get(None)
            if isinstance(o, type(1)):
                # 移进
                state.append(o)
                symble.append(val)
                synTreeNodes.append(SyncTreeNode(val, t))
            elif isinstance(o, ProductinAtom):
                # 规约
                self.reduceToken(state, symble, synTreeNodes, o)
                tokenInd -= 1
            else:
                # 出错处理
                parserError.checkGrammar(actionGoto.getKeys(), t)
                return False

            tokenInd += 1
        # 最后只进行规约，看是否可行
        while not (len(symble) == 1 and self.start_of_grammar.__eq__(symble[-1])):
            self.addStateAndSymbol(state, symble, None)
            # 是否为空 然后还没完成
            if len(state) == 0:
                parserError.checkGrammar(None, None)
                return False
            index = state[-1]
            actionGoto = self.agList[index]
            o = actionGoto.get(None)
            if (o == None or isinstance(o, type(1))):
                # 出错处理
                parserError.checkGrammar(actionGoto.getKeys(), None)
                return False
            else:
                # 规约
                self.reduceToken(state, symble, synTreeNodes, o)

        self.addStateAndSymbol(state, symble, None)
        if len(symble) == 1 and self.start_of_grammar.__eq__(symble[-1]):
            self.syncTreeNode = synTreeNodes[-1]
            return True
        parserError.checkGrammar(self.agList[state[-1]].getKeys(), None)
        return False

    # 进行规约，
    # state 状态栈 symbol 符号栈 pAtom 规约产生式
    def reduceToken(self, state, symbol, synTreeNodes, pAtom):
        tmplist = []
        lenn = len(pAtom.getright())
        token = None
        if lenn == 1:
            token = synTreeNodes[-1].getToken()

        for i in range(lenn):
            state.pop()
            symbol.pop()
            tmplist.append(synTreeNodes.pop())
        # 顺序矫正
        tmplist.reverse()
        # 规约
        endstr = pAtom.getleft()
        index = self.agList[state[-1]].get(endstr)
        state.append(index)
        symbol.append(endstr)
        tmpsyncTreeNode = SyncTreeNode(endstr,tmplist,token)
        for t in tmplist:
            t.setFather(tmpsyncTreeNode)
        synTreeNodes.append(tmpsyncTreeNode)


    # 状态符号栈，下一个字符格式输入
    def addStateAndSymbol(self, state, symbol, next):
        self.analysisTable.append("{:<75}{:<100}{:<1}".format(str(state),str(symbol),str(next)))
        #self.analysisTable.append("\n")

    # 生成action goto 表
    def genActionGotoList(self):
        for itemSet in self.itemSetList:
            actionGoto = ActionGoto(itemSet.id)
            actionGoto.putAll(itemSet.shiftItem)
            for i in itemSet.itemList:
                if i.index == len(i.p.getright()):
                    if i.forward == None:
                        actionGoto.put(None, i.p)
                    else:
                        if i.forward.isEndToken():
                            actionGoto.put(None, i.p)
                        actionGoto.putKeys(i.forward.getData(), i.p)
            self.agList.append(actionGoto)

    # 生成状态集族，转换图
    def genItemSetList(self):
        startprodyction = ProductinAtom()
        for i in self.production.getproductionList():
            if self.start_of_grammar.__eq__(i.getleft()):
                startprodyction = i
                break
        # 初始化项目集族
        startitem = ItemSet()
        self.itemSetList.append(startitem)
        startitem.add(Item(startprodyction))
        # 循环遍历每一个项目 this.itemSetList.size()在不断变化
        loop = True
        i = 0
        while loop:
            self.closure(self.itemSetList[i])
            self.searchForward(self.itemSetList[i])
            if i < len(self.itemSetList) - 1:
                i += 1
            else:
                loop = False

    # 传递一个项目，计算闭包
    def closure(self, itemSet):
        item = itemSet.itemList
        loop = True
        i = 0
        while loop:
            tmp = item[i]
            if tmp.index == len(tmp.p.getright()) - 1:
                mayleft = tmp.p.getright()[tmp.index]
                leftMpList = self.production.getLeftMplist(mayleft)
                if (leftMpList != None):
                    for p in leftMpList:
                        item1 = Item(p, 0, tmp.forward)
                        if not item1 in item:
                            item.append(item1)
            elif tmp.index < len(tmp.p.getright()) - 1:
                mayleft = tmp.p.getright()[tmp.index]
                leftMpList = self.production.getLeftMplist(mayleft)
                if (leftMpList != None):
                    secondstr = tmp.p.getright()[tmp.index + 1]
                    for p in leftMpList:
                        item1 = Item(p)
                        item1.forward = self.production.getFirstSet().get(secondstr)
                        if not item1 in item:
                            item.append(item1)
            if i < len(item) - 1:
                i += 1
            else:
                loop = False

    # 向前搜索，计算闭包
    def searchForward(self, itemSet):
        item = itemSet.itemList
        sMap = {}
        keys = []
        # 对每一个产生式，从头到尾
        for tmp in item:
            if (tmp.index < len(tmp.p.getright())):
                str = tmp.p.getright()[tmp.index]
                # itemSet1 = ItemSet()
                if sMap.get(str) != None:
                    itemSet1 = sMap.get(str)
                    itemSet1.itemList.append(Item(tmp.p, tmp.index + 1, tmp.forward))
                else:
                    itemSet1 = ItemSet()
                    itemSet1.itemList.append(Item(tmp.p, tmp.index + 1, tmp.forward))
                    sMap[str] = itemSet1
                    keys.append(str)

        # 解决冲突，重复问题
        idx = len(self.itemSetList)
        for key in keys:
            itemSet1 = sMap.get(key)
            self.closure(itemSet1)
            ind = self.isConflict(itemSet1)
            if ind != -1:
                itemSet.shiftItem[key] = ind
                ItemSet.itemSetCnt -= 1
            else:
                itemSet1.id = idx
                idx += 1
                itemSet.shiftItem[key] = itemSet1.id
                self.itemSetList.append(itemSet1)

    # it:传入一个项目，return项目集族存在该项目情况下的索引
    def isConflict(self, it):
        for i in range(len(self.itemSetList)):
            if self.itemSetList[i].__eq__(it):
                return i
        return -1
