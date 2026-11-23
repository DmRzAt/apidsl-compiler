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

**Pełna dokumentacja:** [`docs/dokumentacja.md`](docs/dokumentacja.md) — gramatyka formalna
G = (N, T, P, S), tabela tokenów i automaty DFA, EBNF, zbiory FIRST/FOLLOW (dowód LL(1)),
reguły semantyczne, schemat kompilatora i przykład kompilacji krok po kroku.

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

## Użycie

Najpierw w osobnym terminalu uruchom testowy serwer API (nasłuchuje tylko lokalnie,
`http://localhost:8000`):

```
python -m mock_server
```

Następnie:

```
python -m apidsl run examples/login.api                  # kompilacja + uruchomienie testów
python -m apidsl compile examples/login.api -o out.py    # zapis wygenerowanego kodu do pliku
python -m apidsl compile examples/login.api              # wygenerowany kod na ekran
python -m apidsl compile examples/login.api --tokens     # tokeny (wynik leksera)
python -m apidsl compile examples/login.api --ast        # drzewo AST (wynik parsera)
```

Błędy kompilacji (kod wyjścia 1):

```
python -m apidsl compile examples/errors/lexical.api
python -m apidsl compile examples/errors/syntax.api
python -m apidsl compile examples/errors/semantic.api
```

Gdy test nie przechodzi, komunikat wskazuje linię w pliku `.api`, np.
`line 9: expected JSON "role" == "guest", got "admin"` (`python -m apidsl run examples/failing.api`).

### Przykłady

| Plik | Co pokazuje |
|---|---|
| `examples/login.api` | logowanie, zapis tokenu, użycie go w nagłówku |
| `examples/users.api` | przechodzenie po endpointach: lista → szczegóły → tworzenie → zmiana → usunięcie |
| `examples/failing.api` | czytelne komunikaty o niepowodzeniu testu |
| `examples/errors/*.api` | błąd leksykalny, składniowy i semantyczne |

### Mock serwer

| Endpoint | Opis |
|---|---|
| `POST /login` | `{"user": "admin", "pass": "123"}` → `200 {"token": ...}`, inaczej `401` |
| `GET /me` | wymaga `Authorization: Bearer <token>` → `{"user": "admin", "role": "admin"}` |
| `GET /users` | `{"items": [...], "count": n}` |
| `POST /users` | `{"name": "..."}` → `201` z nowym `id` |
| `GET /users/<id>` | użytkownik lub `404` |
| `PUT /users/<id>` | zmiana nazwy |
| `DELETE /users/<id>` | `204` lub `404` |

## Wygenerowany kod

Każdy `TEST` staje się osobną funkcją pytest. Wszystkie wartości z programu trafiają do kodu
jako bezpieczne literały Pythona (`ascii()`), nigdy przez sklejanie tekstu. Funkcje pomocnicze
(`send`, `json_path`, `expect_status`, `expect_json`) są dołączane do pliku z `apidsl/runtime.py`,
więc wygenerowany plik działa samodzielnie. Każde zapytanie ma `timeout=10`.

```python
def test_login_flow():
    response = send('POST', resolve_url(BASE, '/login'), 4, body={'user': 'admin', 'pass': '123'})
    expect_status(response, 200, 5)
    var_token = json_path(response, 'token', 6)
    response = send('GET', resolve_url(BASE, '/me'), 8, headers={'Authorization': 'Bearer ' + text(var_token)})
    expect_status(response, 200, 9)
    expect_json(response, 'role', 'admin', 10)
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
- [x] 2. AST (visitor) + testy
- [x] 3. Analiza semantyczna + testy
- [x] 4. Generowanie kodu, CLI, mock serwer, przykłady
- [x] 5. Dokumentacja

## Praca w zespole

- Każde zadanie na osobnej gałęzi: `git checkout -b lexer`.
- Przed wysłaniem: `python -m pytest` musi przechodzić.
- Zmiany do `main` przez Pull Request, drugi członek zespołu przegląda.
