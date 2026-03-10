
from django.db.models import Q


def validate_list_params(params):
    """Validate query parameters used by the offers list endpoint.

    Returns a tuple ``(is_valid, error_message)`` where ``is_valid`` is
    a boolean and ``error_message`` is a string suitable for sending as
    a JSON ``detail`` message when validation fails.
    """
    min_price = params.get("min_price")
    if min_price is not None:
        try:
            float(min_price)
        except (ValueError, TypeError):
            return False, "Invalid value for min_price."

    max_delivery = params.get("max_delivery_time")
    if max_delivery is not None:
        try:
            int(max_delivery)
        except (ValueError, TypeError):
            return False, "Invalid value for max_delivery_time."

    creator_id = params.get("creator_id")
    if creator_id is not None:
        try:
            int(creator_id)
        except (ValueError, TypeError):
            return False, "Invalid value for creator_id."

    return True, None


def apply_offer_filters(qs, params):
    """Apply filtering, search and ordering to an `Offer` queryset.

    The function mirrors the filtering behaviour previously implemented
    in the view: it supports filtering by `creator_id`, `min_price`,
    `max_delivery_time`, a simple text `search` and limited
    `ordering` keys. The function always returns a queryset.
    """
    creator_id = params.get("creator_id")
    if creator_id:
        try:
            qs = qs.filter(user_id=int(creator_id))
        except (ValueError, TypeError):
            pass

    min_price = params.get("min_price")
    if min_price:
        try:
            qs = qs.filter(min_price__gte=float(min_price))
        except (ValueError, TypeError):
            pass

    max_delivery = params.get("max_delivery_time")
    if max_delivery:
        try:
            qs = qs.filter(min_delivery_time__lte=int(max_delivery))
        except (ValueError, TypeError):
            pass

    search = params.get("search")
    if search:
        qs = qs.filter(Q(title__icontains=search) | Q(description__icontains=search))

    ordering = params.get("ordering")
    allowed = {"updated_at", "min_price"}
    if ordering:
        key = ordering.lstrip("-")
        if key in allowed:
            qs = qs.order_by(ordering)
        else:
            qs = qs.order_by("-updated_at")
    else:
        qs = qs.order_by("-updated_at")

    return qs
