from config import Config
from size import Size

SIZE_COST = {
    Size.BIG: 200,
    Size.SMALL: 100
}


def _get_size_cost(size: str) -> int:
    """
    Calculates part of delivery cost for different item sizes.
    Arguments:
        size: size.Size: 'small' | 'big'
    Returns:
        Part of delivery cost for size
    """

    try:
        return SIZE_COST[size]
    except KeyError:
        raise ValueError(f'Unexpected size: {size}')


def _get_distance_cost(distance: int) -> int:
    """
    Calculates part of delivery cost for different distances.
    Arguments:
        distance: kilometers to deliver
    Returns:
        Part of delivery cost for distance
    """
    if distance < 0:
        raise ValueError(f'Distance cant be negative: {distance} < 0')
    elif 0 <= distance <= 2:
        return 50
    elif 2 < distance <= 10:
        return 100
    elif 10 < distance <= 30:
        return 200
    elif 30 < distance <= Config.MAX_DELIVERY_DISTANCE:
        return 300
    else:
        raise ValueError(f'Delivery distance is more than max: {distance} > {Config.MAX_DELIVERY_DISTANCE}')


def calculate_delivery_cost(distance: int, size: str,
                            fragile: bool, delivery_load_rate: float = 1) -> float:
    """
    Calculates delivery cost.
    Arguments:
        distance: distance in km
        size: size.Size: 'small' | 'big'
    Returns:
        Calculated delivery cost
    """
    cost = _get_distance_cost(distance) + _get_size_cost(size)

    if fragile:
        assert distance < Config.MAX_DELIVERY_DISTANCE_FOR_FRAGILE_ITEMS, \
            f'Cant deliver fragile items more than {Config.MAX_DELIVERY_DISTANCE_FOR_FRAGILE_ITEMS} km'
        cost += Config.FRAGILE_DELIVERY_COST

    assert delivery_load_rate >= Config.MIN_DELIVERY_LOAD_RATE, \
        f"Delivery load rate can't be less than {Config.MIN_DELIVERY_LOAD_RATE}: Yandex should make money"

    return max(cost * delivery_load_rate, Config.MIN_DELIVERY_COST)