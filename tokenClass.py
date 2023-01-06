

class Token:
    def __init__(self, text, kind):
     self.text = text
     self.kind = kind
    
    def getKind(self):
        return self.kind
    
    def getText(self):
     return self.text



# myToken = Token("6", tokenKind.TokenKind.IF)


# print(myToken.getText())