import random

class LoadState:
    NORMAL = 'normal'
    HEIGHTENED = 'heightened'
    HIGH = 'high'
    OVERLOADED = 'overloaded'

def get_current_delivery_load() -> str:
    '''
    Returns current delivery load state.
    Might be some logic here...
    '''
    return random.choice([
        LoadState.NORMAL,
        LoadState.HEIGHTENED,
        LoadState.HIGH,
        LoadState.OVERLOADED
    ])

