from datetime import date
from uuid import uuid4

import pytest

from domain.entities.deal import Deal, DealStage
from domain.errors import InvalidStageTransition, ValidationError


def test_move_stage_allows_forward_flow():
    deal = Deal(customer_id=uuid4(), title="A", amount=100.0, stage=DealStage.NEW)
    deal.move_to_stage(DealStage.CONTACTED)
    assert deal.stage == DealStage.CONTACTED


def test_move_stage_disallows_from_terminal():
    deal = Deal(customer_id=uuid4(), title="A", amount=100.0, stage=DealStage.WON)
    with pytest.raises(InvalidStageTransition):
        deal.move_to_stage(DealStage.PROPOSAL)


def test_invalid_stage_rejected():
    with pytest.raises(ValidationError):
        Deal(customer_id=uuid4(), title="A", amount=100.0, stage="UNKNOWN")
