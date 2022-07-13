from constants import Size, LoadState

class Config:
    MAX_DELIVERY_DISTANCE = 1000
    MAX_DELIVERY_DISTANCE_FOR_FRAGILE_ITEMS = 30

    MIN_DELIVERY_COST = 400

    SIZE_COST = {
        Size.BIG: 200,
        Size.SMALL: 100
    }
    FRAGILE_DELIVERY_COST = 300

    DELIVERY_LOAD_RATES = {
        LoadState.NORMAL: 1,
        LoadState.HEIGHTENED: 1.2,
        LoadState.HIGH: 1.4,
        LoadState.OVERLOADED: 1.6
    }