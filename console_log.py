import logging

SUCCESS_LEVEL_NUM = 25

logging.addLevelName(SUCCESS_LEVEL_NUM, "SUCCESS")

def success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS_LEVEL_NUM):
        self._log(SUCCESS_LEVEL_NUM, message, args, **kwargs)

logging.Logger.success = success

class ColorFormatter(logging.Formatter):
    class Color:
        COLOR_RED = "\033[91m"
        COLOR_GREEN = "\033[92m"
        COLOR_YELLOW = "\033[93m"
        COLOR_BLUE = "\033[94m"
        COLOR_RESET = "\033[0m"
        COLOR_CYAN = "\033[96m"

    FORMAT = "%(levelname)s: %(message)s"

    FORMATS = {
        logging.DEBUG: Color.COLOR_BLUE + FORMAT + Color.COLOR_RESET,
        logging.INFO: Color.COLOR_GREEN + FORMAT + Color.COLOR_RESET,
        logging.WARNING: Color.COLOR_YELLOW + FORMAT + Color.COLOR_RESET,
        logging.ERROR: Color.COLOR_RED + FORMAT + Color.COLOR_RESET,
        logging.CRITICAL: Color.COLOR_RED + FORMAT + Color.COLOR_RESET,
        SUCCESS_LEVEL_NUM: Color.COLOR_CYAN + FORMAT + Color.COLOR_RESET,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.FORMAT)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def create_log_app():
    handler = logging.StreamHandler()
    handler.setFormatter(ColorFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(handler)
    return root_logger



