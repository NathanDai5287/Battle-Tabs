import numpy as np

def coord_to_array(coord):
    """converts one coordinate to array form

    Args:
        coord (tuple): (x, y)

    Returns:
        np.ndarray: [[x], [y]]
    """

    return np.array([[coord[0]], [coord[1]]])

def array_to_coords(array):
    """converts an array to tuple form

    Args:
        array (np.ndarray): [[a, b, c], [x, y, z]]

    Returns:
        tuple: [(a, x), (b, y), (c, z)]
    """

    return [tuple(coord) for coord in array.transpose()]
