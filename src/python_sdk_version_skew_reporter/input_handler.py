import os

class InputHandler:
    """
    Handles input path validation for dependency files.
    Accepts a path to requirements.txt or pyproject.toml.
    """
    SUPPORTED_FILES = ("requirements.txt", "pyproject.toml")

    def __init__(self, path: str):
        self.path = path

    def is_supported_file(self) -> bool:
        """
        Checks if the file is one of the supported dependency files.
        """
        filename = os.path.basename(self.path)
        return filename in self.SUPPORTED_FILES

    def exists(self) -> bool:
        """
        Checks if the file exists at the given path.
        """
        return os.path.isfile(self.path)

    def validate(self) -> None:
        """
        Validates that the path exists and is a supported file.
        Raises ValueError if not valid.
        """
        if not self.exists():
            raise ValueError(f"File does not exist: {self.path}")
        if not self.is_supported_file():
            raise ValueError(
                f"Unsupported file type: {self.path}. "
                f"Supported: {', '.join(self.SUPPORTED_FILES)}"
            )
