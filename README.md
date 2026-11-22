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

1. **Lekser** — tekst → tokeny (z numerem linii i kolumny).
2. **Parser** — tokeny → drzewo AST, metoda zstępująca rekurencyjna, gramatyka LL(1).
3. **Analiza semantyczna** — tablica symboli, wykrywanie błędów znaczeniowych.
4. **Generowanie kodu** — AST → plik z testami pytest.

## Uruchomienie

Wymagany Python 3.11+.

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m pytest
```

Docelowo:

```
python -m apidsl compile examples/login.api -o out.py
python -m apidsl run examples/login.api
python -m apidsl compile examples/login.api --tokens
python -m apidsl compile examples/login.api --ast
```

## Struktura

```
apidsl/        kod kompilatora
examples/      przykładowe programy .api (poprawne i z błędami)
mock_server/   testowy serwer API do uruchamiania przykładów offline
tests/         testy jednostkowe każdego etapu
docs/          dokumentacja (gramatyka, automaty, FIRST/FOLLOW, reguły semantyczne)
```

## Plan prac

- [ ] 1. Tokeny i lekser + testy
- [ ] 2. AST i parser + testy
- [ ] 3. Analiza semantyczna + testy
- [ ] 4. Generowanie kodu, CLI, mock serwer, przykłady
- [ ] 5. Dokumentacja

## Praca w zespole

- Każde zadanie na osobnej gałęzi: `git checkout -b lexer`.
- Przed wysłaniem: `python -m pytest` musi przechodzić.
- Zmiany do `main` przez Pull Request, drugi członek zespołu przegląda.
