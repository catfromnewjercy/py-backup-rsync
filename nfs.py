import subprocess
import os
import logging
from config import MOUNT_PATH, NFS_SERVER, NFS_PATH

class NFSManager:
    @staticmethod
    def is_folder_exist(directory: str) -> bool:
        return os.path.isdir(directory)

    @staticmethod
    def is_path_mounted(directory: str) -> bool:
        return os.path.ismount(directory)

    @classmethod
    def mount(cls) -> bool:
        if not cls.is_folder_exist(MOUNT_PATH):
            logging.error(f"Ошибка: директория {MOUNT_PATH} не существует. Создаю...")
            try:
                os.makedirs(MOUNT_PATH, exist_ok=True)
                logging.info(f"Директория {MOUNT_PATH} успешно создана.")
            except OSError as e:
                logging.exception(f"Ошибка при создании директории {MOUNT_PATH}: {e}")
                return False

        if cls.is_path_mounted(MOUNT_PATH):
            logging.info(f"{MOUNT_PATH} уже смонтирована.")
            return True

        remote_path = f"{NFS_SERVER}:{NFS_PATH}"
        cmd = ["mount", "-t", "nfs", remote_path, MOUNT_PATH, "-o", "vers=3"]

        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            logging.info(f"NFS {remote_path} успешно примонтирован в {MOUNT_PATH}")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Ошибка при монтировании NFS: {e.stderr.strip()}")
            return False

    @classmethod
    def unmount(cls) -> bool:
        if cls.is_path_mounted(MOUNT_PATH):
            try:
                subprocess.run(["umount", MOUNT_PATH], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                logging.info(f"{MOUNT_PATH} успешно размонтирован.")
                return True
            except subprocess.CalledProcessError as e:
                logging.error(f"Ошибка при размонтировании: {e.stderr.strip()}")
                return False
        else:
            logging.warning(f"{MOUNT_PATH} не смонтирована, пропускаю размонтирование.")
            return True
