# src/utils/logger.py
import threading
from datetime import datetime

class ConsoleLogger:
    _lock = threading.Lock()
    
    # ANSI color codes
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

    # Set to False to hide technical details (LLM load, paths, etc.)
    VERBOSE = False 

    @staticmethod
    def _print(text):
        """Thread-safe print to avoid line mixing"""
        with ConsoleLogger._lock:
            print(text)

    @staticmethod
    def info(msg):
        """General information (e.g., Current step)"""
        ConsoleLogger._print(f"{ConsoleLogger.CYAN}ℹ️  {msg}{ConsoleLogger.ENDC}")

    @staticmethod
    def success(msg):
        """Success (e.g., Document found)"""
        ConsoleLogger._print(f"{ConsoleLogger.GREEN}✅ {msg}{ConsoleLogger.ENDC}")

    @staticmethod
    def warning(msg):
        """Warning (e.g., Empty PDF, rejected)"""
        ConsoleLogger._print(f"{ConsoleLogger.WARNING}⚠️  {msg}{ConsoleLogger.ENDC}")

    @staticmethod
    def error(msg):
        """Critical error"""
        ConsoleLogger._print(f"{ConsoleLogger.FAIL}❌ {msg}{ConsoleLogger.ENDC}")

    @staticmethod
    def section(msg):
        """Major section headers"""
        ConsoleLogger._print(f"\n{ConsoleLogger.HEADER}{ConsoleLogger.BOLD}=== {msg.upper()} ==={ConsoleLogger.ENDC}")

    @staticmethod
    def debug(msg):
        """Technical details (displayed only if VERBOSE = True)"""
        if ConsoleLogger.VERBOSE:
            ConsoleLogger._print(f"\033[90m⚙️  [DEBUG] {msg}{ConsoleLogger.ENDC}")

# Global instance easy to import
logger = ConsoleLogger()