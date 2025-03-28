import os
import logging
import socket

LOG_FILE = "/var/log/backup.log"

LOG_DIR = os.path.dirname(LOG_FILE)
if LOG_DIR and not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

SOURCE_DIRECTORY_LIST = ["/DATASET/project/scada/local"]
SERVER_NAME = socket.gethostname()
NFS_SERVER = "X.X.X.X"
NFS_PATH = "/NFS"
MOUNT_PATH = "/mnt/nfs"
BACKUPS_LOCATION = "/backups"
DC_ID = "dc1"
TARGET_DIRECTORY = f"{MOUNT_PATH}{BACKUPS_LOCATION}/{DC_ID}/{SERVER_NAME}"

