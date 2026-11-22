from antlr4 import ParserRuleContext
from antlr4.tree.Tree import TerminalNode

from apidsl import ast
from apidsl.generated.ApiDslParser import ApiDslParser
from apidsl.generated.ApiDslVisitor import ApiDslVisitor
from apidsl.lexer import decode_string


def position(ctx: ParserRuleContext) -> dict[str, int]:
    return {"line": ctx.start.line, "col": ctx.start.column + 1}


def string(terminal: TerminalNode) -> str:
    return decode_string(terminal.getSymbol())


class AstBuilder(ApiDslVisitor):
    def visitProgram(self, ctx: ApiDslParser.ProgramContext) -> ast.Program:
        base = self.visit(ctx.base()) if ctx.base() is not None else None
        tests = tuple(self.visit(test) for test in ctx.test())
        return ast.Program(base, tests, **position(ctx))

    def visitBase(self, ctx: ApiDslParser.BaseContext) -> ast.Base:
        return ast.Base(string(ctx.STRING()), **position(ctx))

    def visitTest(self, ctx: ApiDslParser.TestContext) -> ast.Test:
        statements = tuple(self.visit(statement) for statement in ctx.statement())
        return ast.Test(string(ctx.STRING()), statements, **position(ctx))

    def visitStatement(self, ctx: ApiDslParser.StatementContext) -> ast.Statement:
        return self.visit(ctx.getChild(0))

    def visitRequest(self, ctx: ApiDslParser.RequestContext) -> ast.Request:
        method = ast.Method(ctx.method().getText())
        body = self.visit(ctx.object_()) if ctx.object_() is not None else None
        headers = tuple(self.visit(header) for header in ctx.header())
        return ast.Request(method, self.visit(ctx.expr()), body, headers, **position(ctx))

    def visitHeader(self, ctx: ApiDslParser.HeaderContext) -> ast.Header:
        return ast.Header(string(ctx.STRING()), self.visit(ctx.expr()), **position(ctx))

    def visitAssertion(self, ctx: ApiDslParser.AssertionContext) -> ast.Statement:
        if ctx.STATUS() is not None:
            return ast.ExpectStatus(int(ctx.NUMBER().getText()), **position(ctx))
        return ast.ExpectJson(string(ctx.STRING()), self.visit(ctx.value()), **position(ctx))

    def visitSave(self, ctx: ApiDslParser.SaveContext) -> ast.Save:
        return ast.Save(ctx.IDENT().getText(), string(ctx.STRING()), **position(ctx))

    def visitExpr(self, ctx: ApiDslParser.ExprContext) -> ast.Expr:
        return ast.Expr(tuple(self.visit(term) for term in ctx.term()), **position(ctx))

    def visitTerm(self, ctx: ApiDslParser.TermContext) -> ast.Term:
        if ctx.STRING() is not None:
            return ast.StringLiteral(string(ctx.STRING()), **position(ctx))
        return ast.VarRef(ctx.IDENT().getText(), **position(ctx))

    def visitObject(self, ctx: ApiDslParser.ObjectContext) -> ast.ObjectLiteral:
        return ast.ObjectLiteral(tuple(self.visit(pair) for pair in ctx.pair()), **position(ctx))

    def visitPair(self, ctx: ApiDslParser.PairContext) -> ast.Pair:
        return ast.Pair(string(ctx.STRING()), self.visit(ctx.value()), **position(ctx))

    def visitValue(self, ctx: ApiDslParser.ValueContext) -> ast.Value:
        if ctx.object_() is not None:
            return self.visit(ctx.object_())
        token = ctx.start
        where = position(ctx)
        match token.type:
            case ApiDslParser.STRING:
                return ast.StringLiteral(decode_string(token), **where)
            case ApiDslParser.NUMBER:
                return ast.NumberLiteral(int(token.text), **where)
            case ApiDslParser.IDENT:
                return ast.VarRef(token.text, **where)
            case ApiDslParser.TRUE | ApiDslParser.FALSE:
                return ast.BoolLiteral(token.type == ApiDslParser.TRUE, **where)
            case ApiDslParser.NULL:
                return ast.NullLiteral(**where)
        raise ValueError(f"unsupported value token {token.text!r}")
