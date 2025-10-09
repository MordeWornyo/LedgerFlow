from shared.events import ItemCreatedEvent, ItemUpdatedEvent
import pytest


def test_item_created_event_fields():
    """Tests that the ItemCreatedEvent is serialized correctly."""
    event = ItemCreatedEvent(item_id="123", name="Item", description="Desc")
    data = event.model_dump()

    assert data["item_id"] == "123"
    assert data["name"] == "Item"
    assert data["description"] == "Desc"


def test_item_updated_event_optional_description():
    """Tests that ItemUpdatedEvent supports an optional description."""
    event = ItemUpdatedEvent(item_id="999", name="NewName")
    assert event.description is None
    assert event.model_dump_json().startswith("{")
    assert "NewName" in event.model_dump_json()


def test_item_event_validation_error():
    """Tests that Pydantic raises an error if required fields are missing."""
    with pytest.raises(Exception):
        ItemCreatedEvent()  # type: ignore