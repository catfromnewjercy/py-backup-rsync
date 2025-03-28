import os
import tarfile
import shutil
import logging
import tempfile
from config import ARCHIVE_DIRECTORY

class ArchiveManager:
    @staticmethod
    def archive_old_backup(full_backup_dir):
        if not os.path.exists(full_backup_dir):
            logging.error(f"Ошибка: Каталог {full_backup_dir} не найден.")
            return

        if not os.path.exists(ARCHIVE_DIRECTORY):
            os.makedirs(ARCHIVE_DIRECTORY)

        archive_name = os.path.join(ARCHIVE_DIRECTORY, f"{os.path.basename(full_backup_dir)}.tar.gz")
        temp_dir = tempfile.mkdtemp()

        try:
            shutil.copytree(full_backup_dir, os.path.join(temp_dir, "backup"))

            with tarfile.open(archive_name, "w:gz") as tar:
                tar.add(os.path.join(temp_dir, "backup"), arcname=os.path.basename(full_backup_dir))

            logging.info(f"Архив создан: {archive_name}")

        except Exception as e:
            logging.error(f"Ошибка при создании архива: {e}")

        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

        ArchiveManager.cleanup_old_archives()

    @staticmethod
    def cleanup_old_archives(max_archives=2):
        archives = [os.path.join(ARCHIVE_DIRECTORY, f) for f in os.listdir(ARCHIVE_DIRECTORY)]
        archives = sorted(archives, key=os.path.getctime)

        while len(archives) > max_archives:
            old_archive = archives.pop(0)
            os.remove(old_archive)
            logging.info(f"Удален старый архив: {old_archive}")
