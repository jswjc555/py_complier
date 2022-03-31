class Token():
    def __init__(self, row, col, t_type, value):
        self.row = row
        self.col = col
        self.type = t_type
        self.value = value

    def __str__(self):
        return "Token{" +\
              "row= " + str(self.row) +\
              ", col=" + str(self.col) +\
              ", tokentype='" + self.type +\
              "', value='" + self.value +\
              '\'}'

