

class MicroObject:
    latin_name = ""
    common_name = ""
    appearance = 0
    has_button = False
    hotkey = None

    instances = []

    def __init__(self, latin_name, common_name, appearance=0, has_button=False, hotkey=None):
        self.latin_name = latin_name
        self.common_name = common_name
        self.appearance = appearance
        self.has_button = has_button
        self.hotkey = hotkey
        MicroObject.instances.append(self)

    @classmethod
    def get_all_instances(cls):
        return cls.instances

    def __str__(self):
        return f"{self.common_name} ({self.latin_name}) found: {self.appearance}x times"

    def found(self):
        self.appearance += 1

    def set_appearance(self, appearance):
        self.appearance = appearance

    def get_appearance(self):
        return self.appearance

    def set_latin_name(self, latin_name):
        self.latin_name = latin_name

    def get_latin_name(self):
        return self.latin_name

    def set_common_name(self, common_name):
        self.common_name = common_name

    def get_common_name(self):
        return self.common_name

    def set_has_button(self, has_button):
        self.has_button = has_button

    def get_has_button(self):
        return self.has_button

    def set_hotkey(self, hotkey):
        self.hotkey = hotkey

    def get_hotkey(self):
        return self.hotkey

    def to_dict(self):
        return {
            'latin_name': self.latin_name,
            'common_name': self.common_name,
            'has_button': self.has_button,
            'hotkey': self.hotkey
        }
