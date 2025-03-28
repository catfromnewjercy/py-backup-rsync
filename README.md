# Backup Manager

Этот проект представляет собой систему резервного копирования с поддержкой полного и инкрементального бэкапа, а также автоматическим монтированием NFS.

## 📌 Возможности
- 🔹 Полный (`full`) и инкрементальный (`incremental`) бэкап
- 🔹 Архивация старых бэкапов
- 🔹 Поддержка NFS для хранения резервных копий
- 🔹 Автоматическое управление монтированием NFS
- 🔹 Логирование операций

## 🛠️ Установка
1. Клонируйте репозиторий:
   ```sh
   git clone https://github.com/catfromnewjercy/py-backup-nfs.git
   cd py-backup-nfs
   ```
2. Установите зависимости (если необходимо):
   ```sh
   pip install -r requirements.txt
   ```
3. Убедитесь, что у вас установлен `rsync`, `nfs-utils` (или `nfs-common` для Ubuntu/Debian):
   ```sh
   sudo apt install rsync nfs-common  # для Ubuntu/Debian
   ```

## ⚙️ Конфигурация
Редактируйте файл `config.py` для указания необходимых параметров:

```python
SOURCE_DIRECTORY_LIST = ["/DATASET/project/scada/local"]
SERVER_NAME = socket.gethostname()
NFS_SERVER = "X.X.X.X"
NFS_PATH = "/NFS"
MOUNT_PATH = "/mnt/nfs"
BACKUPS_LOCATION = "/backups"
DC_ID = "dc1"
TARGET_DIRECTORY = f"{MOUNT_PATH}{BACKUPS_LOCATION}/{DC_ID}/{SERVER_NAME}"
```

## 🚀 Запуск
Запустите резервное копирование в нужном режиме:

```sh
python main.py --mode full          # Только полный бэкап
python main.py --mode incremental   # Только инкрементальный бэкап
python main.py --mode all           # Полный + инкрементальный бэкап (по умолчанию)
```

## 📂 Структура проекта
```
py-backup-nfs/
├── archive.py        # Управление архивами старых бэкапов
├── backup.py         # Основная логика резервного копирования
├── config.py         # Конфигурация проекта
├── main.py           # Главный скрипт для запуска
├── nfs.py            # Управление NFS монтированием
├── backup.log        # Файл логов
└── README.md         # Документация проекта
```

## 📝 Логирование
Логи сохраняются в файле `backup.log`. В случае ошибок проверьте этот файл:
```sh
cat backup.log
```

## 📜 Лицензия
Этот проект распространяется под лицензией MIT. См. [LICENSE](LICENSE) для деталей.

