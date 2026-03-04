Coderr – Backend API

Python Django DRF License

🌐 English · Deutsch

Coderr is a freelance marketplace platform where business users can offer services and customers can browse, order and review them.

This repository contains the Django REST Framework backend API. It is designed to work together with the coderr-frontend – the matching HTML/CSS/JS frontend.
Tech Stack

    Python 3.13
    Django 6.0
    Django REST Framework 3.16
    SQLite (development)
    django-cors-headers, django-filter, python-decouple

Setup
Prerequisites

Before you start, make sure the following are installed on your machine:

    **Coderr — Backend API (Django REST Framework)**

    Ein einfaches, lokales Backend für den Freelance‑Marktplatz "Coderr". Diese API gehört zur Matching-Frontend-Anwendung und stellt die Endpunkte für Benutzer, Profile, Angebote, Bestellungen und Bewertungen bereit.

    **Technologie**
    - Python 3.10+
    - Django 6
    - Django REST Framework
    - SQLite (Entwicklung)
    - django-cors-headers, django-filter, python-decouple

    **Kurz: Was enthält dieses Repo?**
    - REST-API für Nutzer, Profile, Offers, Orders und Reviews
    - Management‑Command zum Erzeugen von Demo‑Daten
    - Tests mit pytest

    **Schnellstart (lokal)**
    1. Virtuelle Umgebung erstellen und aktivieren:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # macOS / Linux
    ```

    2. Abhängigkeiten installieren:

    ```bash
    pip install -r requirements.txt
    ```

    3. Umgebungsdatei anlegen:

    ```bash
    cp .env.example .env
    # SECRET_KEY in .env setzen (siehe weiter unten)
    ```

    4. Datenbank migrieren:

    ```bash
    python manage.py migrate
    ```

    5. (Optional) Demo-Daten laden:

    ```bash
    python manage.py create_demo_data
    ```

    6. Entwicklungsserver starten:

    ```bash
    python manage.py runserver
    ```

    Die API ist dann unter http://127.0.0.1:8000/api/ erreichbar.

    **.env – wichtig**
    Öffne `.env` und setze mindestens `SECRET_KEY` und `DEBUG`. Einen sicheren Schlüssel erzeugst du z. B. so:

    ```python
    import secrets
    print(secrets.token_urlsafe(50))
    ```

    **Tests**

    ```bash
    pytest
    pytest --cov
    ```

    **Demo-Benutzer**
    Nach Ausführung von `create_demo_data` werden (u. a.) folgende Accounts angelegt:

    - kevin / asdasd24 (business)
    - anna / asdasd24 (business)
    - andrey / asdasd (customer)
    - lisa / asdasd24 (customer)

    Die Kommandozeile ist idempotent — mehrfaches Ausführen erzeugt keine Duplikate.

    **Wichtige API-Endpunkte (Kurzüberblick)**

    - Authentifizierung:
        - `POST /api/registration/` — Account erstellen
        - `POST /api/login/` — Token erhalten

    - Profile:
        - `GET /api/profile/{pk}/` — Profil anzeigen
        - `PATCH /api/profile/{pk}/` — Eigenes Profil aktualisieren
        - `GET /api/profiles/business/` — Business‑Profile
        - `GET /api/profiles/customer/` — Customer‑Profile

    - Offers:
        - `GET /api/offers/` — Angebote (paginiert)
        - `POST /api/offers/` — Angebot erstellen
        - `GET /api/offers/{id}/` — Angebot anzeigen
        - `PATCH /api/offers/{id}/` — Angebot aktualisieren
        - `DELETE /api/offers/{id}/` — Angebot löschen
        - `GET /api/offerdetails/{id}/` — Angebots‑Detail

    - Orders:
        - `GET /api/orders/` — Eigene Bestellungen
        - `POST /api/orders/` — Bestellung erstellen
        - `PATCH /api/orders/{id}/` — Bestellstatus ändern
        - `DELETE /api/orders/{id}/` — Bestellung löschen
        - `GET /api/order-count/{business_user_id}/` — In‑Progress Count
        - `GET /api/completed-order-count/{business_user_id}/` — Completed Count

    - Reviews:
        - `GET /api/reviews/` — Reviews auflisten
        - `POST /api/reviews/` — Review erstellen
        - `PATCH /api/reviews/{id}/` — Review aktualisieren
        - `DELETE /api/reviews/{id}/` — Review löschen

    - Platform Info:
        - `GET /api/base-info/` — Statistiken / Plattform‑Infos

    Für vollständige Details siehe die jeweiligen Apps unter `authentication`, `profiles`, `offers`, `orders`, `reviews`.

    **Related Projects**

    - Frontend: `coderr-frontend` — das passende HTML/CSS/JS‑Frontend für diese API.

    **Lizenz**

    MIT

    ---

    Wenn du möchtest, kann ich noch Badges, ein kurzes Architekturdiagramm oder eine englische Version hinzufügen.

