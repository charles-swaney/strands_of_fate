import random


def compute_stat_bonus(base_aptitude: int, class_aptitude: float) -> int:
    """
    Compute the random stat growth based on aptitude. 

    Args:
        base_aptitude (int): the adventurer's aptitude (expected range:
            0 to 10)
        class_aptitude (float): the aptitude associated with the adventurer's class
            (expected range: -2 to 2)   
    
    Returns:
        int: either 0, +1, or -1, representing an aptitude-based
            perturbation to the adventurer's stat growth.

    Example Probabilities:
        Note that a base aptitude of 5 is considered "average" as reflected in
        the expectation of the bonus equalling zero.

        Aptitude = -2: -1 (67.5%), 0 (22.5%), +1 (10%)
        Aptitude = 1: -1 (53.72%), 0 (29.85%), +1 (16.43%)
        Aptitude = 5: -1 (25%), 0 (50%), +1 (25%)
        Aptitude = 8: -1 (15.27%), 0 (37.57%), +1 (47.16%)
        Aptitude = 10: -1 (8.1%), 0 (24.51%), +1 (67.39%)
        Aptitude = 12: -1 (2.03%), 0 (7.98%), +1 (90%)
    """
    aptitude = base_aptitude + class_aptitude

    if aptitude >= 5:
        threshold_for_plus_one = 1/4 + ((aptitude - 5) ** 1.27) * 0.0549
        threshold_for_plus_zero = 2/3 + ((aptitude - 5) ** 1.27) * 0.011
    else:
        threshold_for_plus_one = 0.15 / 7 * aptitude + 1/7
        threshold_for_plus_zero = 0.5 - (5 - aptitude) / 28
    
    check_plus_one = random.random()
    
    if check_plus_one < threshold_for_plus_one:
        return 1
    
    else:
        check_plus_zero = random.random()
        if check_plus_zero < threshold_for_plus_zero:
            return 0
        else:
            return -1
