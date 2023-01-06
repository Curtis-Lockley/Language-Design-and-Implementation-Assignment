import tokenClass
import tokenKind
from tokenizer import Tokenizer
from helperFunctions import isFloat



tempTokens = []
class Instruction:
    def __init__(self, type,value,dataType):
        self.type = type
        self.value = value
        self.dataType = dataType



def performOp(op,num1,num2):
    # print("op: " + op + " num1: " + str(num1) + " num 2: " + str(num2))
    match op:
        case "+":
            return num1 + num2
        case "-":
            return num1 - num2
        case "*":
            return num1 * num2
        case "/":
            return num1 / num2
        case "==":
            return num1 == num2
        case "!=":
            return num1 != num2
        case ">":
            return num1 > num2
        case "<":
            return num1 < num2
        case "or":
            return num1 or num2
        case "and":
            return num1 and num2
    pass

def opPrecedence(op1, op2):
    precedenceTable = {
    "[": 10,
    "*": 3,
    "/": 3,
    "+" : 2,
    "-" : 2,
    "<": 1,
    "<=": 1,
    ">": 1,
    ">=": 1,
    "==": 0,
    "!=":0,
    "!": 4,
    "or": -1,
    "and": -1 

    }
    

    if  precedenceTable[op1] > precedenceTable[op2]:
        return 1 #o1 has greater precedence than o2
    if  precedenceTable[op1] == precedenceTable[op2]:
        return 0 # equal
    return -1 #o2 has greater precedence or equal to o1

def infixToPost(stack):
  #    input("infix to post strted!")
      outputQueue = []
      operatorStack = []
     
      cursor = 0
      while cursor != len(stack):
       #print(stack[cursor].getText())
       match stack[cursor].getKind().value:
           case "NUMBER" | "IDENTIFIER" | "BOOL" | "STRING" | "LIST_OPEN" | "LIST_CLOSE":
               outputQueue.append(stack[cursor])
           case "ARITHMETIC_OPERATOR" | "COMPARISON_OPERATOR" | "NEGATION_OPERATOR":
               
               while len(operatorStack) != 0 and operatorStack[len(operatorStack) - 1].getKind().value != "LEFT PARENTHESES" and (opPrecedence(stack[cursor].getText(),operatorStack[len(operatorStack) - 1].getText()) == -1 or opPrecedence(stack[cursor].getText(),operatorStack[len(operatorStack) - 1].getText()) == 0):
                   outputQueue.append(operatorStack.pop())
               operatorStack.append(stack[cursor])
           case "LEFT PARENTHESES":
               operatorStack.append(stack[cursor])
           case "RIGHT PARENTHESES":
               while len(operatorStack) != 0 and operatorStack[len(operatorStack) - 1].getKind().value != "LEFT PARENTHESES":
                   outputQueue.append(operatorStack.pop())
               operatorStack.pop() 
       cursor = cursor + 1
        
      while len(operatorStack) != 0:
          outputQueue.append(operatorStack.pop())
      
      
      for i in outputQueue:
          print(str(i.getText()), end = " ")

     # input("postfix done!")
      return outputQueue
               

class Parser():
  def __init__(self, source):
        self.source =  source
        self.cursor = 0
        self.result = []
        self.stack = []
        self.neg = []
        self.openBrackets = 0
        self.openParens = 0
  
  def outPutSource(self):
      result = ""
      for t in self.source:
          print(str(t.getText()))



  def parseNumber(self):
              opStack = []
              isList = False
              isDict = False
              listType = None
              access = True
              #Check remaining tokens
              while self.source[self.cursor].getKind().value != "EOF" and self.source[self.cursor].getKind().value != "DELIM" and self.source[self.cursor].getKind().value != "LEFT CURLY":
                   print(str(self.source[self.cursor].getText()))
                   match self.source[self.cursor].getKind().value:

                       case "LIST_OPEN":
                           opStack.append(self.source[self.cursor])
                           tempCursor = self.cursor + 1
                           if self.source[tempCursor].getKind().value != "LIST_CLOSE":
                            while access == True and self.source[tempCursor].getKind().value != "LIST_CLOSE":
                               match self.source[tempCursor].getKind().value:
                                case "COMMA" | "":
                                    access = False
                                case _:
                                    tempCursor = tempCursor + 1
                           else:
                               access = False
                               self.cursor = self.cursor + 1
                           isList = True
                           self.cursor = self.cursor + 1

                       case "NUMBER" | "BOOL" | "STRING" |"IDENTIFIER":
                           #Check that next element is not invalid
                           opStack.append(self.source[self.cursor])
                           self.cursor = self.cursor + 1
                           match self.source[self.cursor].getKind().value:

                               case "LIST_OPEN":
                                   access = True
                                   opStack.append(self.source[self.cursor])
                                   isList = True
                                   self.cursor = self.cursor + 1
                               case "LIST_CLOSE":
                                 if isList:
                                  isList = False
                                  if access == True:
                                   opStack.append(self.source[self.cursor])
                                  self.cursor = self.cursor + 1  
                               
                               case "COMMA":
                                   #check if in list
                                   if isList or isDict:
                                       self.cursor = self.cursor + 1
                                   else:
                                       input("INVALID SYNTAX, NOT A LIST OR DICTIONARY!")
                               case "NUMBER" | "BOOL" | "STRING" |"IDENTIFIER" | "NEGATION_OPERATOR":
                                   input("INVALID SYNTAX!")
                               case "ARITHMETIC_OPERATOR" | "COMPARISON_OPERATOR":
                                   opStack.append(self.source[self.cursor])
                                   self.cursor = self.cursor + 1
                                   match self.source[self.cursor].getKind().value:
                                       case "ARITHMETIC_OPERATOR" | "COMPARISON_OPERATOR":
                                           input("INVALID SYNTAX!")
                                       case "LEFT PARENTHESES":
                                           self.openParens = self.openParens + 1
                                           opStack.append(self.source[self.cursor])
                                           self.cursor = self.cursor + 1
                               case "EOF" | "DELIM" | "RIGHT PARENTHESES" | "LEFT PARENTHESES":
                                   pass
                               case _:
                                   input("INVALID SYNTAX! " + self.source[self.cursor].getKind().value)
                                   pass
                       case "LEFT PARENTHESES":
                           self.openParens = self.openParens + 1
                           opStack.append(self.source[self.cursor])
                           self.cursor = self.cursor + 1
                       case "RIGHT PARENTHESES":
                           self.openParens = self.openParens - 1
                           opStack.append(self.source[self.cursor])
                           self.cursor = self.cursor + 1
                           if self.openParens <  0:
                               input("INVALID SYNTAX UNOPENED PARENS!")

                       case "ARITHMETIC_OPERATOR" | "COMPARISON_OPERATOR":
                            opStack.append(self.source[self.cursor])
                            self.cursor = self.cursor + 1
                            
                       case "NEGATION_OPERATOR":
                            opStack.append(self.source[self.cursor])
                            self.cursor = self.cursor + 1
                            #Search for bool evidence
                            tempCursor = self.cursor
                            openParens = 0
                            boolEvidence = False
                            while boolEvidence == False:
                                print(str(self.source[tempCursor].getText()))
                                match self.source[tempCursor].getKind().value:
                                    case "BOOL":
                                        boolEvidence = True
                                    case "LEFT PARENTHESES":
                                        #Evidence has to be inside brackets or it is invalid syntax
                                        openParens = openParens + 1
                                        tempCursor = tempCursor + 1
                                        while openParens > 0 or boolEvidence == False:
                                         match self.source[tempCursor].getKind().value:
                                          case "RIGHT PARENTHESES":
                                              openParens = openParens - 1
                                              tempCursor = tempCursor + 1
                                              if openParens == 0 and boolEvidence == False:
                                                  input("INVALID SYNTAX, NO BOOL FOUND!")
                                          case "LEFT PARENTHESES":
                                              openParens = openParens + 1
                                              tempCursor = tempCursor + 1
                                          
                                          case "COMPARISON_OPERATOR":
                                              boolEvidence = True
                                              tempCursor = tempCursor + 1
                                          case _:
                                              tempCursor = tempCursor + 1

                                tempCursor = tempCursor + 1
                            opStack.extend(self.source[self.cursor:tempCursor])
                            self.cursor = tempCursor


     
              print("mathematical expression found")

              self.stack.extend(infixToPost(opStack))

  def stackToInstructions(self):
      ifCount = -1
      ifEndStack = []
      seenFunctions = []
      inFunction = False
      currentFunction = ""
      noJump = False
      newStack = []
      setStack = []
      skipIteration = False
    #  input("source: " + str(len(self.source)) + "\tstack: " + str(len(self.stack)))


      print("Converting stack to instructions")
      for e in self.stack:
          print(str(e.getText()) + "\t" + e.getKind().value)
     # input("stack above!")
      for idx, i in enumerate(self.stack):
          if skipIteration == True:
              skipIteration = False
              continue
          match i.getKind().value:

               case "RETURN":
                   newStack.append(Instruction("RET",None,None))
               
               case "FUNCTION":
                   if i.getText() not in seenFunctions:
                       seenFunctions.append(i.getText())
                       newStack.append(Instruction("LABEL",i.getText(),None))
                       noJump = True
                       inFunction = True
                       currentFunction = i.getText()
                   else:
                       newStack.append(Instruction("JMP",i.getText(),None))

               case "NEW":
                   newStack.append(Instruction("NEW-FLAG",None,None))
               case "LIST_OPEN":
                   newStack.append(Instruction("LIST-FLAG",None,None))
               case "LIST_CLOSE":
                    newStack.append(Instruction("LIST-ACCESS-FLAG",None,None))
               case "PRINT":
                   newStack.append(Instruction("PRINT", "",None))
               case "INPUT":
                   newStack.append(Instruction("INPUT", None ,None))
               
               case "NEGATION_OPERATOR":
                   newStack.append(Instruction("NOT", i.getText(),i.getKind().value))
               case "WHILE" | "IF":
                   ifCount = ifCount + 1
                   newStack.append(Instruction("LABEL", i.getText()+str(ifCount),i.getKind().value))
                   #Find closing parens to place
                   if i.getKind().value == "WHILE":
                       ifEndStack.append([Instruction("JMP", "while" + str(ifCount) ,i.getKind().value),Instruction("EXIT", "exit" + str(ifCount) ,i.getKind().value)])
                   else:
                    ifEndStack.append([Instruction("EXIT", "exit" + str(ifCount) ,i.getKind().value)])
               case "LEFT CURLY":
                   if noJump == False:
                    newStack.append(Instruction("JIF","exit" + str(ifCount),None))
                   noJump = False
               case "RIGHT CURLY":
                   if len(ifEndStack) > 0:
                    newStack.extend(ifEndStack.pop())
                   
                   elif inFunction:
                       inFunction = False
                       newStack.append(Instruction("EXIT", "exit" + currentFunction,None))

               case "DELIM":
                   if len(setStack) > 0:
                       idx = idx + 1
                       variable = setStack.pop()
                       newStack.append(Instruction("SET", variable.getText(),variable.getKind().value))
                    
                   newStack.append(Instruction("CLEAR", None,None))
               
               case "INSERT" | "DELETE":
                   newStack.append(Instruction(i.getKind().value, self.stack[idx + 1].getText(),None))
                   skipIteration = True

               case "IDENTIFIER":
                   if len(self.stack) > 2 and self.stack[idx + 1].getKind().value == "ASSIGNMENT_OPERATOR":
                       setStack.append(i)
                       skipIteration = True
                   else:
                       newStack.append(Instruction("GET", i.getText(),i.getKind().value))
                       

               case "COMPARISON_OPERATOR":
                   newStack.append(Instruction("CMP", i.getText(),i.getKind().value))
               case "ARITHMETIC_OPERATOR":
                   type = ""
                   match i.getText():
                       case "+":
                           type = "ADD"
                       case "-":
                           type = "SUB"
                       case "*":
                           type = "MULT"
                       case "/":
                           type = "DIV"
                           
                       
                   newStack.append(Instruction(type, i.getText(),i.getKind().value))

               case _:
                   newStack.append(Instruction("PUSH", i.getText(),i.getKind().value))
          
      return newStack

  def executeInstructions(self):
      dataStack = []
      
      scopeStack = [{}] # for each scope a new dictionary of variables is created
      cursor = 0
      scopesInFunction = 0
      callStack = []
      listFlag = False
      listAccess = False
      ifFlag = False
      newFlag = False
      print("STACK")
      for i in self.stack:
       print(i.type + "\t" + str(i.value))

     # input("\nexecuting stack instructions")
      
      while self.stack[cursor].type != "EOF":
          
          match self.stack[cursor].type:
              
              case "INSERT":
                  #Find list in scopestack
                  listName = self.stack[cursor].value
                  for s in range(len(scopeStack),0,-1):
                      if listName in scopeStack[s - 1]:
                          scopeStack[s - 1][listName].append(dataStack.pop())
                          break
              case "DELETE":
                  #Find list in scopestack
                  listName = self.stack[cursor].value
                  for s in range(len(scopeStack),0,-1):
                      if listName in scopeStack[s - 1]:
                          del scopeStack[s - 1][listName][int(dataStack.pop())]
                          break                  

              case "NEW-FLAG":
                  newFlag = True
              case "LIST-ACCESS-FLAG":
                     #Get list Name
                     l = self.stack[cursor - 3].value
                     #Find list in scope stack
                     for s in range(len(scopeStack),0,-1):
                         #search scope for variable
                          
                         if self.stack[cursor - 3].value in scopeStack[s - 1]:
                             dataStack.append(scopeStack[s - 1][self.stack[cursor - 3].value][int(dataStack.pop())])
                             break

              case "LIST-FLAG":
                  if self.stack[cursor - 1].type != "GET":
                   listFlag = True

              case "GET":
                  var = self.stack[cursor].value
                  for s in range(len(scopeStack),0,-1):
                      if var in scopeStack[s - 1]:
                          dataStack.append(scopeStack[s - 1][self.stack[cursor].value])
                          break
                #   for s in scopeStack:
                 
                #       if self.stack[cursor].value in s:
                #           #Set value if already defined
                #           dataStack.append(s[self.stack[cursor].value])
              case "LABEL":
                  if self.stack[cursor].value.startswith('if') or self.stack[cursor].value.startswith('while'):
                      ifFlag = True
                  else:
                      #Jump to end of funciton
                      functionName = self.stack[cursor].value
                      while not (self.stack[cursor].value == "exit" + functionName):
                          cursor = cursor + 1
                      
              case "CLEAR":
                #   if ifFlag == False:
                #       dataStack = []
                pass
              case "NOT":
                  if dataStack.pop() == True:
                      dataStack.append(False)
                  else:
                      dataStack.append(True)

              case "JMP":
                  if not (self.stack[cursor].value.startswith("if")) and not (self.stack[cursor].value.startswith("while")):
                   callStack.append(cursor)
                  else:
                      scopeStack.pop()
                  label = self.stack[cursor].value
                  while self.stack[cursor].value != label or  self.stack[cursor].type != "LABEL":
                      cursor = cursor - 1
                  if not (label.startswith('if')) and not (label.startswith('while')): 
                      scopeStack.append({})
                  
              case "JIF":
                  ifFlag = False

                  jmpToExit = performOp("==",True,dataStack.pop())
                  if jmpToExit == False:
                      
                      exit = self.stack[cursor].value
                      #Search for exit with same number
                      while self.stack[cursor].value != exit or self.stack[cursor].type != "EXIT":
                       cursor = cursor + 1
                  else: 
                      scopeStack.append({})
                      if len(callStack) != 0:
                          scopesInFunction = scopesInFunction + 1
                      
              case "RET":
                  scopeStack.pop()
                  while scopesInFunction != 0:
                      scopeStack.pop()
                      scopesInFunction = scopesInFunction - 1
                  cursor = callStack.pop()
              case "EXIT":
                  scopeStack.pop()
                  if scopesInFunction != 0:
                      scopesInFunction = scopesInFunction - 1

                   
              case "SET":
                  value = None
                  if listFlag == False:
                   value = dataStack.pop()
                  else:
                   #Determine how large the list is
                   value = []
                   tempCursor = cursor - 1
                   distance = 0
                   while(self.stack[tempCursor].type != "LIST-FLAG"):
                       distance = distance + 1
                       tempCursor = tempCursor - 1
                   while distance != 0:
                       distance = distance - 1
                       value.append(dataStack.pop())
                   value.reverse()
                   listFlag = False

                  #if NEW keyword not used, search from bottom of the stack up
                  if newFlag == False:
                   #Iterate backwards in scope stack to find variable
                   scopeCursor = len(scopeStack) - 1
                   variableFound = False
                   insert = self.stack[cursor].value
                   while scopeCursor > -1:
                    #Check if variable exists in current scope
                    if self.stack[cursor].value in scopeStack[scopeCursor]:
                        #Change existing value
                        variableFound = True
                        scopeStack[scopeCursor][self.stack[cursor].value] = value
                        scopeCursor = -1
                    scopeCursor = scopeCursor - 1

                   #Make new variable in latest scope
                   if variableFound == False:
                    scopeStack[len(scopeStack) - 1][self.stack[cursor].value] = value
              
                  else:
                      #If NEW keyword used, always write to latest scope
                      newFlag = False
                      scopeStack[len(scopeStack) - 1][self.stack[cursor].value] = value



              case "PUSH":
                  dataStack.append(self.stack[cursor].value)
              case "ADD" | "SUB" | "MULT" | "DIV" | "CMP":
                
                  op1 = dataStack.pop()
                  op2 = dataStack.pop()
                  if isinstance(op1,str) or isinstance(op2,str):
                      op1 = str(op1)
                      op2 = str(op2)
                  dataStack.append(performOp(self.stack[cursor].value,op2,op1))

              case "PRINT":
                  popped = None
                  if len(dataStack) != 0:
                      popped = dataStack.pop()
                  print(popped)
              case "INPUT":
                  popped = None
                  if len(dataStack) != 0:
                      popped = dataStack.pop()
                  entered = input(popped or "")
                  if entered == '':
                      entered = ""
                  if entered.isnumeric():
                      entered = float(entered)
                  elif isFloat(entered):
                      entered = float(entered)
                  if entered == "True" or entered == "False":
                      entered = entered == "True"
                  dataStack.append(entered)

          cursor = cursor + 1

  def parseTokens(self):
        print("parsing token list")
        whileBrace = False
        leftBrace = False
        seenFunctions = []

        while self.source[self.cursor].getKind().value != "EOF":
         #Determine what the parser is looking at
         print(str(self.source[self.cursor].getText()) + "\t" + self.source[self.cursor].getKind().value)
         match self.source[self.cursor].getKind().value:
             
             case "RETURN":
                 self.stack.append(self.source[self.cursor])
                 self.cursor = self.cursor + 1
             case "PRINT" | "INPUT":
                 #Check correct formatting
                 temp = self.source[self.cursor]
                 self.cursor = self.cursor + 1
                  
                 if self.source[self.cursor].getKind().value == "LEFT PARENTHESES":
                     self.parseNumber()
                     self.stack.append(temp)
             case "LIST_OPEN":
                self.parseNumber()
                 
             case "RIGHT PARENTHESES":
                 self.cursor = self.cursor + 1
                    
             case "DELIM":
                 self.stack.append(self.source[self.cursor])
                 self.cursor = self.cursor + 1
             case "IDENTIFIER":
                 self.cursor = self.cursor + 1
                 match self.source[self.cursor].getKind().value:
                  case "LEFT PARENTHESES":
                       self.cursor = self.cursor + 1
                       if self.source[self.cursor].getKind().value == "RIGHT PARENTHESES":
                           #Function
                           self.cursor = self.cursor + 1
                           if self.source[self.cursor - 3].getText() not in seenFunctions:
                               seenFunctions.append(self.source[self.cursor - 3].getText())
                               whileBrace = True

                           self.stack.append(tokenClass.Token(self.source[self.cursor - 3].getText(), tokenKind.TokenKind.FUNCTION))
                           
                  
                  case "ASSIGNMENT_OPERATOR":
                     match self.source[self.cursor - 2].getKind().value:
                         case "NEW":
                             self.stack.extend([self.source[self.cursor - 2],self.source[self.cursor - 1],self.source[self.cursor]])
                         case _:
                             self.stack.extend([self.source[self.cursor - 1],self.source[self.cursor]])
                     self.cursor = self.cursor + 1
                  case "INSERT" | "DELETE":
                      tempCursor = self.cursor
                      self.cursor = self.cursor + 1
                      if self.source[self.cursor].getKind().value == "LEFT PARENTHESES":
                        self.parseNumber()
                        self.stack.extend([self.source[tempCursor],self.source[tempCursor - 1]])
                      else:
                          input("INVALID INSERT/DELETE CALL")

                  case "ARITHMETIC_OPERATOR":
                      #check is bool, string or number arithmetic
                      tempCursor = self.cursor + 1
                      while self.source[tempCursor].getKind().value != "EOF" or self.source[tempCursor].getKind().value != "DELIM":
                          match self.source[tempCursor].getKind().value:
                              case "NUMBER" | "STRING" | "BOOL" | "IDENTIFIER":
                                  self.cursor = self.cursor - 1
                                  self.parseNumber()
                                  break
                          tempCursor = tempCursor + 1
                  case _:
                      self.cursor = self.cursor - 1
                      self.parseNumber()

             case "WHILE" | "IF":
                 #Check that while format is correct
                 self.stack.append(self.source[self.cursor])
                 self.cursor = self.cursor + 1
                 if self.source[self.cursor].getKind().value == "LEFT PARENTHESES":
                     #Find matching right paren
                     tempCursor = self.cursor
                     openParens = 1
                     boolEvidence = False
                     
                     while openParens != 0 and  self.source[tempCursor].getKind().value != "EOF":
                         tempCursor = tempCursor + 1
                         match self.source[tempCursor].getKind().value:
                          case "LEFT PARENTHESES":
                              openParens = openParens + 1
                          case "RIGHT PARENTHESES":
                              openParens = openParens - 1
                          case "COMPARISON_OPERATOR" | "BOOL":
                              boolEvidence = True
                     if boolEvidence == "FALSE":
                        input("NO BOOL FOUND IN WHILE!")
                     
                    #  print(self.source.pop(tempCursor).getKind().value)
                    #  print(self.source.pop(self.cursor).getKind().value)
                     
                     
                     tempCursor = tempCursor - 1
                     #Find while loop opening curly braces
                     leftCurly = - 1
                     openParens = 1
                     while leftCurly == -1:
                         kind = self.source[tempCursor].getKind().value
                         match self.source[tempCursor].getKind().value:
                             case "DELIM":
                                 tempCursor = tempCursor + 1
                             case "LEFT CURLY":

                                 leftCurly = tempCursor
                                 #find corresponding right brace
                                 while openParens != 0:
                                     tempCursor = tempCursor + 1
                                     kind = self.source[tempCursor].getKind().value
                                     match self.source[tempCursor].getKind().value:
                                         case "RIGHT CURLY":
                                             openParens = openParens - 1
                                         case "LEFT CURLY":
                                             openParens = openParens + 1
                                 whileBrace = True 
                             case _:
                                 tempCursor = tempCursor + 1
                     print(self.source[self.cursor].getKind().value)
                     self.parseNumber()        
                    

             case "STRING":
                 self.parseNumber()

             case "BOOL":
                 self.parseNumber()



                          
             case "RIGHT CURLY":
                 if leftBrace == True:
                  self.stack.append(self.source[self.cursor])
                  self.cursor = self.cursor + 1
                 else:
                  input("INVALID RIGHT CURLY!")

             case "LEFT CURLY":
                 if whileBrace == True:
                  self.stack.append(self.source[self.cursor])
                  self.cursor = self.cursor + 1
                  leftBrace = True
                 else:
                  input("INVALID LEFT CURLY!")

             case "NUMBER":
                 self.parseNumber()
             case "LEFT PARENTHESES":
                 self.parseNumber()
             case _:
                 self.cursor = self.cursor + 1

              
        print("parsing complete!")


            
        self.stack =  self.stackToInstructions()
        self.stack.append(Instruction("EOF",None,None))
        
        self.executeInstructions()


tokenList = []

test = Tokenizer(str(open("bool.txt", "r").read()))

#Get first token
myToken = test.get()
tokenList.append(myToken)

#Get remaining tokens
while myToken.getKind().value != "EOF":
    myToken = test.get()
    if myToken.getKind().value == "NUMBER" and (tokenList[len(tokenList) - 1].getKind().value == "ARITHMETIC_OPERATOR" and tokenList[len(tokenList) - 1].getText() == "-") and (tokenList[len(tokenList) - 2].getKind().value != "NUMBER" and tokenList[len(tokenList) - 2].getKind().value != "IDENTIFIER" ):
        tokenList.pop()
        myToken.text = 0 - myToken.getText()
    if not (tokenList[len(tokenList) - 1].getKind().value == "DELIM" and myToken.getKind().value == "DELIM"):
     tokenList.append(myToken)


for t in tokenList:
    print(t.getKind().value, end = " ")
print("")
for t in tokenList:
    print(str(t.getText()), end = " ")


#Parse and execute tokens
I2P = Parser(tokenList)
I2P.parseTokens()

