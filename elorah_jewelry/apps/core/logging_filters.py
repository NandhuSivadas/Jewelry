import logging
import re

class SensitiveDataFilter(logging.Filter):
    def __init__(self, name=""):
        super().__init__(name)
        # Regex patterns to redact
        self.patterns = [
            (re.compile(r'(password=)([^&\'"]+)'), r'\1***'),
            (re.compile(r'(secret=)([^&\'"]+)'), r'\1***'),
            (re.compile(r'(token=)([^&\'"]+)'), r'\1***'),
            (re.compile(r'(authorization:\s*)([^\s\'"]+)'), r'\1***'),
            # Basic CC pattern (very rough)
            (re.compile(r'\b(?:\d[ -]*?){13,16}\b'), r'***'),
        ]

    def filter(self, record):
        if isinstance(record.msg, str):
            for pattern, replacement in self.patterns:
                record.msg = pattern.sub(replacement, record.msg)
        return True
