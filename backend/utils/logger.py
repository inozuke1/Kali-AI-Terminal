import logging
import sys
from datetime import datetime

def setup_logger(name: str) -> logging.Logger:
    """Setup logger with colored output and proper formatting"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        
        # Custom formatter with colors and emojis
        formatter = ColoredFormatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
            datefmt='%H:%M:%S'
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        # File handler for persistent logs
        fh = logging.FileHandler('logs/kali_ai_terminal.log', mode='a')
        fh.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(file_formatter)
        logger.addHandler(fh)

    return logger

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors and emojis for better readability"""
    
    # Color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
    }
    
    EMOJIS = {
        'DEBUG': '[DEBUG]',
        'INFO': '[INFO]',
        'WARNING': '[WARN]',
        'ERROR': '[ERROR]',
        'CRITICAL': '[CRIT]',
    }
    
    RESET = '\033[0m'

    def format(self, record):
        # Add color and emoji
        log_color = self.COLORS.get(record.levelname, '')
        emoji = self.EMOJIS.get(record.levelname, '')
        reset = self.RESET
        
        # Format the message
        record.levelname = f"{emoji} {record.levelname}"
        formatted = super().format(record)
        
        return f"{log_color}{formatted}{reset}"
