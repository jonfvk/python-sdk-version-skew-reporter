import ast
import os
from typing import Dict, List, Set, Optional

class ImportScanner:
    """
    Scans Python source files for import statements.
    Extracts top-level imported package/module names.
    """
    def __init__(self, root_dir: str):
        self.root_dir = root_dir

    def scan(self) -> Dict[str, Set[str]]:
        """
        Walks the root directory, parses .py files, and collects imports.
        Returns a dict: {filename: set of imported package names}
        """
        imports_by_file = {}
        for dirpath, _, filenames in os.walk(self.root_dir):
            for fname in filenames:
                if fname.endswith('.py'):
                    fpath = os.path.join(dirpath, fname)
                    try:
                        with open(fpath, 'r', encoding='utf-8') as f:
                            content = f.read()
                        imported = self._extract_imports(content)
                        imports_by_file[fpath] = imported
                    except Exception:
                        # Skip files that can't be read or parsed
                        continue
        return imports_by_file

    @staticmethod
    def _extract_imports(source: str) -> Set[str]:
        """
        Parses Python source and extracts top-level imported package names.
        Returns a set of names (e.g., {'requests', 'os', 'numpy'}).
        """
        imported = set()
        try:
            tree = ast.parse(source)
        except Exception:
            return imported
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.name.split('.', 1)[0]
                    imported.add(name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    name = node.module.split('.', 1)[0]
                    imported.add(name)
        return imported
