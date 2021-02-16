from All_Functions import open_image


def zoom_out(self):
    if self.z - 1 < 0:
        return None
    self.z -= 1
    open_image(self.ll, self.z)


def zoom_in(self):
    if self.z + 1 > 17:
        return None
    self.z += 1
    open_image(self.ll, self.z)
