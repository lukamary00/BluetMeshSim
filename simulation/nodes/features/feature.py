class Feature:
    """
    Base class for all features
    """
    def __init__(self, device):
        super().__init__()
        self.device = device
    
    def on_receive(self, frame):
        """
        Called on frame receive
        """