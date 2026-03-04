import webbrowser,os
import subprocess
from typing import Optional, Dict,Any,List
import os
from dotenv import load_dotenv
from pathlib import Path
import shutil
here = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
dot=os.path.join(here,'.env')
def tools_list():
    return """create_file(path) — Creates a new file at the specified path(path of the new file). Creates parent directories if needed.
read_file(path) — Reads and returns the content of the specified file.
write_file(path, content) — Writes the given content to the specified file. Overwrites existing content.
delete_file(path) — Deletes the file or folder at the specified path.
move_file(source, destination) — Moves a file or folder from source path to destination path. Creates destination folder if it doesn't exist.
list_directory(path) — Lists all files and folders inside the specified directory.
search_file_by_name(name, start_path) — Recursively searches for files with a name containing the given string starting from start_path. Returns a list of matches.
copy_file(source, destination) — Copies a file from source to destination.
copy_folder(source, destination) — Recursively copies a folder from source to destination.
rename_file(source, new_name) — Renames a file or folder to the specified new name.
move_file(source_path, destination_path) - Moves a File or Folder from source_path to destination_path. Creates destination folder if it doesn't exist."""
if os.path.exists(dot):
    load_dotenv(dot)
DEFAULT_RESTRICTIONS = ['rm', 'shutdown', 'reboot', 'poweroff', 'format', 'del ', 'erase', ':(){', 'mkfs', 'dd ']
def load_restrictions() -> list[str]:
    s = os.getenv('AGENT_RESTRICTIONS', '')
    if not s:
        return DEFAULT_RESTRICTIONS.copy()
    return [r.strip() for r in s.split(',') if r.strip()]
def check_safe_shell(cmd: str, restrictions: list[str]) -> bool:
    lower = cmd.lower()
    for bad in restrictions:
        if bad in lower:
            return False
    return True



def run_shell(command: str, timeout: Optional[int] = 10) -> Dict:
    try:
        restrictions = load_restrictions()

        if not check_safe_shell(command, restrictions):
            return {
                "status": "blocked",
                "output": None,
                "error": "Command contains restricted keywords."
            }

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        return {
            "status": "success" if result.returncode == 0 else "error",
            "output": (result.stdout + result.stderr).strip(),
            "error": None if result.returncode == 0 else "Non-zero exit code"
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "output": None,
            "error": "Command timed out."
        }

    except Exception as e:
        return {
            "status": "error",
            "output": None,
            "error": str(e)
        }
def open_url(url: str):
    try:
        webbrowser.open(url)
        return True
    except Exception as e:
        return False
class FileSystemTools:
    @staticmethod
    def _response(status: str, output=None, error=None) -> Dict[str, Any]:
        return {
            "status": status,
            "output": output,
            "error": error
        }
    @staticmethod
    def create_file(path: str) -> Dict[str, Any]:
        try:
            p = Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.touch(exist_ok=False)
            return FileSystemTools._response("success", f"File created at {path}")
        except Exception as e:
            return FileSystemTools._response("error", None, str(e))
    @staticmethod
    def read_file(path: str) -> Dict[str, Any]:
        try:
            p = Path(path)

            if not p.exists():
                return FileSystemTools._response("error", None, "File does not exist.")

            if not p.is_file():
                return FileSystemTools._response("error", None, "Path is not a file.")

            content = p.read_text(encoding="utf-8")
            return FileSystemTools._response("success", content)
        except Exception as e:
            return FileSystemTools._response("error", None, str(e))
    @staticmethod
    def overwrite_file(path: str, content: str) -> Dict[str, Any]:
        try:
            p = Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
            return FileSystemTools._response("success", f"Written to {path}")
        except Exception as e:
            return FileSystemTools._response("error", None, str(e))
    @staticmethod
    def delete_file(path: str) -> Dict[str, Any]:
        try:
            p = Path(path)

            if not p.exists():
                return FileSystemTools._response("error", None, "File does not exist.")

            if p.is_file():
                p.unlink()
            else:
                shutil.rmtree(p)

            return FileSystemTools._response("success", f"{path} deleted.")

        except Exception as e:
            return FileSystemTools._response("error", None, str(e))
    @staticmethod
    def list_directory(path: str) -> Dict[str, Any]:
        try:
            p = Path(path)

            if not p.exists():
                return FileSystemTools._response("error", None, "Directory does not exist.")

            if not p.is_dir():
                return FileSystemTools._response("error", None, "Path is not a directory.")

            items = [item.name for item in p.iterdir()]
            return FileSystemTools._response("success", items)

        except Exception as e:
            return FileSystemTools._response("error", None, str(e))
    @staticmethod
    def list_directory(path: str) -> Dict[str, Any]:
        try:
            p = Path(path)

            if not p.exists():
                return FileSystemTools._response("error", None, "Directory does not exist.")

            if not p.is_dir():
                return FileSystemTools._response("error", None, "Path is not a directory.")

            items = [item.name for item in p.iterdir()]
            return FileSystemTools._response("success", items)

        except Exception as e:
            return FileSystemTools._response("error", None, str(e))
    @staticmethod
    def move_file(source: str, destination: str) -> Dict[str, Any]:
        try:
            src = Path(source)
            dst = Path(destination)
            if not src.exists():
                return FileSystemTools._response("error", None, "Source file/folder does not exist.")
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            return FileSystemTools._response("success", f"Moved {source} to {destination}")
        except Exception as e:
            return FileSystemTools._response("error", None, str(e))