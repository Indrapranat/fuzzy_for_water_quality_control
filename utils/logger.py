"""
utils/logger.py
===============
Konfigurasi sistem logging terpusat untuk seluruh project.

Menggunakan standar library `logging` Python dengan:
- Handler ke konsol (StreamHandler) untuk output real-time.
- Handler ke file (FileHandler) untuk arsip permanen.
- Format pesan yang konsisten dan informatif.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

import config


def setup_logger(
    log_file: Optional[Path] = None,
    level: str = config.LOG_LEVEL,
) -> logging.Logger:
    """Mengkonfigurasi dan mengembalikan root logger project.

    Memanggil fungsi ini di main.py sebelum menggunakan modul apapun
    untuk memastikan semua log tercatat dengan baik.

    Args:
        log_file: Path opsional ke file log. Jika None, hanya log ke konsol.
        level: Level logging (DEBUG, INFO, WARNING, ERROR, CRITICAL).

    Returns:
        Root logger yang sudah dikonfigurasi.

    Examples:
        >>> logger = setup_logger(log_file=Path("output/run.log"))
        >>> logger.info("Sistem dimulai.")
    """
    root_logger = logging.getLogger()

    # Hindari duplikasi handler jika dipanggil lebih dari sekali
    if root_logger.handlers:
        root_logger.handlers.clear()

    numeric_level = getattr(logging, level.upper(), logging.INFO)
    root_logger.setLevel(numeric_level)

    formatter = logging.Formatter(
        fmt=config.LOG_FORMAT,
        datefmt=config.LOG_DATE_FORMAT,
    )

    # Handler: Output ke konsol (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Handler: Output ke file (opsional)
    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    return root_logger
