
# Coderr – Backend API

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Coderr is a freelance marketplace platform where business users can offer services and customers can browse, order, and review them.

This repository contains the Django REST Framework backend API. It is designed to work together with the [coderr-frontend](https://github.com/your-org/coderr-frontend) – the matching HTML/CSS/JS frontend.

## Tech Stack

- Python 3.10+
- Django 6.0
- Django REST Framework 3.16
- SQLite (development)
- django-cors-headers, django-filter, python-decouple

## Features

- REST API for users, profiles, offers, orders, and reviews
- Management command to generate demo data
- Tests with pytest

## Quickstart (Local Development)

1. Create and activate a virtual environment:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # macOS / Linux
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Create environment file:

    ```bash
    cp .env.example .env
    # Set SECRET_KEY in .env (see below)
    ```

4. Migrate the database:


    ```bash
    python manage.py migrate
    ```

5. Start the development server:

    ```bash
    python manage.py runserver
    ```

    The API will be available at http://127.0.0.1:8000/api/

## .env – Important

Open `.env` and set at least `SECRET_KEY` and `DEBUG`. You can generate a secure key like this:

```python
import secrets
print(secrets.token_urlsafe(50))
```

## Testing

```bash
pytest
pytest --cov
```

## Key API Endpoints (Overview)

- **Authentication:**
    - `POST /api/registration/` — Create account
    - `POST /api/login/` — Obtain token

- **Profiles:**
    - `GET /api/profile/{pk}/` — View profile
    - `PATCH /api/profile/{pk}/` — Update own profile
    - `GET /api/profiles/business/` — Business profiles
    - `GET /api/profiles/customer/` — Customer profiles

- **Offers:**
    - `GET /api/offers/` — List offers (paginated)
    - `POST /api/offers/` — Create offer
    - `GET /api/offers/{id}/` — View offer
    - `PATCH /api/offers/{id}/` — Update offer
    - `DELETE /api/offers/{id}/` — Delete offer
    - `GET /api/offerdetails/{id}/` — Offer details

- **Orders:**
    - `GET /api/orders/` — List own orders
    - `POST /api/orders/` — Create order
    - `PATCH /api/orders/{id}/` — Change order status
    - `DELETE /api/orders/{id}/` — Delete order
    - `GET /api/order-count/{business_user_id}/` — In-progress count
    - `GET /api/completed-order-count/{business_user_id}/` — Completed count

- **Reviews:**
    - `GET /api/reviews/` — List reviews
    - `POST /api/reviews/` — Create review
    - `PATCH /api/reviews/{id}/` — Update review
    - `DELETE /api/reviews/{id}/` — Delete review

- **Platform Info:**
    - `GET /api/base-info/` — Statistics / platform info

For full details, see the respective apps: `authentication`, `profiles`, `offers`, `orders`, `reviews`.


## License

MIT

---

Feel free to add badges, a short architecture diagram, or further documentation as needed.

