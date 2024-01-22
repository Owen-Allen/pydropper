from scipy.spatial import KDTree
from webcolors import CSS3_HEX_TO_NAMES, hex_to_rgb

class ColorConverter:
    def __init__(self):
        self.names, self.rgb_values = self._initialize_color_data()

    def _initialize_color_data(self):
        names = []
        rgb_values = []
        for color_hex, color_name in CSS3_HEX_TO_NAMES.items():
            names.append(color_name)
            rgb_values.append(hex_to_rgb(color_hex))
        return names, rgb_values

    def convert_rgb_to_names(self, rgb_tuple):
        kdt_db = KDTree(self.rgb_values)
        distance, index = kdt_db.query(rgb_tuple)
        return self.names[index]

    def rgb_to_hex(self, r, g, b):
        return "#{:02x}{:02x}{:02x}".format(r, g, b)
