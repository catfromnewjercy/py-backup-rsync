import os
import datetime
import subprocess
import shutil
import logging
from config import TARGET_DIRECTORY
from archive import ArchiveManager
from nfs import NFSManager

class BackupManager:
    @staticmethod
    def get_backups(prefix: str):
        return sorted(
            [d for d in os.listdir(TARGET_DIRECTORY) if d.startswith(prefix)],
            key=lambda x: datetime.datetime.strptime(x[5:], "%Y-%m-%d"),
            reverse=True
        )

    @classmethod
    def create_full_backup(cls, source_dir: str):
        full_backup = os.path.join(TARGET_DIRECTORY, "full_" + datetime.date.today().strftime("%Y-%m-%d"))
        logging.info(f"Создаю полный бэкап: {full_backup}")

        if os.path.exists(full_backup):
            shutil.rmtree(full_backup, ignore_errors=True)
        
        os.makedirs(full_backup, exist_ok=True)

        try:
            subprocess.run(["rsync", "-av", "--delete", source_dir, full_backup], check=True)
            ArchiveManager.archive_old_backup(full_backup)
        except subprocess.CalledProcessError as e:
            logging.error(f"Ошибка при выполнении rsync: {e}")
            return None

        return full_backup

    @classmethod
    def create_incremental_backup(cls, source_dir: str, latest_full: str):
        incr_backup = os.path.join(TARGET_DIRECTORY, "incr_" + datetime.date.today().strftime("%Y-%m-%d"))
        logging.info(f"Создаю инкрементальный бэкап: {incr_backup}")

        os.makedirs(incr_backup, exist_ok=True)

        try:
            subprocess.run(["rsync", "-av", "--link-dest=" + latest_full, source_dir, incr_backup], check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Ошибка при выполнении rsync: {e}")

    @classmethod
    def backup_source_directory(cls, source_directory: str):
        if not NFSManager.mount():
            return

        full_backups = cls.get_backups("full_")
        latest_full = None

        if full_backups:
            latest_full = os.path.join(TARGET_DIRECTORY, full_backups[0])
            full_backup_date = datetime.datetime.strptime(full_backups[0][5:], "%Y-%m-%d").date()
            days_since_full = (datetime.date.today() - full_backup_date).days

            if days_since_full > 6:
                latest_full = cls.create_full_backup(source_directory)
        else:
            latest_full = cls.create_full_backup(source_directory)

        if latest_full:
            cls.create_incremental_backup(source_directory, latest_full)

        NFSManager.unmount()
