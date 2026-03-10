"""Filter- und Validierungs-Hilfsfunktionen für die Reviews-API.

Dieses Modul kapselt die Logik zum Anwenden von Query-Parametern
auf ein `QuerySet` von `Review`-Objekten. Ziel ist eine saubere
Trennung und bessere Testbarkeit.
"""


def validate_list_params(params):
    """Validiere gängige Query-Parameter für die Review-Liste.

    Gibt ein Tuple (is_valid, error_message) zurück. Die Funktion
    wird aktuell nicht zwingend in den Views verwendet, ist aber als
    Hilfsfunktion verfügbar.
    """
    business_user_id = params.get("business_user_id")
    if business_user_id is not None:
        try:
            int(business_user_id)
        except (ValueError, TypeError):
            return False, "Invalid value for business_user_id."

    reviewer_id = params.get("reviewer_id")
    if reviewer_id is not None:
        try:
            int(reviewer_id)
        except (ValueError, TypeError):
            return False, "Invalid value for reviewer_id."

    ordering = params.get("ordering")
    if ordering is not None:
        key = ordering.lstrip("-")
        allowed = {"updated_at", "rating"}
        if key not in allowed:
            return False, "Invalid ordering key."

    return True, None


def apply_review_filters(qs, params):
    """Wendet Filter, Suche und Sortierung auf ein `Review`-QuerySet an.

    Unterstützt `business_user_id`, `reviewer_id` und eingeschränkte
    `ordering`-Schlüssel. Fehlerhafte Werte werden still ignoriert
    (gleiches Verhalten wie vorher in den Views).
    """
    business_user_id = params.get("business_user_id")
    if business_user_id:
        try:
            qs = qs.filter(business_user_id=int(business_user_id))
        except (ValueError, TypeError):
            pass

    reviewer_id = params.get("reviewer_id")
    if reviewer_id:
        try:
            qs = qs.filter(reviewer_id=int(reviewer_id))
        except (ValueError, TypeError):
            pass

    ordering = params.get("ordering")
    allowed = {"updated_at", "rating"}
    if ordering:
        key = ordering.lstrip("-")
        if key in allowed:
            qs = qs.order_by(ordering)
        else:
            qs = qs.order_by("-updated_at")
    else:
        qs = qs.order_by("-updated_at")

    return qs
