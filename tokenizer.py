import tokenClass
import tokenKind
from helperFunctions import toBool
class Tokenizer:
    def __init__(self, source):
        self.source =  source
        self.cursor = 0

    def get(self):
      #  print("SOURCE: " + self.source)
       # print("cursor location: " + str(self.cursor))
        while self.cursor < len(self.source):
            
            match self.source[self.cursor]:
                case ",":
                    self.cursor = self.cursor + 1
                    return tokenClass.Token(self.source[self.cursor - 1], tokenKind.TokenKind.COMMA)
                case "[":
                    self.cursor = self.cursor + 1
                    return tokenClass.Token(self.source[self.cursor - 1], tokenKind.TokenKind.LIST_OPEN)
                case "]":
                    self.cursor = self.cursor + 1
                    return tokenClass.Token(self.source[self.cursor - 1], tokenKind.TokenKind.LIST_CLOSE)
                case ";" |  "\n":
                    self.cursor = self.cursor + 1
                    return tokenClass.Token(self.source[self.cursor - 1], tokenKind.TokenKind.DELIM)
                case "}":
                    self.cursor = self.cursor + 1
                    return tokenClass.Token(self.source[self.cursor - 1], tokenKind.TokenKind.RIGHT_CURLY)                     
                case "{":
                    self.cursor = self.cursor + 1
                    return tokenClass.Token(self.source[self.cursor - 1], tokenKind.TokenKind.LEFT_CURLY)                    
                case "(":
                    self.cursor = self.cursor + 1
                    return tokenClass.Token(self.source[self.cursor - 1], tokenKind.TokenKind.LEFT_PAREN)
                case ")":
                    self.cursor = self.cursor + 1
                    return tokenClass.Token(self.source[self.cursor - 1], tokenKind.TokenKind.RIGHT_PAREN)

                case "+"  | "*" | "/" | "-":
                    self.cursor = self.cursor + 1
                    return tokenClass.Token(self.source[self.cursor - 1], tokenKind.TokenKind.ARITHMETIC_OPERATOR)
                case ">" | "<":
                    self.cursor = self.cursor + 1
                    return tokenClass.Token(self.source[self.cursor - 1], tokenKind.TokenKind.COMPARISON_OPERATOR)

                case "=":
                    self.cursor = self.cursor + 1
                    if self.source[self.cursor] == "=":
                        self.cursor = self.cursor + 1
                        return tokenClass.Token("==", tokenKind.TokenKind.COMPARISON_OPERATOR)
                    else:
                        return tokenClass.Token("=", tokenKind.TokenKind.ASSIGNMENT_OPERATOR)
                case "!":
                    self.cursor = self.cursor + 1
                    if self.source[self.cursor] == "=":
                        self.cursor = self.cursor + 1
                        return tokenClass.Token("!=", tokenKind.TokenKind.COMPARISON_OPERATOR)
                    else:
                        return tokenClass.Token("!", tokenKind.TokenKind.NEGATION_OPERATOR)
                case "\"":
                  stringStart = self.cursor
                  while self.cursor < len(self.source):
                      self.cursor = self.cursor + 1
                      if self.source[self.cursor] == "\"":
                        self.cursor = self.cursor + 1
                        return tokenClass.Token(self.source[stringStart + 1:self.cursor - 1], tokenKind.TokenKind.STRING)

                case _: #Default

                 if self.source[self.cursor].isalpha():
                     
                     identifierStart = self.cursor
                   #  print("alpha")
                     while self.cursor < len(self.source) and self.source[self.cursor].isspace() == False and self.source[self.cursor].isnumeric() or self.source[self.cursor].isalpha() and ",=<>+[-*/{)}](;".find(self.source[self.cursor]) == -1:
                         self.cursor = self.cursor + 1
                     self.cursor = self.cursor + 1
                     if self.source[identifierStart:self.cursor - 1] == "True" or self.source[identifierStart:self.cursor - 1 ]  == "False":
                      return tokenClass.Token(toBool(self.source[identifierStart:self.cursor - 1]), tokenKind.TokenKind.BOOL)
                     #Check for keywords
                     match self.source[identifierStart:self.cursor - 1]:
                         case "input":
                           self.cursor = self.cursor - 1
                           return tokenClass.Token(self.source[identifierStart:self.cursor], tokenKind.TokenKind.INPUT)
                         case "print":
                           self.cursor = self.cursor - 1
                           return tokenClass.Token(self.source[identifierStart:self.cursor], tokenKind.TokenKind.PRINT)
                         case "and" | "or":
                           self.cursor = self.cursor - 1
                           return tokenClass.Token(self.source[identifierStart:self.cursor], tokenKind.TokenKind.COMPARISON_OPERATOR)
                         case "while":
                           self.cursor = self.cursor - 1
                           return tokenClass.Token(self.source[identifierStart:self.cursor], tokenKind.TokenKind.WHILE)
                         case "if":
                           self.cursor = self.cursor - 1
                           return tokenClass.Token(self.source[identifierStart:self.cursor], tokenKind.TokenKind.IF)
                         case "new":
                           self.cursor = self.cursor - 1
                           return tokenClass.Token(self.source[identifierStart:self.cursor], tokenKind.TokenKind.NEW)
                         case "insert":
                           self.cursor = self.cursor - 1
                           return tokenClass.Token(self.source[identifierStart:self.cursor], tokenKind.TokenKind.INSERT)
                         case "delete":
                           self.cursor = self.cursor - 1
                           return tokenClass.Token(self.source[identifierStart:self.cursor], tokenKind.TokenKind.DELETE)
                         case "return":
                           self.cursor = self.cursor - 1
                           return tokenClass.Token(self.source[identifierStart:self.cursor], tokenKind.TokenKind.RETRUN)       
                     
                     return tokenClass.Token(self.source[identifierStart:self.cursor - 1], tokenKind.TokenKind.IDENTIFIER)
                    
                 elif self.source[self.cursor].isnumeric():
                     numStart = self.cursor
                   #  print("numeric")
                     decimalCount = 0
                     while self.cursor < len(self.source) and self.source[self.cursor].isspace() == False and self.source[self.cursor].isalpha() == False and ",=<>+-*/{)}](;".find(self.source[self.cursor]) == -1:
                         if self.source[self.cursor] == ".":
                             decimalCount = decimalCount + 1
                             if decimalCount == 2:
                                 raise ValueError("cannot have more than 1 decimal")
                         self.cursor = self.cursor + 1
                         value = self.source[numStart:self.cursor]
                     return tokenClass.Token(float(self.source[numStart:self.cursor]), tokenKind.TokenKind.NUMBER) 
          
                 else:
                     pass
                    # print("exception: " + self.source[self.cursor])
            self.cursor = self.cursor + 1     
                     
        return tokenClass.Token("",tokenKind.TokenKind.EOF)