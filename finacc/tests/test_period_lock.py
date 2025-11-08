import pytest
from finacc.models.period import PeriodLock
from finacc.posting.engine import post_entry, PeriodLockedError


@pytest.mark.django_db
def test_lock_blocks_posting(company, sample_entry):
    PeriodLock.objects.create(company=company, through_date=sample_entry.date)
    with pytest.raises(PeriodLockedError):
         post_entry(sample_entry)