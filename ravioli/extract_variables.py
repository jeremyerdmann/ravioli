from pyparsing import (
    Word,
    alphas,
    alphanums,
    Optional,
    delimitedList,
    lineno,
    Keyword, nestedExpr, MatchFirst, printables, ZeroOrMore,
)


class Token:
    def __init__(self, name):
        self.name = name


class VariableExtractor:
    def __init__(self):
        self.declarations = []
        self.usages = []
        self.functions = []

    def extract_declaration(self, token):
        name_index = 1
        # Check for declaration qualifiers.
        if token[0] == "static":
            name_index += 1
        self.declarations.append(Token(token[name_index]))
        print(f"extracting declaration: {token}")

    def extract_assignment(self, token):
        self.usages.append(Token(token[0]))
        print(f"extracting assignment: {token}")

    def extract_function(self, token):
        self.functions.append(Token(token[1]))
        print(f"extracting function: {token}")

    def extract(self, code):
        type_ = Word(alphanums)
        identifier = Word(alphas, alphanums + "_")
        declaration = Optional(Keyword("static")) + type_ + identifier + ";"
        declaration.setParseAction(self.extract_declaration)

        assignment = identifier + "=" + Word(alphanums) + ";"
        assignment.setParseAction(self.extract_assignment)

        function = type_ + identifier + "(" + ... + ")" + nestedExpr("{", "}")
        function.setParseAction(self.extract_function)

        ZeroOrMore(MatchFirst([assignment, declaration, function])).parseString(code)

        return self

    def get_all_as_dict(self):
        """Get all of the extracted variable information in a single dictionary.
        Note: Call `extract` first to do the extraction.
        :return: A dictionary containing all variable information.
        """
        return {
            "declarations": self.declarations,
            "usages": self.usages,
            "functions": self.functions,
        }


def extract_variables(code):
    return VariableExtractor().extract(code).get_all_as_dict()
