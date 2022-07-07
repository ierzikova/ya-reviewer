from app.delivery_cost import calculate_delivery_cost
from app.size import SIZE_BIG, SIZE_SMALL

if __name__ == '__main__':
    print('hello! lets count delivery cost')

    print(calculate_delivery_cost(1, SIZE_BIG, fragile=True, delivery_load_rate=1.2))
    print(calculate_delivery_cost(30, SIZE_SMALL, fragile=False))
    print(calculate_delivery_cost(150, SIZE_BIG, fragile=False, delivery_load_rate=1.2))
    print(calculate_delivery_cost(150, SIZE_BIG, fragile=False, delivery_load_rate=1.2))