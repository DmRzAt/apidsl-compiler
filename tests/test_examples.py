from pathlib import Path

import pytest

from apidsl import cli
from apidsl.compiler import CompilationFailed, check

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"
DEMO_BASE = 'BASE "http://localhost:8000";'
VALID = ["login.api", "users.api", "failing.api"]


def errors_of(name: str) -> list[str]:
    with pytest.raises(CompilationFailed) as caught:
        check((EXAMPLES / name).read_text(encoding="utf-8"))
    return [f"{e.line}:{e.col}: {e.kind}: {e.message}" for e in caught.value.errors]


def against(mock_api: str, name: str, tmp_path: Path) -> Path:
    source = (EXAMPLES / name).read_text(encoding="utf-8")
    assert DEMO_BASE in source
    target = tmp_path / name
    target.write_text(source.replace(DEMO_BASE, f'BASE "{mock_api}";'), encoding="utf-8")
    return target


@pytest.mark.parametrize("name", VALID)
def test_valid_examples_compile(name):
    check((EXAMPLES / name).read_text(encoding="utf-8"))


def test_lexical_example():
    assert errors_of("errors/lexical.api") == ["4:9: LexicalError: unterminated string"]


def test_syntax_example():
    assert errors_of("errors/syntax.api") == [
        "5:5: SyntaxError: expected one of 'BODY', 'HEADER', ';', got 'EXPECT'"
    ]


def test_semantic_example():
    assert errors_of("errors/semantic.api") == [
        "2:5: SemanticError: EXPECT STATUS before any request in test 'Semantic errors'",
        "3:9: SemanticError: relative path '/users/' requires BASE",
        "3:21: SemanticError: variable 'user_id' is used before SAVE",
        "4:5: SemanticError: status code 700 is outside 100-599",
        "7:1: SemanticError: duplicate test name 'Semantic errors' (first defined at line 1)",
        "7:1: SemanticError: test 'Semantic errors' is empty",
    ]


@pytest.mark.parametrize("name, test_count", [("login.api", 3), ("users.api", 2)])
def test_run_passes_against_mock_server(mock_api, tmp_path, capfd, name, test_count):
    exit_code = cli.main(["run", str(against(mock_api, name, tmp_path))])
    output = capfd.readouterr().out

    assert exit_code == 0, output
    assert f"{test_count} passed" in output


def test_run_reports_dsl_lines_of_failures(mock_api, tmp_path, capfd):
    exit_code = cli.main(["run", str(against(mock_api, "failing.api", tmp_path))])
    output = capfd.readouterr().out

    assert exit_code == 1
    assert 'line 9: expected JSON "role" == "guest", got "admin"' in output
    assert "line 14: expected status 200, got 404" in output
    assert "2 failed" in output


def test_run_reports_unreachable_server(tmp_path, capfd):
    source = tmp_path / "down.api"
    source.write_text('TEST "down" { GET "http://127.0.0.1:9/x"; }', encoding="utf-8")

    assert cli.main(["run", str(source)]) == 1
    assert "line 1: GET http://127.0.0.1:9/x failed:" in capfd.readouterr().out
