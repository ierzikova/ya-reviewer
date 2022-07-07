MIN_DELIVERY_COST = 400
MIN_DELIVERY_LOAD_RATE = 1
MAX_DELIVERY_DISTANCE_FOR_FRAGILE_ITEMS = 30

SIZE_COST = {
    'big': 200,
    'small': 100
}

def _get_distance_cost(distance: int) -> int:
    if distance < 2:
        return 50
    elif 2 < distance <= 10:
        return 100
    elif 10 < distance <= 30:
        return 200
    else:
        return 300


def _get_size_cost(size: str) -> int:
    try:
        return SIZE_COST[size]
    except KeyError:
        raise ValueError(f'Unexpected size: {size}')


def calculate_delivery_cost(distance: int, size: str,
                            fragile: bool, delivery_load_rate: float = 1) -> float:
    """
    Calculates delivery cost.
    Arguments:
        distance: distance in km
        size: 'small' | 'big'
    Returns:
        The sum of the two integer arguments
    """
    cost = _get_distance_cost(distance) + _get_size_cost(size)

    if fragile:
        assert distance < MAX_DELIVERY_DISTANCE_FOR_FRAGILE_ITEMS, \
            f'Cant deliver fragile items more than {MAX_DELIVERY_DISTANCE_FOR_FRAGILE_ITEMS} km'
        cost += 300

    assert delivery_load_rate >= MIN_DELIVERY_LOAD_RATE, \
        f"Delivery load rate can't be less than {MIN_DELIVERY_LOAD_RATE}: Yandex should make money"

    delivery_load_rate = max(1, delivery_load_rate)

    return max(cost * delivery_load_rate, MIN_DELIVERY_COST)