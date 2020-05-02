class Util:
    # TODO: make static
    def calculate_center(corners):
        return [(corners[0][0] + corners[3][0]) / 2, (corners[0][1] + corners[3][1]) / 2]


def calculate_center(corners):
    return [(corners[0][0] + corners[3][0]) / 2, (corners[0][1] + corners[3][1]) / 2]
