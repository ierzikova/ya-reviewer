from delivery_cost import calculate_delivery_cost, MAX_DELIVERY_DISTANCE_FOR_FRAGILE_ITEMS
import pytest

class TestDeliveryCost:

    def test_value_error_when_fragile_delivery_distance_more_than_max(self):
        with pytest.raises(AssertionError, match=r"Cant deliver fragile items.*"):
            calculate_delivery_cost(
                MAX_DELIVERY_DISTANCE_FOR_FRAGILE_ITEMS + 1,
                'small',
                fragile=True
            )
