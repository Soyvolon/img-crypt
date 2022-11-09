class ImageProcessingError(Exception):
    """An error raised when something went wrong with image processing"""
    def __init__(self, message: str = None):
        self.message = message
    
    def __str__(self) -> str:
        return self.message