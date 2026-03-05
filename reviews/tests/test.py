"""Tests for the reviews API – Happy Path matching the teacher's Postman tests."""

import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from reviews.models import Review


@pytest.fixture
def business_user(db):
    """Create a business user with matching profile."""
    user = User.objects.create_user(username="business", password="pass1234")
    profile = user.profile
    profile.type = "business"
    profile.save()
    return user


@pytest.fixture
def customer_user(db):
    """Create a customer user with matching profile."""
    user = User.objects.create_user(username="customer", password="pass1234")
    profile = user.profile
    profile.type = "customer"
    profile.save()
    return user


@pytest.fixture
def customer_client(customer_user):
    """APIClient authenticated as customer user via token."""
    token, _ = Token.objects.get_or_create(user=customer_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return client


@pytest.fixture
def existing_review(db, business_user, customer_user):
    """A pre-existing review used for retrieve/update/delete tests."""
    return Review.objects.create(
        business_user=business_user,
        reviewer=customer_user,
        rating=2,
        description="Nicht so gut.",
    )



class TestReviewRetrieve:
    """Tests matching the teacher's Postman 'Happy Path / Reviews / reviews' suite."""

    def test_all_fields_in_response(self, customer_client, existing_review):
        """ID should be a number and all required fields must be present."""
        resp = customer_client.get(f"/api/reviews/{existing_review.id}/")
        assert resp.status_code == 200, resp.content

        data = resp.data
        assert "id" in data, "Field 'id' missing"
        assert isinstance(data["id"], int), f"'id' should be int, got {type(data['id'])}"

    def test_created_at_exists_in_response(self, customer_client, existing_review):
        """created_at must be present in response."""
        resp = customer_client.get(f"/api/reviews/{existing_review.id}/")
        assert resp.status_code == 200
        assert "created_at" in resp.data, "'created_at' is missing"
        assert resp.data["created_at"] is not None

    def test_updated_at_exists_in_response(self, customer_client, existing_review):
        """updated_at must be present in response."""
        resp = customer_client.get(f"/api/reviews/{existing_review.id}/")
        assert resp.status_code == 200
        assert "updated_at" in resp.data, "'updated_at' is missing"
        assert resp.data["updated_at"] is not None

    def test_business_user_matches_expected_value(self, customer_client, existing_review, business_user):
        """business_user in response must match the actual business user id."""
        resp = customer_client.get(f"/api/reviews/{existing_review.id}/")
        assert resp.status_code == 200
        assert resp.data["business_user"] == business_user.id, (
            f"Expected business_user={business_user.id}, got {resp.data.get('business_user')}"
        )

    def test_reviewer_matches_expected_value(self, customer_client, existing_review, customer_user):
        """reviewer in response must match the actual reviewer id."""
        resp = customer_client.get(f"/api/reviews/{existing_review.id}/")
        assert resp.status_code == 200
        assert resp.data["reviewer"] == customer_user.id, (
            f"Expected reviewer={customer_user.id}, got {resp.data.get('reviewer')}"
        )



class TestReviewCreate:
    """Tests for creating a review."""

    def test_create_review_returns_201(self, customer_client, business_user):
        """POST should return 201 and full review data including id."""
        payload = {
            "business_user": business_user.id,
            "rating": 4,
            "description": "Sehr gut!",
        }
        resp = customer_client.post("/api/reviews/", payload, format="json")
        assert resp.status_code == 201, resp.content

        data = resp.data
        assert isinstance(data["id"], int)
        assert data["business_user"] == business_user.id
        assert "created_at" in data
        assert "updated_at" in data



class TestReviewUpdate:
    """Tests for updating a review – response must also contain all fields."""

    def test_patch_returns_full_representation(self, customer_client, existing_review, business_user, customer_user):
        """PATCH response must contain id, created_at, updated_at, business_user, reviewer."""
        payload = {"rating": 5, "description": "Jetzt doch super!"}
        resp = customer_client.patch(
            f"/api/reviews/{existing_review.id}/", payload, format="json"
        )
        assert resp.status_code == 200, resp.content

        data = resp.data
        assert isinstance(data["id"], int)
        assert "created_at" in data
        assert "updated_at" in data
        assert data["business_user"] == business_user.id
        assert data["reviewer"] == customer_user.id
        assert data["rating"] == 5