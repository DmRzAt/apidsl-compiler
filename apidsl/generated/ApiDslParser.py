# Generated from grammar/ApiDsl.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,29,134,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        1,0,3,0,30,8,0,1,0,4,0,33,8,0,11,0,12,0,34,1,0,1,0,1,1,1,1,1,1,1,
        1,1,2,1,2,1,2,1,2,5,2,47,8,2,10,2,12,2,50,9,2,1,2,1,2,1,3,1,3,1,
        3,3,3,57,8,3,1,4,1,4,1,4,1,4,3,4,63,8,4,1,4,5,4,66,8,4,10,4,12,4,
        69,9,4,1,4,1,4,1,5,1,5,1,6,1,6,1,6,1,6,1,6,1,7,1,7,1,7,1,7,1,7,1,
        7,1,7,3,7,87,8,7,1,7,1,7,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,9,1,9,1,9,
        5,9,101,8,9,10,9,12,9,104,9,9,1,10,1,10,1,11,1,11,1,11,1,11,5,11,
        112,8,11,10,11,12,11,115,9,11,3,11,117,8,11,1,11,1,11,1,12,1,12,
        1,12,1,12,1,13,1,13,1,13,1,13,1,13,1,13,1,13,3,13,132,8,13,1,13,
        0,0,14,0,2,4,6,8,10,12,14,16,18,20,22,24,26,0,2,1,0,3,6,2,0,16,16,
        18,18,136,0,29,1,0,0,0,2,38,1,0,0,0,4,42,1,0,0,0,6,56,1,0,0,0,8,
        58,1,0,0,0,10,72,1,0,0,0,12,74,1,0,0,0,14,79,1,0,0,0,16,90,1,0,0,
        0,18,97,1,0,0,0,20,105,1,0,0,0,22,107,1,0,0,0,24,120,1,0,0,0,26,
        131,1,0,0,0,28,30,3,2,1,0,29,28,1,0,0,0,29,30,1,0,0,0,30,32,1,0,
        0,0,31,33,3,4,2,0,32,31,1,0,0,0,33,34,1,0,0,0,34,32,1,0,0,0,34,35,
        1,0,0,0,35,36,1,0,0,0,36,37,5,0,0,1,37,1,1,0,0,0,38,39,5,2,0,0,39,
        40,5,18,0,0,40,41,5,22,0,0,41,3,1,0,0,0,42,43,5,1,0,0,43,44,5,18,
        0,0,44,48,5,20,0,0,45,47,3,6,3,0,46,45,1,0,0,0,47,50,1,0,0,0,48,
        46,1,0,0,0,48,49,1,0,0,0,49,51,1,0,0,0,50,48,1,0,0,0,51,52,5,21,
        0,0,52,5,1,0,0,0,53,57,3,8,4,0,54,57,3,14,7,0,55,57,3,16,8,0,56,
        53,1,0,0,0,56,54,1,0,0,0,56,55,1,0,0,0,57,7,1,0,0,0,58,59,3,10,5,
        0,59,62,3,18,9,0,60,61,5,11,0,0,61,63,3,22,11,0,62,60,1,0,0,0,62,
        63,1,0,0,0,63,67,1,0,0,0,64,66,3,12,6,0,65,64,1,0,0,0,66,69,1,0,
        0,0,67,65,1,0,0,0,67,68,1,0,0,0,68,70,1,0,0,0,69,67,1,0,0,0,70,71,
        5,22,0,0,71,9,1,0,0,0,72,73,7,0,0,0,73,11,1,0,0,0,74,75,5,12,0,0,
        75,76,5,18,0,0,76,77,5,27,0,0,77,78,3,18,9,0,78,13,1,0,0,0,79,86,
        5,7,0,0,80,81,5,8,0,0,81,87,5,17,0,0,82,83,5,9,0,0,83,84,5,18,0,
        0,84,85,5,26,0,0,85,87,3,26,13,0,86,80,1,0,0,0,86,82,1,0,0,0,87,
        88,1,0,0,0,88,89,5,22,0,0,89,15,1,0,0,0,90,91,5,10,0,0,91,92,5,16,
        0,0,92,93,5,27,0,0,93,94,5,9,0,0,94,95,5,18,0,0,95,96,5,22,0,0,96,
        17,1,0,0,0,97,102,3,20,10,0,98,99,5,25,0,0,99,101,3,20,10,0,100,
        98,1,0,0,0,101,104,1,0,0,0,102,100,1,0,0,0,102,103,1,0,0,0,103,19,
        1,0,0,0,104,102,1,0,0,0,105,106,7,1,0,0,106,21,1,0,0,0,107,116,5,
        20,0,0,108,113,3,24,12,0,109,110,5,24,0,0,110,112,3,24,12,0,111,
        109,1,0,0,0,112,115,1,0,0,0,113,111,1,0,0,0,113,114,1,0,0,0,114,
        117,1,0,0,0,115,113,1,0,0,0,116,108,1,0,0,0,116,117,1,0,0,0,117,
        118,1,0,0,0,118,119,5,21,0,0,119,23,1,0,0,0,120,121,5,18,0,0,121,
        122,5,23,0,0,122,123,3,26,13,0,123,25,1,0,0,0,124,132,5,18,0,0,125,
        132,5,17,0,0,126,132,5,16,0,0,127,132,3,22,11,0,128,132,5,13,0,0,
        129,132,5,14,0,0,130,132,5,15,0,0,131,124,1,0,0,0,131,125,1,0,0,
        0,131,126,1,0,0,0,131,127,1,0,0,0,131,128,1,0,0,0,131,129,1,0,0,
        0,131,130,1,0,0,0,132,27,1,0,0,0,11,29,34,48,56,62,67,86,102,113,
        116,131
    ]

class ApiDslParser ( Parser ):

    grammarFileName = "ApiDsl.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'TEST'", "'BASE'", "'GET'", "'POST'", 
                     "'PUT'", "'DELETE'", "'EXPECT'", "'STATUS'", "'JSON'", 
                     "'SAVE'", "'BODY'", "'HEADER'", "'true'", "'false'", 
                     "'null'", "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'{'", "'}'", "';'", "':'", "','", "'+'", "'=='", "'='" ]

    symbolicNames = [ "<INVALID>", "TEST", "BASE", "GET", "POST", "PUT", 
                      "DELETE", "EXPECT", "STATUS", "JSON", "SAVE", "BODY", 
                      "HEADER", "TRUE", "FALSE", "NULL", "IDENT", "NUMBER", 
                      "STRING", "UNTERMINATED_STRING", "LBRACE", "RBRACE", 
                      "SEMI", "COLON", "COMMA", "PLUS", "EQ", "ASSIGN", 
                      "COMMENT", "WS" ]

    RULE_program = 0
    RULE_base = 1
    RULE_test = 2
    RULE_statement = 3
    RULE_request = 4
    RULE_method = 5
    RULE_header = 6
    RULE_assertion = 7
    RULE_save = 8
    RULE_expr = 9
    RULE_term = 10
    RULE_object = 11
    RULE_pair = 12
    RULE_value = 13

    ruleNames =  [ "program", "base", "test", "statement", "request", "method", 
                   "header", "assertion", "save", "expr", "term", "object", 
                   "pair", "value" ]

    EOF = Token.EOF
    TEST=1
    BASE=2
    GET=3
    POST=4
    PUT=5
    DELETE=6
    EXPECT=7
    STATUS=8
    JSON=9
    SAVE=10
    BODY=11
    HEADER=12
    TRUE=13
    FALSE=14
    NULL=15
    IDENT=16
    NUMBER=17
    STRING=18
    UNTERMINATED_STRING=19
    LBRACE=20
    RBRACE=21
    SEMI=22
    COLON=23
    COMMA=24
    PLUS=25
    EQ=26
    ASSIGN=27
    COMMENT=28
    WS=29

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(ApiDslParser.EOF, 0)

        def base(self):
            return self.getTypedRuleContext(ApiDslParser.BaseContext,0)


        def test(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ApiDslParser.TestContext)
            else:
                return self.getTypedRuleContext(ApiDslParser.TestContext,i)


        def getRuleIndex(self):
            return ApiDslParser.RULE_program

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = ApiDslParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 29
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==2:
                self.state = 28
                self.base()


            self.state = 32 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 31
                self.test()
                self.state = 34 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==1):
                    break

            self.state = 36
            self.match(ApiDslParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BaseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BASE(self):
            return self.getToken(ApiDslParser.BASE, 0)

        def STRING(self):
            return self.getToken(ApiDslParser.STRING, 0)

        def SEMI(self):
            return self.getToken(ApiDslParser.SEMI, 0)

        def getRuleIndex(self):
            return ApiDslParser.RULE_base

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBase" ):
                return visitor.visitBase(self)
            else:
                return visitor.visitChildren(self)




    def base(self):

        localctx = ApiDslParser.BaseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_base)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 38
            self.match(ApiDslParser.BASE)
            self.state = 39
            self.match(ApiDslParser.STRING)
            self.state = 40
            self.match(ApiDslParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TEST(self):
            return self.getToken(ApiDslParser.TEST, 0)

        def STRING(self):
            return self.getToken(ApiDslParser.STRING, 0)

        def LBRACE(self):
            return self.getToken(ApiDslParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(ApiDslParser.RBRACE, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ApiDslParser.StatementContext)
            else:
                return self.getTypedRuleContext(ApiDslParser.StatementContext,i)


        def getRuleIndex(self):
            return ApiDslParser.RULE_test

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTest" ):
                return visitor.visitTest(self)
            else:
                return visitor.visitChildren(self)




    def test(self):

        localctx = ApiDslParser.TestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_test)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 42
            self.match(ApiDslParser.TEST)
            self.state = 43
            self.match(ApiDslParser.STRING)
            self.state = 44
            self.match(ApiDslParser.LBRACE)
            self.state = 48
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 1272) != 0):
                self.state = 45
                self.statement()
                self.state = 50
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 51
            self.match(ApiDslParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def request(self):
            return self.getTypedRuleContext(ApiDslParser.RequestContext,0)


        def assertion(self):
            return self.getTypedRuleContext(ApiDslParser.AssertionContext,0)


        def save(self):
            return self.getTypedRuleContext(ApiDslParser.SaveContext,0)


        def getRuleIndex(self):
            return ApiDslParser.RULE_statement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = ApiDslParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_statement)
        try:
            self.state = 56
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [3, 4, 5, 6]:
                self.enterOuterAlt(localctx, 1)
                self.state = 53
                self.request()
                pass
            elif token in [7]:
                self.enterOuterAlt(localctx, 2)
                self.state = 54
                self.assertion()
                pass
            elif token in [10]:
                self.enterOuterAlt(localctx, 3)
                self.state = 55
                self.save()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RequestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def method(self):
            return self.getTypedRuleContext(ApiDslParser.MethodContext,0)


        def expr(self):
            return self.getTypedRuleContext(ApiDslParser.ExprContext,0)


        def SEMI(self):
            return self.getToken(ApiDslParser.SEMI, 0)

        def BODY(self):
            return self.getToken(ApiDslParser.BODY, 0)

        def object_(self):
            return self.getTypedRuleContext(ApiDslParser.ObjectContext,0)


        def header(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ApiDslParser.HeaderContext)
            else:
                return self.getTypedRuleContext(ApiDslParser.HeaderContext,i)


        def getRuleIndex(self):
            return ApiDslParser.RULE_request

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRequest" ):
                return visitor.visitRequest(self)
            else:
                return visitor.visitChildren(self)




    def request(self):

        localctx = ApiDslParser.RequestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_request)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 58
            self.method()
            self.state = 59
            self.expr()
            self.state = 62
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==11:
                self.state = 60
                self.match(ApiDslParser.BODY)
                self.state = 61
                self.object_()


            self.state = 67
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==12:
                self.state = 64
                self.header()
                self.state = 69
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 70
            self.match(ApiDslParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MethodContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def GET(self):
            return self.getToken(ApiDslParser.GET, 0)

        def POST(self):
            return self.getToken(ApiDslParser.POST, 0)

        def PUT(self):
            return self.getToken(ApiDslParser.PUT, 0)

        def DELETE(self):
            return self.getToken(ApiDslParser.DELETE, 0)

        def getRuleIndex(self):
            return ApiDslParser.RULE_method

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMethod" ):
                return visitor.visitMethod(self)
            else:
                return visitor.visitChildren(self)




    def method(self):

        localctx = ApiDslParser.MethodContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_method)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 72
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 120) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class HeaderContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def HEADER(self):
            return self.getToken(ApiDslParser.HEADER, 0)

        def STRING(self):
            return self.getToken(ApiDslParser.STRING, 0)

        def ASSIGN(self):
            return self.getToken(ApiDslParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(ApiDslParser.ExprContext,0)


        def getRuleIndex(self):
            return ApiDslParser.RULE_header

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitHeader" ):
                return visitor.visitHeader(self)
            else:
                return visitor.visitChildren(self)




    def header(self):

        localctx = ApiDslParser.HeaderContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_header)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 74
            self.match(ApiDslParser.HEADER)
            self.state = 75
            self.match(ApiDslParser.STRING)
            self.state = 76
            self.match(ApiDslParser.ASSIGN)
            self.state = 77
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssertionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EXPECT(self):
            return self.getToken(ApiDslParser.EXPECT, 0)

        def SEMI(self):
            return self.getToken(ApiDslParser.SEMI, 0)

        def STATUS(self):
            return self.getToken(ApiDslParser.STATUS, 0)

        def NUMBER(self):
            return self.getToken(ApiDslParser.NUMBER, 0)

        def JSON(self):
            return self.getToken(ApiDslParser.JSON, 0)

        def STRING(self):
            return self.getToken(ApiDslParser.STRING, 0)

        def EQ(self):
            return self.getToken(ApiDslParser.EQ, 0)

        def value(self):
            return self.getTypedRuleContext(ApiDslParser.ValueContext,0)


        def getRuleIndex(self):
            return ApiDslParser.RULE_assertion

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssertion" ):
                return visitor.visitAssertion(self)
            else:
                return visitor.visitChildren(self)




    def assertion(self):

        localctx = ApiDslParser.AssertionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_assertion)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 79
            self.match(ApiDslParser.EXPECT)
            self.state = 86
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [8]:
                self.state = 80
                self.match(ApiDslParser.STATUS)
                self.state = 81
                self.match(ApiDslParser.NUMBER)
                pass
            elif token in [9]:
                self.state = 82
                self.match(ApiDslParser.JSON)
                self.state = 83
                self.match(ApiDslParser.STRING)
                self.state = 84
                self.match(ApiDslParser.EQ)
                self.state = 85
                self.value()
                pass
            else:
                raise NoViableAltException(self)

            self.state = 88
            self.match(ApiDslParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SaveContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SAVE(self):
            return self.getToken(ApiDslParser.SAVE, 0)

        def IDENT(self):
            return self.getToken(ApiDslParser.IDENT, 0)

        def ASSIGN(self):
            return self.getToken(ApiDslParser.ASSIGN, 0)

        def JSON(self):
            return self.getToken(ApiDslParser.JSON, 0)

        def STRING(self):
            return self.getToken(ApiDslParser.STRING, 0)

        def SEMI(self):
            return self.getToken(ApiDslParser.SEMI, 0)

        def getRuleIndex(self):
            return ApiDslParser.RULE_save

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSave" ):
                return visitor.visitSave(self)
            else:
                return visitor.visitChildren(self)




    def save(self):

        localctx = ApiDslParser.SaveContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_save)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 90
            self.match(ApiDslParser.SAVE)
            self.state = 91
            self.match(ApiDslParser.IDENT)
            self.state = 92
            self.match(ApiDslParser.ASSIGN)
            self.state = 93
            self.match(ApiDslParser.JSON)
            self.state = 94
            self.match(ApiDslParser.STRING)
            self.state = 95
            self.match(ApiDslParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ApiDslParser.TermContext)
            else:
                return self.getTypedRuleContext(ApiDslParser.TermContext,i)


        def PLUS(self, i:int=None):
            if i is None:
                return self.getTokens(ApiDslParser.PLUS)
            else:
                return self.getToken(ApiDslParser.PLUS, i)

        def getRuleIndex(self):
            return ApiDslParser.RULE_expr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr" ):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)




    def expr(self):

        localctx = ApiDslParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 97
            self.term()
            self.state = 102
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==25:
                self.state = 98
                self.match(ApiDslParser.PLUS)
                self.state = 99
                self.term()
                self.state = 104
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TermContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(ApiDslParser.STRING, 0)

        def IDENT(self):
            return self.getToken(ApiDslParser.IDENT, 0)

        def getRuleIndex(self):
            return ApiDslParser.RULE_term

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTerm" ):
                return visitor.visitTerm(self)
            else:
                return visitor.visitChildren(self)




    def term(self):

        localctx = ApiDslParser.TermContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_term)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 105
            _la = self._input.LA(1)
            if not(_la==16 or _la==18):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ObjectContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACE(self):
            return self.getToken(ApiDslParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(ApiDslParser.RBRACE, 0)

        def pair(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ApiDslParser.PairContext)
            else:
                return self.getTypedRuleContext(ApiDslParser.PairContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(ApiDslParser.COMMA)
            else:
                return self.getToken(ApiDslParser.COMMA, i)

        def getRuleIndex(self):
            return ApiDslParser.RULE_object

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitObject" ):
                return visitor.visitObject(self)
            else:
                return visitor.visitChildren(self)




    def object_(self):

        localctx = ApiDslParser.ObjectContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_object)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 107
            self.match(ApiDslParser.LBRACE)
            self.state = 116
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==18:
                self.state = 108
                self.pair()
                self.state = 113
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==24:
                    self.state = 109
                    self.match(ApiDslParser.COMMA)
                    self.state = 110
                    self.pair()
                    self.state = 115
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 118
            self.match(ApiDslParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PairContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(ApiDslParser.STRING, 0)

        def COLON(self):
            return self.getToken(ApiDslParser.COLON, 0)

        def value(self):
            return self.getTypedRuleContext(ApiDslParser.ValueContext,0)


        def getRuleIndex(self):
            return ApiDslParser.RULE_pair

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPair" ):
                return visitor.visitPair(self)
            else:
                return visitor.visitChildren(self)




    def pair(self):

        localctx = ApiDslParser.PairContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_pair)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 120
            self.match(ApiDslParser.STRING)
            self.state = 121
            self.match(ApiDslParser.COLON)
            self.state = 122
            self.value()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(ApiDslParser.STRING, 0)

        def NUMBER(self):
            return self.getToken(ApiDslParser.NUMBER, 0)

        def IDENT(self):
            return self.getToken(ApiDslParser.IDENT, 0)

        def object_(self):
            return self.getTypedRuleContext(ApiDslParser.ObjectContext,0)


        def TRUE(self):
            return self.getToken(ApiDslParser.TRUE, 0)

        def FALSE(self):
            return self.getToken(ApiDslParser.FALSE, 0)

        def NULL(self):
            return self.getToken(ApiDslParser.NULL, 0)

        def getRuleIndex(self):
            return ApiDslParser.RULE_value

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValue" ):
                return visitor.visitValue(self)
            else:
                return visitor.visitChildren(self)




    def value(self):

        localctx = ApiDslParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_value)
        try:
            self.state = 131
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [18]:
                self.enterOuterAlt(localctx, 1)
                self.state = 124
                self.match(ApiDslParser.STRING)
                pass
            elif token in [17]:
                self.enterOuterAlt(localctx, 2)
                self.state = 125
                self.match(ApiDslParser.NUMBER)
                pass
            elif token in [16]:
                self.enterOuterAlt(localctx, 3)
                self.state = 126
                self.match(ApiDslParser.IDENT)
                pass
            elif token in [20]:
                self.enterOuterAlt(localctx, 4)
                self.state = 127
                self.object_()
                pass
            elif token in [13]:
                self.enterOuterAlt(localctx, 5)
                self.state = 128
                self.match(ApiDslParser.TRUE)
                pass
            elif token in [14]:
                self.enterOuterAlt(localctx, 6)
                self.state = 129
                self.match(ApiDslParser.FALSE)
                pass
            elif token in [15]:
                self.enterOuterAlt(localctx, 7)
                self.state = 130
                self.match(ApiDslParser.NULL)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





