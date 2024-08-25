class TextFormatter:
    def __init__(self, text, domain):
        self.text = text
        self.domain = domain

    def format_text(self):
        raise NotImplementedError("Subclasses should implement this method.")