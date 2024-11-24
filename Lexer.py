import sys

from Token import *
from TokenType import *

class Lexer:
    def __init__(self,source):
        self.source = source + '\n'
        self.curPos = -1
        self.curChar = ''
        self.nextChar()

    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = '/0'
        else:
            self.curChar = self.source[self.curPos]
    def peekNextChar(self):
        if self.curPos + 1 >= len(self.source):
            return '/0'
        return self.source[self.curPos + 1]

    def skipWhiteSpace(self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()

    def skipComment(self):
        if(self.curChar == '#'):
            while(self.curChar != '\n'):
                self.nextChar()

    def abort(self,message):
        sys.exit("Lexing error: " + message)

    def getToken(self):
        token = None

        self.skipWhiteSpace()
        self.skipComment()

        if self.curChar == '+':
            token = Token(TokenType.PLUS,self.curChar) #plus token
        elif self.curChar == '-':
                token = Token(TokenType.MINUS,self.curChar)
        elif self.curChar == '*':
            token = Token(TokenType.ASTERISK,self.curChar)
        elif self.curChar == '/':
            token = Token(TokenType.SLASH,self.curChar)
        elif self.curChar == '\n':
            token = Token(TokenType.NEWLINE,self.curChar)
        elif self.curChar == '/0':
            token = Token(TokenType.EOF,self.curChar)
        elif self.curChar == '=':
            if self.peekNextChar() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(TokenType.EQEQ,lastChar + self.curChar)
            else:
                token = Token(TokenType.EQ,self.curChar)
        elif self.curChar == '>':
            if self.peekNextChar() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(TokenType.GTEQ,lastChar + self.curChar)
            else:
                token = Token(TokenType.GT,self.curChar)
        elif self.curChar == '<':
            if self.peekNextChar() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(TokenType.LTEQ,lastChar + self.curChar)
            else:
                token = Token(TokenType.LT,self.curChar)
        elif self.curChar == '!':
            if self.peekNextChar() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(TokenType.NOTEQ,lastChar + self.curChar)
            else:
                self.abort("Unknown Token " + self.curChar)
        elif self.curChar == '\"':
            startPos = self.curPos
            self.nextChar()

            while self.curChar != '"':
                if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                    self.abort("Illegal char")
                self.nextChar()

            tokenText = self.source[startPos:self.curPos+1]
            token = Token(TokenType.STRING,tokenText)
        elif self.curChar.isdigit():

            startPos = self.curPos
            while self.peekNextChar().isdigit():
                self.nextChar()

            if self.peekNextChar() =='.':
                self.nextChar()

                if not self.peekNextChar().isdigit():
                    self.abort("Character in numbers no no no")

                while self.peekNextChar().isdigit():
                    self.nextChar()

            tokenText = self.source[startPos:self.curPos + 1]
            token = Token(TokenType.NUMBER,tokenText)

        elif self.curChar.isalnum():
            startPos = self.curPos

            while self.peekNextChar().isalnum():
                self.nextChar ()

            tokenText = self.source[startPos:self.curPos + 1]
            keyword = Token.checkIfKeyword(tokenText)

            if keyword == None:
                token = Token(TokenType.IDENT,tokenText)
            else:
                token = Token(keyword,tokenText)
        else:
            self.abort("Unknown Token " + self.curChar)

        self.nextChar()

        return token

