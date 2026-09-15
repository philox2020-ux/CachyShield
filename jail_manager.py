import atexit
import logging
import os
import shutil
import stat
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class JailedItem:
    """Represents an application or directory that has been sandboxed into the jail."""
    original_path: str
    jailed_path: str
    name: str
    is_directory: bool
    timestamp: datetime
    size_bytes: int

    def formatted_size(self) -> str:
        """Returns the size of the item in human-readable string format."""
        size = float(self.size_bytes)
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"


class JailManager:
    """Handles file operations for sandboxing: manages jail directory,
    moves applications or folders into jail, tracks jailed items, and clears
    the jail folder completely on exit.
    """

    def __init__(self, jail_dir: Optional[Path] = None) -> None:
        """Initializes the JailManager with a target jail directory.

        Args:
            jail_dir: Optional custom Path for the jail folder. Defaults to ~/.local/share/arch_jail
        """
        if jail_dir is None:
            home = Path.home()
            self._jail_dir = home / ".local" / "share" / "arch_jail"
        else:
            self._jail_dir = Path(jail_dir).resolve()

        self._jailed_items: Dict[str, JailedItem] = {}
        self._ensure_jail_directory()
        atexit.register(self.cleanup_jail)

    @property
    def jail_dir(self) -> Path:
        """Returns the path to the jail directory."""
        return self._jail_dir

    def _ensure_jail_directory(self) -> None:
        """Creates the jail directory if it does not exist and ensures correct permissions."""
        try:
            self._jail_dir.mkdir(parents=True, exist_ok=True)
            os.chmod(self._jail_dir, stat.S_IRWXU)
        except OSError as e:
            logger.error("Failed to initialize jail directory '%s': %s", self._jail_dir, e)
            raise

    def _calculate_size(self, path: Path) -> int:
        """Calculates total size in bytes for a file or directory tree."""
        try:
            if path.is_symlink():
                return 0
            if path.is_file():
                return path.stat().st_size
            if path.is_dir():
                total = 0
                for root, _, files in os.walk(path):
                    for f in files:
                        fp = Path(root) / f
                        if not fp.is_symlink() and fp.exists():
                            total += fp.stat().st_size
                return total
        except OSError as e:
            logger.warning("Error calculating size for '%s': %s", path, e)
        return 0

    def jail_item(self, source_path_str: str) -> Optional[JailedItem]:
        """Moves an application file or folder into the sandbox jail.

        Args:
            source_path_str: Filesystem path to the application or directory to sandbox.

        Returns:
            JailedItem instance tracking the moved item, or None if the operation fails.
        """
        source = Path(source_path_str).resolve()
        if not source.exists():
            logger.error("Source path does not exist: %s", source_path_str)
            return None

        self._ensure_jail_directory()

        if self._jail_dir in source.parents or source == self._jail_dir:
            logger.warning("Cannot jail an item already inside or containing the jail directory: %s", source)
            return None

        target_name = source.name
        dest = self._jail_dir / target_name

        counter = 1
        stem = source.stem
        suffix = source.suffix
        while dest.exists():
            if source.is_dir():
                dest = self._jail_dir / f"{stem}_{counter}"
            else:
                dest = self._jail_dir / f"{stem}_{counter}{suffix}"
            counter += 1

        is_dir = source.is_dir()
        size_bytes = self._calculate_size(source)

        try:
            shutil.move(str(source), str(dest))
            item = JailedItem(
                original_path=str(source),
                jailed_path=str(dest),
                name=dest.name,
                is_directory=is_dir,
                timestamp=datetime.now(),
                size_bytes=size_bytes,
            )
            self._jailed_items[str(dest)] = item
            logger.info("Successfully moved '%s' into jail at '%s'", source, dest)
            return item
        except OSError as e:
            logger.error("Failed to move '%s' to '%s': %s", source, dest, e)
            return None

    def release_item(self, jailed_path_str: str) -> bool:
        """Restores a jailed item back to its original location.

        Args:
            jailed_path_str: Path of the item inside the jail.

        Returns:
            True if successfully restored, False otherwise.
        """
        target = Path(jailed_path_str).resolve()
        item = self._jailed_items.get(str(target))

        if not target.exists():
            logger.warning("Item to release does not exist in jail: %s", jailed_path_str)
            self._jailed_items.pop(str(target), None)
            return False

        orig_path = Path(item.original_path) if item else Path.home() / target.name

        if orig_path.exists():
            logger.error("Original path already occupied, cannot restore '%s' to '%s'", target, orig_path)
            return False

        try:
            orig_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(target), str(orig_path))
            self._jailed_items.pop(str(target), None)
            logger.info("Restored '%s' to original location '%s'", target, orig_path)
            return True
        except OSError as e:
            logger.error("Failed to release '%s' to '%s': %s", target, orig_path, e)
            return False

    def list_jailed_items(self) -> List[JailedItem]:
        """Returns a list of all currently tracked jailed items.

        Returns:
            List of JailedItem instances.
        """
        active_items = []
        for path_str, item in list(self._jailed_items.items()):
            if Path(path_str).exists():
                active_items.append(item)
            else:
                self._jailed_items.pop(path_str, None)
        return active_items

    def cleanup_jail(self) -> None:
        """Completely empties all contents of the jail folder."""
        if not self._jail_dir.exists():
            return

        logger.info("Emptying sandbox jail at '%s'", self._jail_dir)
        try:
            for entry in self._jail_dir.iterdir():
                try:
                    if entry.is_symlink() or entry.is_file():
                        entry.unlink(missing_ok=True)
                    elif entry.is_dir():
                        shutil.rmtree(entry, ignore_errors=False)
                except OSError as err:
                    logger.error("Failed to remove item '%s' during cleanup: %s", entry, err)
        except OSError as e:
            logger.error("Failed to list jail directory during cleanup: %s", e)
        finally:
            self._jailed_items.clear()
            logger.info("Jail cleanup completed.")