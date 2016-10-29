def is_valid_direction(direction):
    valid_directions = [-1,0,1]

    if int(direction) in valid_directions:
        return True
    else:
        return False