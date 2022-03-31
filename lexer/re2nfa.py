from input import lexer_config
from utils.Exception import RegularExpressionError

# 正则表达式合法的输入字符，D代表数字，C代表大小写字母，#代表空集
legal_cha = ['D', 'C', '.', '*', '|', '#', '(', ')', '+', '-', '_','"','\'']
character = ['.', '+', '-', '#', '_','"','\'']
idx = 0


def new_idx():
    global idx
    idx += 1
    return idx


class pre2suffix:
    def __init__(self, prefixstr):
        self.prefixstr = prefixstr.split('/')
        self.suffix = []
        # 优先函数,c代表字母数字.等合法字符
        self.f = {'^': 3, '*': 5, '|': 5, '(': 1, ')': 5, 'd': 5, 'c': 5, '$': 1}
        self.g = {'^': 2, '*': 4, '|': 4, '(': 6, ')': 1, 'd': 6, 'c': 6, '$': 1}
        # 检查正则表达式字符合法性
        self.check_legal()
        self.join_add()
        self.to_suffix()

    def f_priority(self, char):
        priority = self.f.get(char, -1)
        if priority == -1:
            raise RegularExpressionError("出现未知符号！")
        else:
            return priority

    def g_priority(self, char):
        priority = self.g.get(char, -1)
        if priority == -1:
            raise RegularExpressionError("出现未知符号！")
        else:
            return priority

    # 检查输入的正则表达式合法性,包括括号匹配和正确字符
    def check_legal(self):
        for prestr in self.prefixstr:
            for i in prestr:
                if not i.isalpha() and not i.isdigit() and not legal_cha.count(i):
                    raise RegularExpressionError("正则表达式出现非法字符:" + i)
        tmpstack = []
        for prestr in self.prefixstr:
            for j in prestr:
                if j != "(" and j != ")":
                    continue
                if j == '(':
                    tmpstack.append(j)
                if j == ')' and not tmpstack:
                    raise RegularExpressionError("正则表达式括号不匹配")
                if j == ')' and len(tmpstack):
                    tmpstack.pop()
        if tmpstack:
            raise RegularExpressionError("正则表达式括号不匹配")

    # 在正则表达式里适当位置加+连接符
    def join_add(self):
        new_prefixstr = []
        for prestr in self.prefixstr:
            new_str = ""
            for i in range(len(prestr) - 1):
                first = prestr[i]
                second = prestr[i + 1]
                new_str = new_str + first
                if first != "(" and first != "|" and (second.isalpha() or second.isdigit() or second in character):
                    new_str = new_str + '^'
                elif second == "(" and first != "|" and first != "(":
                    new_str = new_str + '^'
            new_str = new_str + second

            # print(new_str)
            new_prefixstr.append(new_str)
        self.prefixstr = new_prefixstr
        # print(self.prefixstr)

    # 前缀表达式转后缀表达式
    def to_suffix(self):
        for prestr in self.prefixstr:
            prefixstr = prestr + '$'
            suff = ""
            stack = ['$']
            loc = 0
            while stack and loc < len(prefixstr):
                c1, c2 = stack[-1], prefixstr[loc]
                f1 = c1
                f2 = c2
                if c1.isdigit() or c1.isalpha() or c1 in character:
                    f1 = 'c'
                if c2.isdigit() or c2.isalpha() or c2 in character:
                    f2 = 'c'
                if self.f[f1] < self.g[f2]:
                    stack.append(c2)
                    loc += 1
                elif self.f[f1] > self.g[f2]:
                    suff += stack.pop()
                else:
                    stack.pop()
                    loc += 1
            self.suffix.append(suff)


class Nfa_unit:
    def __init__(self):
        self.edges = []
        self.edgecount = 0
        self.startidx = 0
        self.endidx = 0

    def make_edge(self, s, e, chr):
        self.edges.append({"start": s, "end": e, "Trans": chr})
        self.edgecount += 1


class Nfa_Maker:
    def __init__(self, re_expression):
        self.re_expression = re_expression
        self.nfas = []
        self.expression_2_Nfa()
        # self.display()

    def expression_2_Nfa(self):
        n_unit = Nfa_unit()
        x_unit = Nfa_unit()
        y_unit = Nfa_unit()
        for re_str in self.re_expression:
            STACK = []
            for i in range(len(re_str)):
                element = re_str[i]
                if element == '|':
                    y_unit = STACK.pop()
                    x_unit = STACK.pop()
                    n_unit = self.exe_unite(x_unit, y_unit)
                    STACK.append(n_unit)
                elif element == '*':
                    x_unit = STACK.pop()
                    n_unit = self.exe_star(x_unit)
                    STACK.append(n_unit)
                elif element == '^':
                    y_unit = STACK.pop()
                    x_unit = STACK.pop()
                    n_unit = self.exe_join(x_unit, y_unit)
                    STACK.append(n_unit)
                else:
                    n_unit = self.exe_unit(element)
                    STACK.append(n_unit)
            # print("处理完毕")
            self.nfas.append(STACK.pop())

    def unit_unite(self, master, son):
        master_count = master.edgecount
        son_count = son.edgecount
        for i in range(son_count):
            master.edges.append(son.edges[i])
        master.edgecount = master_count + son_count

    def exe_unit(self, chr):
        n_unit = Nfa_unit()
        startidx = new_idx()
        endidx = new_idx()
        n_unit.make_edge(startidx, endidx, chr)
        n_unit.startidx = startidx
        n_unit.endidx = endidx
        return n_unit

    def exe_unite(self, x_unit, y_unit):
        n_unit = Nfa_unit()
        startidx = new_idx()
        endidx = new_idx()
        self.unit_unite(n_unit, x_unit)
        self.unit_unite(n_unit, y_unit)
        n_unit.make_edge(startidx, x_unit.edges[0]["start"], '#')
        n_unit.make_edge(startidx, y_unit.edges[0]["start"], '#')
        n_unit.make_edge(x_unit.edges[x_unit.edgecount - 1]["end"], endidx, '#')
        n_unit.make_edge(y_unit.edges[y_unit.edgecount - 1]["end"], endidx, '#')
        n_unit.startidx = startidx
        n_unit.endidx = endidx
        return n_unit

    def exe_join(self, x_unit, y_unit):
        for i in range(y_unit.edgecount):
            if y_unit.edges[i]["start"] == y_unit.startidx:
                y_unit.edges[i]["start"] = x_unit.endidx
            elif y_unit.edges[i]["end"] == y_unit.startidx:
                y_unit.edges[i]["end"] = x_unit.endidx
        y_unit.startidx = x_unit.endidx
        self.unit_unite(x_unit, y_unit)
        x_unit.endidx = y_unit.endidx
        return x_unit

    def exe_star(self, x_unit):
        n_unit = Nfa_unit()
        startidx = new_idx()
        endidx = new_idx()
        self.unit_unite(n_unit, x_unit)
        n_unit.make_edge(startidx, endidx, '#')
        n_unit.make_edge(x_unit.endidx, x_unit.startidx, '#')
        n_unit.make_edge(startidx, x_unit.startidx, '#')
        n_unit.make_edge(x_unit.endidx, endidx, '#')
        n_unit.startidx = startidx
        n_unit.endidx = endidx

        return n_unit

    def display(self):
        for i in self.nfas:
            print("NFA边数：" + str(i.edgecount))
            print("NFA起始状态:" + str(i.startidx))
            print("NFA终止状态：" + str(i.endidx))
            for j in range(len(i.edges)):
                print("第" + str(j + 1) +
                      "条边的起始状态:" + str(i.edges[j]["start"])
                      + "    终止状态:" + str(i.edges[j]["end"])
                      + "   状态转换符:" + str(i.edges[j]["Trans"]))

    def match(self, str):
        begin, end = 0, 0
        match_flag = False
        for nfa in self.nfas:
            fake_end = 0
            loop = True
            already_get = []
            already_get.append(nfa.startidx)
            immi_stop = True
            while loop:
                loop = False
                sharp_loop = True
                while (sharp_loop):
                    sharp_loop = False
                    for i in nfa.edges:
                        if i["start"] in already_get and i["Trans"] == '#' and i["end"] not in already_get:
                            already_get.append(i["end"])
                            sharp_loop = True
                            immi_stop = False
                c = str[fake_end]
                next_end = False  # True的意思是只要所有边有匹配到当前字符的，就fake_end+1
                for i in nfa.edges:
                    if i["start"] in already_get and (i["Trans"] == c or (i["Trans"] == 'D' and c.isdigit())
                                                      or (i["Trans"] == 'C' and (c.isalpha() or c =='_'))):
                        next_end = True
                        if fake_end < len(str) - 1:
                            loop = True
                        if i["end"] not in already_get:
                            already_get.append(i["end"])
                            if nfa.endidx in already_get and immi_stop:  # 如果是无#的nfa则指针不+1，立即结束
                                loop = False
                            break
                if next_end:
                    fake_end += 1

            if nfa.endidx in already_get or (len(str) == 1 and fake_end):
                match_flag = True
                end = max(end, fake_end)
            if immi_stop and match_flag:
                break
        if match_flag == False:
            return 0, 0
        else:
            return begin, end
