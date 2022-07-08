from delivery_cost import calculate_delivery_cost, MAX_DELIVERY_DISTANCE_FOR_FRAGILE_ITEMS
from delivery_cost import MAX_DELIVERY_DISTANCE, FRAGILE_DELIVERY_COST, MIN_DELIVERY_LOAD_RATE, MIN_DELIVERY_COST
from size import Size
import pytest
from random import randint


class TestDeliveryCost:

    def test_calculate_delivery_cost_raises_error_when_fragile_delivery_distance_more_than_max(self):
        with pytest.raises(AssertionError, match=r"Cant deliver fragile items.*"):
            calculate_delivery_cost(
                MAX_DELIVERY_DISTANCE_FOR_FRAGILE_ITEMS + 1,
                Size.SMALL,
                fragile=True
            )
        with pytest.raises(AssertionError, match=r"Cant deliver fragile items.*"):
            calculate_delivery_cost(
                MAX_DELIVERY_DISTANCE_FOR_FRAGILE_ITEMS + 1,
                Size.BIG,
                fragile=True
            )

    def test_calculate_delivery_cost_increase_cost_when_fragile_item(self):
        distance = MAX_DELIVERY_DISTANCE_FOR_FRAGILE_ITEMS - 1
        size = Size.BIG
        cost_fragile = calculate_delivery_cost(
            distance,
            size,
            fragile=True
        )
        cost_not_fragile = calculate_delivery_cost(
            distance,
            size,
            fragile=False
        )
        assert cost_fragile - cost_not_fragile == FRAGILE_DELIVERY_COST, \
            'Should add fragile delivery cost to total cost'


    def test_calculate_delivery_cost_raises_error_when_delivery_load_rate_less_than_min(self):
        with pytest.raises(AssertionError, match=r"Delivery load rate can't be less than.*"):
            calculate_delivery_cost(
                randint(1, MAX_DELIVERY_DISTANCE),
                Size.SMALL,
                fragile=False,
                delivery_load_rate=MIN_DELIVERY_LOAD_RATE * 0.99
            )


    def test_calculate_delivery_cost_increases_cost_with_delivery_load_rate(self):
        distance = 30
        size = Size.BIG
        high_delivery_load_rate = 1.5
        cost_regular_delivery_rate = calculate_delivery_cost(
            distance,
            size,
            fragile=False
        )
        cost_high_delivery_rate = calculate_delivery_cost(
            distance,
            size,
            fragile=False,
            delivery_load_rate=high_delivery_load_rate
        )
        assert cost_high_delivery_rate/cost_regular_delivery_rate == high_delivery_load_rate, \
            'Should multiply delivery cost to delivery load rate'

    def test_calculate_delivery_cost_default_delivery_load_rate_is_1(self):
        distance = 25
        size = Size.SMALL
        cost_default_delivery_rate = calculate_delivery_cost(
            distance,
            size,
            fragile=False
        )
        cost_expected_delivery_rate = calculate_delivery_cost(
            distance,
            size,
            fragile=False,
            delivery_load_rate=1
        )
        assert cost_default_delivery_rate == cost_expected_delivery_rate, \
            'Default delivery load rate should be 1'


    def test_calculate_delivery_cost_returns_min_cost_when_cost_is_less(self, mocker):
        mocker.patch('delivery_cost._get_distance_cost', return_value=1)
        mocker.patch('delivery_cost._get_size_cost', return_value=1)
        cost = calculate_delivery_cost(1, Size.SMALL, fragile=False)
        assert cost == MIN_DELIVERY_COST, 'Should not return cost less than minimum delivery cost'


