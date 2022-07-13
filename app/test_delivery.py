import pytest
from delivery import calculate_delivery_cost, _get_size_cost, _get_distance_cost, _get_delivery_load_rate
from item import Item
from delivery import LoadState
from config import Config


class TestDeliveryCost:

    @pytest.mark.parametrize(
        'distance, item, delivery_load',
        [
            (2, Item.random(), LoadState.NORMAL),
            (45, Item.random(), LoadState.HIGH),
            (132, Item.random(), LoadState.OVERLOADED),
        ]
    )
    def test_calculate_delivery_cost_calculates_cost_with_size_cost_and_load(self, distance, item, delivery_load):
        cost = calculate_delivery_cost(distance, item, delivery_load=delivery_load)
        expected_cost = (_get_size_cost(item.size) + _get_distance_cost(distance)) * _get_delivery_load_rate(delivery_load)
        if expected_cost <= Config.MIN_DELIVERY_COST:
            expected_cost = Config.MIN_DELIVERY_COST

        assert cost == expected_cost, 'Cost should depend of item size, cost and delivery_load'

    def test_calculate_delivery_cost_returns_min_cost_when_cost_is_less(self, mocker):
        mocker.patch('delivery._get_distance_cost', return_value=1)
        mocker.patch('delivery._get_size_cost', return_value=1)
        mocker.patch('delivery._get_delivery_load_rate', return_value=1)
        cost = calculate_delivery_cost(1, Item.random(), delivery_load=LoadState.NORMAL)
        assert cost == Config.MIN_DELIVERY_COST, 'Should not return cost less than minimum delivery cost'


    def test_calculate_delivery_cost_increase_cost_when_fragile_item(self):
        distance = Config.MAX_DELIVERY_DISTANCE_FOR_FRAGILE_ITEMS - 1
        item_fragile = Item.random(fragile=True)
        item_not_fragile = Item.random(fragile=False)

        cost_fragile = calculate_delivery_cost(
            distance,
            item_fragile,
            delivery_load = LoadState.NORMAL
        )
        cost_not_fragile = calculate_delivery_cost(
            distance,
            item_not_fragile,
            delivery_load = LoadState.NORMAL
        )
        assert cost_fragile - cost_not_fragile == Config.FRAGILE_DELIVERY_COST, \
            'Should add fragile delivery cost to total cost'

    def test_calculate_delivery_cost_raises_error_when_fragile_delivery_distance_more_than_max(self):
        with pytest.raises(AssertionError, match=r"Cant deliver fragile items.*"):
            calculate_delivery_cost(
                Config.MAX_DELIVERY_DISTANCE_FOR_FRAGILE_ITEMS + 1,
                Item.random(fragile=True),
                delivery_load = LoadState.NORMAL
            )

    @pytest.mark.parametrize(
        "load_state, rate",
        Config.DELIVERY_LOAD_RATES.items()
    )
    def test_calculate_delivery_cost_increases_cost_with_delivery_load_rate(self, load_state, rate):
        distance = 30
        item = Item.random()

        cost_normal_delivery_load = calculate_delivery_cost(
            distance,
            item,
            delivery_load=LoadState.NORMAL
        )
        cost_with_delivery_load = calculate_delivery_cost(
            distance,
            item,
            delivery_load=load_state
        )
        assert cost_with_delivery_load / cost_normal_delivery_load == rate, \
            'Should multiply delivery cost to delivery load rate'


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

    @pytest.mark.parametrize(
        "size, expected_size_cost",
        Config.SIZE_COST.items()
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


class TestGetDeliveryLoadRate:

    @pytest.mark.parametrize(
        "load, rate_expected",
        Config.DELIVERY_LOAD_RATES.items()
    )
    def test_get_size_cost_values(self, load, rate_expected):
        rate = _get_delivery_load_rate(load)

        assert rate == rate_expected, \
            'Load Rate should be equal expected: values were hardcoded :( '

    def test_get_delivery_load_rate_raises_error_when_unexpected_load_state(self):
        with pytest.raises(ValueError, match=r"Unexpected load state: .*"):
            _get_delivery_load_rate('unexisting_load_state')
