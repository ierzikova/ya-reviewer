from delivery_cost import calculate_delivery_cost, _get_size_cost, _get_distance_cost
from size import Size
from config import Config
import pytest
from random import randint


class TestDeliveryCost:

    def test_calculate_delivery_cost_returns_min_cost_when_cost_is_less(self, mocker):
        mocker.patch('delivery_cost._get_distance_cost', return_value=1)
        mocker.patch('delivery_cost._get_size_cost', return_value=1)
        cost = calculate_delivery_cost(1, Size.SMALL, fragile=False)
        assert cost == Config.MIN_DELIVERY_COST, 'Should not return cost less than minimum delivery cost'


    def test_calculate_delivery_cost_increase_cost_when_fragile_item(self):
        distance = Config.MAX_DELIVERY_DISTANCE_FOR_FRAGILE_ITEMS - 1
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
        assert cost_fragile - cost_not_fragile == Config.FRAGILE_DELIVERY_COST, \
            'Should add fragile delivery cost to total cost'

    def test_calculate_delivery_cost_raises_error_when_fragile_delivery_distance_more_than_max(self):
        with pytest.raises(AssertionError, match=r"Cant deliver fragile items.*"):
            calculate_delivery_cost(
                Config.MAX_DELIVERY_DISTANCE_FOR_FRAGILE_ITEMS + 1,
                Size.SMALL,
                fragile=True
            )
        with pytest.raises(AssertionError, match=r"Cant deliver fragile items.*"):
            calculate_delivery_cost(
                Config.MAX_DELIVERY_DISTANCE_FOR_FRAGILE_ITEMS + 1,
                Size.BIG,
                fragile=True
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
        assert cost_high_delivery_rate / cost_regular_delivery_rate == high_delivery_load_rate, \
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

    def test_calculate_delivery_cost_raises_error_when_delivery_load_rate_less_than_min(self):
        with pytest.raises(AssertionError, match=r"Delivery load rate can't be less than.*"):
            calculate_delivery_cost(
                randint(1, Config.MAX_DELIVERY_DISTANCE),
                Size.SMALL,
                fragile=False,
                delivery_load_rate=Config.MIN_DELIVERY_LOAD_RATE * 0.99
            )

class TestGetDistanceCost:
    params = [
        (0, 50),
        (2, 50),
        (3, 100),
        (10, 100),
        (11, 200),
        (30, 200),
        (31, 300),
        (Config.MAX_DELIVERY_DISTANCE, 300)
    ]

    @pytest.mark.parametrize(
        "distance, expected_distance_cost",
        params
    )
    def test_get_distance_cost_values(self, distance, expected_distance_cost):
        distance_cost = _get_distance_cost(distance)
        assert distance_cost == expected_distance_cost, \
            'Distance cost should be equal expected: values were hardcoded :( '

    def test_get_distance_cost_raises_error_when_distance_more_than_max(self):
        with pytest.raises(ValueError, match=r"Delivery distance is more than max.*"):
            _get_distance_cost(Config.MAX_DELIVERY_DISTANCE + 1)

    def test_get_distance_cost_raises_error_when_distance_is_negative(self):
        with pytest.raises(ValueError, match=r"Distance cant be negative.*"):
            _get_distance_cost(-1)


class TestGetSizeCost:
    params = [
        (Size.SMALL, 100),
        (Size.BIG, 200)
    ]

    @pytest.mark.parametrize(
        "size, expected_size_cost",
        params
    )
    def test_get_size_cost_values(self, size, expected_size_cost):
        size_cost = _get_size_cost(size)
        assert size_cost == expected_size_cost, \
            'Sizecost should be equal expected: values were hardcoded :( '

    def test_get_size_cost_raises_error_when_unexpected_size(self):
        with pytest.raises(ValueError, match=r"Unexpected size.*"):
            _get_size_cost('unexisting_size')

    def test_get_distance_cost_raises_error_when_distance_is_negative(self):
        with pytest.raises(ValueError, match=r"Distance cant be negative.*"):
            _get_distance_cost(-1)
