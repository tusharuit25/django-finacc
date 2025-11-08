import pytest
from decimal import Decimal
from finacc.models.company import Company
from finacc.models.accounts import Account
from finacc.posting.rules import create_simple_entry
from finacc.posting.engine import post_entry


@pytest.mark.django_db
def test_balanced_posting():
    c = Company.objects.create(name="ACME")
    cash = Account.objects.create(company=c, code="1000", name="Cash", kind="asset", normal_balance="debit")
    eq = Account.objects.create(company=c, code="3000", name="Equity", kind="equity", normal_balance="credit")
    je = create_simple_entry(c, date="2025-11-08", currency="INR", memo="capital", lines=[
    {"account": cash, "debit": Decimal("1000.00"), "credit": Decimal("0.00")},
    {"account": eq, "debit": Decimal("0.00"), "credit": Decimal("1000.00")},
    ])
    posted = post_entry(je)
    assert posted.is_posted is True