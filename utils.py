def values2grid(values):
    """Convert grid into a dict of {square: char} with '123456789' for empties.

    Parameters
    ----------
    grid(string)
        a string representing a game grid.
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value,
            then the value will be '123456789'.
    """
    grid = []
    row = []
    for idx in range(len(values)):
        value = values[idx]
        if value == '.':
            row.append('123456789')
        else:
            row.append(value)
        if len(row) == 9:
            grid.append(row)
            row = []
    return grid


def debug_display(sudoku):
    """Display the values as a 2-D grid.

    Parameters
    ----------
        values(dict): The game in dictionary form
    """
    for row in sudoku.get_values():
        row_str = ""
        for item in row:
            row_str += item + " "*(10 - len(item))
        print(row_str)
    print("")