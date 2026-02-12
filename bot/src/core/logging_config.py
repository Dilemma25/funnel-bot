import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


def setup_logging(name: str = None, service: str = "bot") -> logging.Logger:
    """Настройка с ротацией по миднайту"""

    # ✅ Абсолютный путь к директории проекта
    project_root = Path(__file__).parent.parent.parent  # /app
    log_dir = project_root / "logs"
    log_dir.mkdir(exist_ok=True)

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.handlers.clear()

    # Консоль
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    root_logger.addHandler(console)

    # Файл
    file_handler = TimedRotatingFileHandler(
        filename=log_dir / f'{service}.log',  # ✅ Абсолютный путь
        when='midnight',
        backupCount=30,
        encoding='utf-8'
    )
    file_handler.suffix = "%Y-%m-%d"
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    logging.getLogger('arq').propagate = True

    return logging.getLogger(name)