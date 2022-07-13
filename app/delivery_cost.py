from config import Config
from item import Item


def _get_size_cost(size: str) -> int:
    """
    Calculates part of delivery cost for different item sizes.
    Arguments:
        size: size.Size: 'small' | 'big'
    Returns:
        Part of delivery cost for size
    """
    if size not in Config.SIZE_COST.keys():
        raise ValueError(f'Unexpected size: {size}')
    return Config.SIZE_COST.get(size)


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

def _get_delivery_load_rate(load: str) -> float:
    """
    Returns delivery load rate.
    Arguments:
        load: size.Size: 'small' | 'big'
    Returns:
        Delivery load rate
    """
    if load not in Config.DELIVERY_LOAD_RATES.keys():
        raise ValueError(f'Unexpected load state: {load}')
    return Config.DELIVERY_LOAD_RATES.get(load)


def calculate_delivery_cost(distance: int, item: Item, delivery_load: str) -> float:
    """
    Calculates delivery cost.
    Arguments:
        distance: distance in km
        item: item.Item
    Returns:
        Calculated delivery cost
    """
    cost = _get_distance_cost(distance) + _get_size_cost(item.size)

    if item.fragile:
        assert distance < Config.MAX_DELIVERY_DISTANCE_FOR_FRAGILE_ITEMS, \
            f'Cant deliver fragile items more than {Config.MAX_DELIVERY_DISTANCE_FOR_FRAGILE_ITEMS} km'
        cost += Config.FRAGILE_DELIVERY_COST

    delivery_load_rate = _get_delivery_load_rate(delivery_load)

    return max(cost * delivery_load_rate, Config.MIN_DELIVERY_COST)