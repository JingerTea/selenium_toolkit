import random

class coordinate:
    def __init__(self, driver, element, frame=None):
        self.location = element.location
        x_offset = driver.execute_script("return window.scrollX")
        y_offset = driver.execute_script("return window.scrollY")
        self.location['x'] -= x_offset
        self.location['y'] -= y_offset
        self.size = element.size

        if frame:
            driver.switch_to.parent_frame()
            frame_location = frame.location
            x_offset = driver.execute_script("return window.scrollX")
            y_offset = driver.execute_script("return window.scrollY")
            self.location['x'] += frame_location['x']
            self.location['y'] += frame_location['y']
            self.location['x'] -= x_offset
            self.location['y'] -= y_offset
            driver.switch_to.frame(frame)


    def top_left(self):
        xy = self.location['x']
        return xy

    def top_right(self):
        xy = {
            'x': self.location['x'] + self.size['width'],
            'y': self.location['y']
        }
        return xy

    def bottom_left(self):
        xy = {
            'x': self.location['x'],
            'y': self.location['y'] + self.size['height']
        }
        return xy

    def bottom_right(self):
        xy = {
            'x': self.location['x'] + self.size['width'],
            'y': self.location['y'] + self.size['height']
        }
        return xy

    def center(self):
        x, y = self.location['x'], self.location['y']
        w, h = self.size['width'], self.size['height']
        wCenter = w / 2
        hCenter = h / 2

        xy = {
            'x': int(wCenter + x),
            'y': int(hCenter + y)
        }
        return xy

    def random(self):
        # Top left coordinate
        tl_xy = self.location

        # Bottom right coordinate
        br_xy = {
            'x': self.location['x'] + self.size['width'],
            'y': self.location['y'] + self.size['height']
        }

        # Random X Y within the element
        x = random.randint(tl_xy['x'], br_xy['x']) - 1
        y = random.randint(tl_xy['y'], br_xy['y']) - 1

        xy = {
            'x': x,
            'y': y
        }
        return xy