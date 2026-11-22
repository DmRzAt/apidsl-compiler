# apidsl — kompilator języka do testowania API

Projekt na przedmiot **Języki formalne i kompilatory**.
Temat: *Testowanie API i przechodzenie po endpointach*.

Własny język DSL do opisywania testów API oraz kompilator, który tłumaczy programy `.api`
na testy w Pythonie (pytest).

```
BASE "http://localhost:8000";

TEST "Login flow" {
    POST "/login" BODY { "user": "admin", "pass": "123" };
    EXPECT STATUS 200;
    SAVE token = JSON "token";

    GET "/me" HEADER "Authorization" = "Bearer " + token;
    EXPECT STATUS 200;
    EXPECT JSON "role" == "admin";
}
```

## Etapy kompilatora

Lekser i parser są generowane przez **ANTLR 4** z gramatyki [`grammar/ApiDsl.g4`](grammar/ApiDsl.g4).

1. **Lekser** (ANTLR) — tekst → tokeny (z numerem linii i kolumny).
2. **Parser** (ANTLR) — tokeny → drzewo rozbioru; gramatyka jest klasy LL(1).
3. **Budowa AST** — visitor zamienia drzewo rozbioru na własne drzewo AST.
4. **Analiza semantyczna** — tablica symboli, wykrywanie błędów znaczeniowych.
5. **Generowanie kodu** — AST → plik z testami pytest.

Błędy ANTLR są przechwytywane i zgłaszane w jednolitym formacie:
`plik.api:5:12: SyntaxError: expected ';', got 'GET'`.

## Uruchomienie

Wymagany Python 3.11+.

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m pytest
```

Wygenerowany kod parsera (`apidsl/generated/`) jest w repozytorium, więc do uruchomienia
**nie jest potrzebna Java**.

### Zmiana gramatyki

Po edycji `grammar/ApiDsl.g4` trzeba ponownie wygenerować parser (wymagana Java 11+):

```
pip install -r requirements-dev.txt
antlr4 -v 4.13.2 -Dlanguage=Python3 -visitor -no-listener -Xexact-output-dir -o apidsl/generated grammar/ApiDsl.g4
```

W PyCharm / IntelliJ warto zainstalować wtyczkę **ANTLR v4** — podświetlanie składni
i podgląd drzewa rozbioru (*ANTLR Preview*).

Docelowo:

```
python -m apidsl compile examples/login.api -o out.py
python -m apidsl run examples/login.api
python -m apidsl compile examples/login.api --tokens
python -m apidsl compile examples/login.api --ast
```

## Struktura

```
grammar/       gramatyka ANTLR (ApiDsl.g4)
apidsl/        kod kompilatora
  generated/   lekser i parser wygenerowane przez ANTLR (nie edytować ręcznie)
examples/      przykładowe programy .api (poprawne i z błędami)
mock_server/   testowy serwer API do uruchamiania przykładów offline
tests/         testy jednostkowe każdego etapu
docs/          dokumentacja (gramatyka, automaty, FIRST/FOLLOW, reguły semantyczne)
```

## Plan prac

- [x] 1. Gramatyka ANTLR, lekser i parser + testy błędów leksykalnych i składniowych
- [ ] 2. AST (visitor) + testy
- [ ] 3. Analiza semantyczna + testy
- [ ] 4. Generowanie kodu, CLI, mock serwer, przykłady
- [ ] 5. Dokumentacja

## Praca w zespole

- Każde zadanie na osobnej gałęzi: `git checkout -b lexer`.
- Przed wysłaniem: `python -m pytest` musi przechodzić.
- Zmiany do `main` przez Pull Request, drugi członek zespołu przegląda.
