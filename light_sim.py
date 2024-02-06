class SmartLight:
    def __init__(self):
        self.state = "OFF"  # Possible states: "ON", "OFF"
        self.brightness = 0  # Brightness level: 0 to 100

    def set_state(self, state):
        self.state = state

    def set_brightness(self, brightness):
        self.brightness = brightness

    def get_status(self):
        return f"Light State: {self.state}, Brightness: {self.brightness}"
