import argparse
import logging
from backup import BackupManager
from config import SOURCE_DIRECTORY_LIST
from nfs import NFSManager

logging.info("Запуск Backup Manager")

def main():
    parser = argparse.ArgumentParser(description="Backup Manager")
    parser.add_argument(
        "--mode", choices=["full", "incremental", "all"], default="all",
        help="Выбор режима: full (только полный), incremental (только инкрементальный), all (оба)"
    )
    args = parser.parse_args()

    if not isinstance(SOURCE_DIRECTORY_LIST, (list, tuple)):
        logging.error("SOURCE_DIRECTORY_LIST в config.py должен быть списком!")
        return

    if not NFSManager.mount():
        logging.error("Ошибка монтирования NFS. Бэкап отменён.")
        return

    for src_dir in SOURCE_DIRECTORY_LIST:
        if args.mode in ["full", "all"]:
            logging.info(f"🔹 Запуск полного бэкапа для {src_dir}")
            latest_full = BackupManager.create_full_backup(src_dir)
        else:
            latest_full = BackupManager.get_backups("full_")[0]

        if args.mode in ["incremental", "all"]:
            logging.info(f"🔹 Запуск инкрементального бэкапа для {src_dir}")
            if latest_full:
                BackupManager.create_incremental_backup(src_dir, latest_full)
            else:
                logging.warning(f"Пропущен инкрементальный бэкап для {src_dir}, так как нет полного.")

    NFSManager.unmount()

if __name__ == "__main__":
    main()
