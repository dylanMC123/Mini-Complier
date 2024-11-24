from TokenType import *
class Token:
    def __init__(self,tokenType,tokenText):
        self.tokenType = tokenType
        self.tokenText = tokenText

    @staticmethod
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
                return kind
        return None

