# Generated from grammar/ApiDsl.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .ApiDslParser import ApiDslParser
else:
    from ApiDslParser import ApiDslParser

# This class defines a complete generic visitor for a parse tree produced by ApiDslParser.

class ApiDslVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ApiDslParser#program.
    def visitProgram(self, ctx:ApiDslParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiDslParser#base.
    def visitBase(self, ctx:ApiDslParser.BaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiDslParser#test.
    def visitTest(self, ctx:ApiDslParser.TestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiDslParser#statement.
    def visitStatement(self, ctx:ApiDslParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiDslParser#request.
    def visitRequest(self, ctx:ApiDslParser.RequestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiDslParser#method.
    def visitMethod(self, ctx:ApiDslParser.MethodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiDslParser#header.
    def visitHeader(self, ctx:ApiDslParser.HeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiDslParser#assertion.
    def visitAssertion(self, ctx:ApiDslParser.AssertionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiDslParser#save.
    def visitSave(self, ctx:ApiDslParser.SaveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiDslParser#expr.
    def visitExpr(self, ctx:ApiDslParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiDslParser#term.
    def visitTerm(self, ctx:ApiDslParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiDslParser#object.
    def visitObject(self, ctx:ApiDslParser.ObjectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiDslParser#pair.
    def visitPair(self, ctx:ApiDslParser.PairContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ApiDslParser#value.
    def visitValue(self, ctx:ApiDslParser.ValueContext):
        return self.visitChildren(ctx)



del ApiDslParser