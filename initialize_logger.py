import logging
from logging import Formatter, FileHandler, StreamHandler


update_logger = logging.getLogger(name="update_logger")
update_logger.setLevel(logging.DEBUG)

update_logger_file_handler = FileHandler(filename="logs/update.log", encoding="UTF-8")
update_logger_file_handler.setLevel(logging.DEBUG)
update_logger_file_handler.setFormatter(Formatter(u"[{asctime}] {message}", style="{"))

update_logger.addHandler(update_logger_file_handler)


keyboard_logger = logging.getLogger(name="keyboard_logger")
keyboard_logger.setLevel(logging.DEBUG)

keyboard_logger_file_handler = FileHandler(filename="logs/keyboard.log")
keyboard_logger_file_handler.setLevel(logging.DEBUG)
keyboard_logger_file_handler.setFormatter(
    Formatter("[{asctime}] [{filename} - {funcName} - {lineno}] {message}", style="{")
)

# keyboard_logger_console_handler = StreamHandler()
# keyboard_logger_console_handler.setLevel(logging.DEBUG)
# keyboard_logger_console_handler.setFormatter(
#     Formatter("[{asctime}] [{filename} - {funcName} - {lineno}] {message}", style="{")
# )

# keyboard_logger.addHandler(keyboard_logger_console_handler)
keyboard_logger.addHandler(keyboard_logger_file_handler)
