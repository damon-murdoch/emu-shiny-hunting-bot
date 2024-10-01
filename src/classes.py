# Macro Class
# For simple macros
class Macro:
    def __init__(self, action):

        # Function to execute
        self.action = action

    def is_macro(self):
        return True

    def run(self, game, method):
        self.action(game, method)


# Bot Class
# For complex macros
class Bot(Macro):
    def __init__(self, action):
        super().__init__(action)

    def is_macro(self):
        return False

    def run(self, game, method, window=None, autostart=None):
        self.action(window, game, method, autostart)
