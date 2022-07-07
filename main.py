from app.delivery_cost import calculate_delivery_cost
from app.size import Size

if __name__ == '__main__':
    print('hello! lets count delivery cost')

    print(calculate_delivery_cost(1, Size.SMALL, fragile=True, delivery_load_rate=1.2))
    print(calculate_delivery_cost(30, Size.SMALL, fragile=False))
    print(calculate_delivery_cost(150, Size.SMALL, fragile=False, delivery_load_rate=1.2))
    print(calculate_delivery_cost(150, Size.SMALL, fragile=False, delivery_load_rate=1.2))