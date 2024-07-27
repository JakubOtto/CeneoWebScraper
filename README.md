# CeneoWebScraper

CeneoWebScraper to narzędzie do web scraping'u, które pozwala na automatyczne pobieranie danych o produktach z serwisu Ceneo.pl. Projekt został stworzony w celu zebrania informacji o produktach, recenzjach i ocenach, które mogą być wykorzystane do analizy danych. Aplikacja wykorzystuje Flask i Jinja do prezentacji wyników w przeglądarce internetowej.

## Spis treści

- [Instalacja](#instalacja)
- [Użycie](#użycie)
- [Funkcje](#funkcje)
- [Technologie](#technologie)
- [Autor](#autor)
- [Licencja](#licencja)

## Instalacja

Aby zainstalować i uruchomić projekt lokalnie, wykonaj poniższe kroki:

1. Sklonuj repozytorium:
    ```bash
    git clone https://github.com/JakubOtto/CeneoWebScraper.git
    ```
2. Przejdź do katalogu projektu:
    ```bash
    cd CeneoWebScraper
    ```
3. Utwórz i aktywuj wirtualne środowisko (opcjonalne, ale zalecane):
    ```bash
    python -m venv venv
    source venv/bin/activate  # dla systemów Unix/macOS
    .\venv\Scripts\activate  # dla systemu Windows
    ```
4. Zainstaluj wymagane zależności:
    ```bash
    pip install -r requirements.txt
    ```

## Użycie

Aby uruchomić web scraper i przeglądać wyniki w przeglądarce, wykonaj poniższe kroki:

1. Skonfiguruj parametry scrapowania w pliku `config.py` (jeśli jest dostępny).
2. Uruchom aplikację Flask:
    ```bash
    flask run
    ```
3. Otwórz przeglądarkę i przejdź do `http://localhost:5000`, aby przeglądać wyniki scrapowania.

## Funkcje

- **Pobieranie danych o produktach z Ceneo.pl**: Skrypt automatycznie zbiera informacje o produktach, takie jak nazwa, cena, liczba recenzji i średnia ocena.
- **Zbieranie recenzji i ocen produktów**: Narzędzie przechodzi przez strony z recenzjami, zbierając szczegółowe opinie użytkowników.
- **Przechodzenie między stronami**: Skrypt automatycznie przechodzi między stronami wyników, pobierając dane z wielu stron produktu.
- **Wyświetlanie danych**: Wyniki są zapisywane w formacie CSV lub JSON, co pozwala na łatwą analizę i przetwarzanie danych.
- **Tworzenie wykresów**: Narzędzie generuje wykresy przedstawiające zebrane dane, takie jak rozkład ocen czy liczba recenzji w czasie. Wykresy są zapisywane jako pliki PNG.
- **Interfejs webowy**: Dane są prezentowane w przeglądarce za pomocą Flask i Jinja, umożliwiając przeglądanie i analizę danych w wygodny sposób.

## Technologie

- **Python**: Język programowania używany do implementacji narzędzia.
- **BeautifulSoup**: Biblioteka do parsowania HTML i ekstrakcji danych z kodu HTML.
- **Requests**: Biblioteka do wykonywania zapytań HTTP.
- **Pandas**: Biblioteka do manipulacji danymi i analizy danych.
- **Matplotlib/Seaborn**: Biblioteki do tworzenia wykresów i wizualizacji danych.
- **Flask**: Mikroframework webowy do budowania interfejsu użytkownika.
- **Jinja**: Silnik szablonów używany do renderowania stron HTML.

## Autor

Projekt został stworzony przez [Jakub Otto](https://github.com/JakubOtto).

## Licencja

Ten projekt jest licencjonowany na licencji MIT - zobacz plik [LICENSE](LICENSE) po więcej szczegółów.
