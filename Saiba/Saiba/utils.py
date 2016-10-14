def is_valid_direction(direction):
    direction = int(direction)
    valid_directions = [-1,0,1]

    if direction in valid_directions:
        return True
    else:
        return False