import sys

from Token import  *
from Lexer import *
from TokenType import *


class Parser:
    def __init__(self,lexer,emitter):
        self.lexer = lexer
        self.emitter = emitter

        self.symbols = set()
        self.labelsDeclared = set()
        self.labelsGotoed = set()
        self.hash = {}



        self.curToken = None
        self.peekNext = None
        self.previousToken = None
        self.previousToken2 = None
        self.nextToken()
        self.nextToken()

#returns true if the current token matches
    def checkToken(self,kind):
        return kind == self.curToken.tokenType

#returns true if the next token matches
    def checkPeek(self,kind):
        return kind == self.curToken.tokenType

#match token if not error occurs and moves onto next

    def match(self,kind):
        if not self.checkToken(kind):
            self.abort("expected " + kind.name + " got " + self.curToken.tokenText + self.previousToken.tokenText+ self.previousToken2.tokenText+ self.peekNext.tokenText + self.curToken.tokenText)
        self.nextToken()

    def nextToken(self):
        self.previousToken2 = self.previousToken
        self.previousToken = self.curToken
        self.curToken = self.peekNext
        self.peekNext = self.lexer.getToken()

    def abort(self,message):
        sys.exit("Error " + message)

    def program(self):
        self.emitter.headerLine("public class Teeny\n{")
        self.emitter.headerLine("\tpublic static void main(String[] args)\n\t{")


        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

        while not self.checkToken(TokenType.EOF):
            self.statement()

        self.emitter.emitLine("\t}//Main")
        self.emitter.emitLine("}//Class")

        for label in self.labelsGotoed:
            if label not in self.labelsDeclared:
                self.abort("Attempting to goto an undeclared label")

    def statement(self):

        if self.checkToken(TokenType.PRINT):
            self.nextToken()

            if self.checkToken(TokenType.STRING):
                self.emitter.emitLine("\t\tSystem.out.println(" + self.curToken.tokenText + ");")
                self.nextToken()
            else:
                self.emitter.emit("\t\tSystem.out.println(\"")
                self.expression()
                self.emitter.emitLine("\");")
        elif self.checkToken(TokenType.IF):

            self.nextToken()
            self.emitter.emit("\t\tif(")
            self.comparison()

            self.match(TokenType.THEN)
            self.nl()
            self.emitter.emitLine(")\n\t\t{")

            while not self.checkToken(TokenType.ENDIF):
                self.statement()

            self.match(TokenType.ENDIF)
            self.emitter.emitLine("\t\t}")

        elif self.checkToken(TokenType.WHILE):

            self.nextToken()
            self.emitter.emit("\t\twhile(")
            self.comparison()

            self.match(TokenType.REPEAT)
            self.nl()
            self.emitter.emitLine(")\n\t\t{")

            while not self.checkToken(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)
            self.emitter.emitLine("\t\t}")

        elif self.checkToken(TokenType.LABEL):
            self.nextToken()

            if self.curToken.tokenText in self.labelsDeclared:
                self.abort("Label already exists")
            self.labelsDeclared.add(self.curToken.tokenText)

            self.emitter.emitLine(self.curToken.tokenText + ":")
            self.match(TokenType.IDENT)

        elif self.checkToken(TokenType.GOTO):

            self.nextToken()
            self.labelsGotoed.add(self.curToken.tokenText)
            self.emitter.emitLine("goto " + self.curToken.tokenText + ";")
            self.match(TokenType.IDENT)

        elif self.checkToken(TokenType.LET):
            self.nextToken()

            if self.curToken.tokenText not in self.symbols:
                self.symbols.add(self.curToken.tokenText)


            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)

            if self.curToken.tokenText in self.hash and self.hash[self.curToken.tokenText] == "int":
                self.emitter.emit("\t\tint " + self.previousToken2.tokenText + " = ")
            elif self.checkPeek(TokenType.NUMBER):
                self.emitter.emit("\t\tint " + self.previousToken2.tokenText + " = ")
                self.hash[self.previousToken2.tokenText] = "int"
            else:
                self.emitter.emit("\t\tString " + self.previousToken2.tokenText + " = ")
                self.hash[self.previousToken2.tokenText] = "String"

            self.expression()
            self.emitter.emit(";")
            self.emitter.emitLine(" ")

        elif self.checkToken(TokenType.INPUT):
            self.nextToken()

            if self.curToken.tokenText not in self.symbols:
                self.symbols.add(self.curToken.tokenText)
                self.emitter.headerLine("float " + self.curToken.tokenText + ";")

            self.match(TokenType.IDENT)
        elif self.curToken.tokenText in self.symbols:
            self.emitter.emit("\t\t" + self.curToken.tokenText + " = ")
            self.nextToken()

            self.match(TokenType.EQ)
            self.expression()
            self.emitter.emitLine(";")
        else:
            self.abort("Invalid statement at " + self.curToken.tokenText + " (" + self.curToken.tokenType.name + ") ")
        self.nl()

    def expression(self):

        self.term()

        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.emitter.emit(self.curToken.tokenText)
            self.nextToken()
            self.term()

    def nl(self):

        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

    def comparison(self):

        self.expression()

        if self.isComparisonOperator():
            self.emitter.emit(self.curToken.tokenText)
            self.nextToken()
            self.expression()
        else:
            self.abort("Expected comparison operator at: " + self.curToken.tokenText)

        while self.isComparisonOperator():
            self.emitter.emit(self.curToken.tokenText)
            self.nextToken()
            self.expression()

    def isComparisonOperator(self):
        return self.checkToken(TokenType.GT) or self.checkToken(TokenType.GTEQ) or self.checkToken(TokenType.LT) or self.checkToken(TokenType.LTEQ) or self.checkToken(TokenType.EQEQ) or self.checkToken(TokenType.NOTEQ)

    def term(self):

        self.unary()

        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
            self.emitter.emit(self.curToken.tokenText)
            self.nextToken()
            self.unary()

    def unary(self):

        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.emitter.emit(self.curToken.tokenText)
            self.nextToken()
        self.primary()

    def primary(self):
        if self.checkToken(TokenType.NUMBER):
            self.emitter.emit(self.curToken.tokenText)
            self.nextToken()
        elif self.checkToken(TokenType.IDENT):
            if self.curToken.tokenText not in self.symbols:
                self.abort("referencing variable before assignment " + self.curToken.tokenText)
            self.emitter.emit(self.curToken.tokenText)
            self.nextToken()
        elif self.checkToken(TokenType.STRING):
            if self.hash.get(self.previousToken2.tokenText) == "String":
                self.emitter.emit(self.curToken.tokenText)
                self.nextToken()
            else:
                self.abort("Unexpected token at " + self.curToken.tokenText)
        else:
            self.abort("Unexpected token at " + self.curToken.tokenText)


