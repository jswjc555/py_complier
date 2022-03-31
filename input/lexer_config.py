Key_word = ["class", "void", "function", "static",
            "private", "public", "protected",
            "char", "int", "boolean", "double", "bool", "var",
            "if", "else", "while", "do", "for",
            "this", "return", "null", "print", "liwan"]
Operator = ["+", "-", "*", "/", "+=", "-=", "*=", "/=",
            "++", "--", "&", "|", "~", "&&", "||",
            "<", ">", "=", "<=", ">=", "==", "!="]
Symble = [".", ",", ";", "(", ")", "[", "]", "{", "}"]
ID = "[A-Z|a-z|_][A-Z|a-z|0-9]*"
Constant = "false|true|[0-9]+\.?[0-9]*E?[+|-]?([0-9]+\.?[0-9]*)?|[0-9]+\.?[0-9][+|-][0-9]+\.?[0-9]i"
constant = "true/" \
           "false/" \
           "(+|#)(-|#)DD*((.D*)|#)(E|#)(e|#)(+|#)(-|#)D*((.D*)|#)/" \
           "(+|#)(-|#)DD*((.D*)|#)/" \
           "(+|#)(-|#)DD*((.D*)|#)(+|#)(-|#)D*((.D*)|#)i/" \
           "(\"|#)(\'|#)(D|C)*(\"|#)(\'|#)"
id = "(C|_)(C|D)*"
