import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from datetime import datetime


def setup_logging(name: str = None, service: str = "bot") -> logging.Logger:
    """Настройка с ротацией по миднайту и хранением в папках по датам"""

    # Абсолютный путь к директории проекта
    project_root = Path(__file__).parent.parent.parent  # /app

    # ✅ Создаём папку по текущей дате
    today = datetime.now().strftime("%Y-%m-%d")
    log_dir = project_root / "logs" / today
    log_dir.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Очищаем handlers только если ещё не настроено
    if not root_logger.handlers:
        # Консоль
        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(formatter)
        root_logger.addHandler(console)

        # Файл
        file_handler = TimedRotatingFileHandler(
            filename=log_dir / f'{service}.log',
            when='midnight',
            backupCount=30,
            encoding='utf-8'
        )
        file_handler.suffix = "%Y-%m-%d"
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    # Настройка ARQ логгера
    arq_logger = logging.getLogger('arq')
    arq_logger.propagate = True
    arq_logger.setLevel(logging.INFO)

    return logging.getLogger(name) if name else root_logger