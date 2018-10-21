class Item:
    def __init__(self, stack=1, use_function=None, targeting=False, targeting_message=None, **kwargs):
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.stack = stack
        self.function_kwargs = kwargs
