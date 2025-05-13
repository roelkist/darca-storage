import os
from typing import List, Union, Optional

from darca_file_utils.file_utils import FileUtils, FileUtilsException
from darca_file_utils.directory_utils import DirectoryUtils
from darca_storage.interfaces.file_backend import FileBackend


class LocalFileBackend(FileBackend):
    """
    Local disk-based implementation of the FileBackend protocol.

    Supports per-operation permissions and ownership for files and directories.
    """

    def read(self, path: str, binary: bool = False) -> Union[str, bytes]:
        """
        Read a file. Binary mode is ignored — format is auto-detected.
        """
        return FileUtils.read_file(path)

    def write(
        self,
        path: str,
        content: Union[str, bytes],
        *,
        permissions: Optional[int] = None,
        user: Optional[str] = None
    ):
        """
        Write content to a file with optional permissions and ownership.

        Args:
            path (str): Target file path.
            content (str | bytes): Data to write.
            permissions (int, optional): chmod-style permissions (e.g., 0o644).
            user (str, optional): Owner username (requires privilege).
        """
        if not isinstance(content, (str, bytes)):
            raise TypeError(f"Unsupported content type: {type(content)}")

        FileUtils.write_file(
            file_path=path,
            content=content,
            permissions=permissions,
            user=user,
        )

    def delete(self, path: str):
        FileUtils.remove_file(path)

    def exists(self, path: str) -> bool:
        return FileUtils.file_exist(path) or DirectoryUtils.directory_exist(path)

    def list(self, base_path: str, recursive: bool = False) -> List[str]:
        return DirectoryUtils.list_directory(base_path, recursive=recursive)

    def mkdir(
        self,
        path: str,
        parents: bool = True,
        *,
        permissions: Optional[int] = None,
        user: Optional[str] = None
    ):
        """
        Create a directory with optional permissions and ownership.

        Note: `parents` is accepted but not yet handled by DirectoryUtils.

        Args:
            path (str): Directory to create.
            permissions (int, optional): chmod-style permissions (e.g., 0o755).
            user (str, optional): Owner username (requires privilege).
        """
        DirectoryUtils.create_directory(
            path=path,
            permissions=permissions,
            user=user,
        )

    def rmdir(self, path: str):
        DirectoryUtils.remove_directory(path)

    def rename(self, src: str, dest: str):
        if FileUtils.file_exist(src):
            FileUtils.rename_file(src, dest)
        elif DirectoryUtils.directory_exist(src):
            DirectoryUtils.rename_directory(src, dest)
        else:
            raise FileUtilsException(
                message=f"Cannot rename: source path does not exist: {src}",
                error_code="RENAME_SOURCE_NOT_FOUND",
                metadata={"src": src, "dest": dest}
            )

    def stat_mtime(self, path: str) -> float:
        if not os.path.exists(path):
            raise FileUtilsException(
                message=f"Cannot stat: path does not exist: {path}",
                error_code="STAT_MTIME_NOT_FOUND",
                metadata={"path": path}
            )
        return os.path.getmtime(path)
