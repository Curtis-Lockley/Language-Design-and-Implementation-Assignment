from ast import And
import enum

class TokenKind(enum.Enum):
    #Literals
    IDENTIFIER = "IDENTIFIER" # myVar
    STRING = "STRING" # "Hello World"
    NUMBER = "NUMBER" # 1, -2, 3.4
    BOOL = "BOOL" # True False
    
    #Operators
    ARITHMETIC_OPERATOR = "ARITHMETIC_OPERATOR" # + - * /
    COMPARISON_OPERATOR = "COMPARISON_OPERATOR" # > < !() == 
    ASSIGNMENT_OPERATOR = "ASSIGNMENT_OPERATOR" # =
    NEGATION_OPERATOR = "NEGATION_OPERATOR" # ! e.g !True

    #Lists and Dicts
    LIST_OPEN = "LIST_OPEN"
    LIST_CLOSE = "LIST_CLOSE"
    COMMA = "COMMA"
    
    #Parenthesis
    LEFT_PAREN = "LEFT PARENTHESES" # (
    RIGHT_PAREN = "RIGHT PARENTHESES" # )

    LEFT_CURLY = "LEFT CURLY" # {
    RIGHT_CURLY = "RIGHT CURLY"# }
    
    #Keywords
    IF = "IF"
    RETRUN = "RETURN"
    AND = "AND"
    OR = "OR"
    WHILE = "WHILE"
    NEW = "NEW"

    #Built-in Functions
    PRINT = "PRINT"
    INPUT = "INPUT"
    #Other
    EOF = "EOF"
    DELIM = "DELIM" # newline ;
    INSERT = "INSERT"
    DELETE = "DELETE"
    FUNCTION = "FUNCTION"
