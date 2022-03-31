class SyncTreeNode:
    cnt = 0

    def __init__(self, val=None, child=None, token=None):
        self.val = val
        self.child = child
        self.id = SyncTreeNode.cnt
        SyncTreeNode.cnt += 1
        self.token = token
        self.father = None

    def getToken(self):
        return self.token

    def setFather(self,father):
        self.father = father