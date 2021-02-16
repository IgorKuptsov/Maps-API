from All_Functions import open_image


# если нажаты pgup и pgdown
def zoom_out(z):
    if z - 1 < 0:
        return None
    open_image()


def zoom_in(z):
    if z + 1 > 17:
        return None
    open_image()
