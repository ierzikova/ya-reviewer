class Size:
    SMALL = 'small'
    BIG = 'big'

def determine_size(height: int, width: int, length: int) -> str:
    height = max(height, 1)
    width = max(width, 1)
    length = max(length, 1)

    dimensions_sum = height + width + length

    if 0 < dimensions_sum < 30:
        return Size.SMALL
    else:
        return Size.BIG