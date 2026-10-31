from typing import Dict, Set, Optional, List, Tuple

class CrossReferencer:
    """
    Cross-references imported packages with dependency versions.
    For each imported package, determines if it is present in the dependency list
    and what version specifier (if any) is declared.
    """
    def __init__(self, 
                 imports_by_file: Dict[str, Set[str]],
                 dependencies: Dict[str, Optional[str]]):
        self.imports_by_file = imports_by_file
        self.dependencies = dependencies

    def cross_reference(self) -> Dict[str, Dict[str, Optional[str]]]:
        """
        Returns a mapping:
            {filename: {imported_package: version_spec or None}}
        For each file and each imported package, shows the declared version (if any) from dependencies.
        """
        result: Dict[str, Dict[str, Optional[str]]] = {}
        for fname, imports in self.imports_by_file.items():
            file_result = {}
            for imp in imports:
                dep_version = self._find_dependency_version(imp)
                file_result[imp] = dep_version
            result[fname] = file_result
        return result

    def _find_dependency_version(self, import_name: str) -> Optional[str]:
        """
        Looks up the dependency version for a given import name.
        Tries exact match, then case-insensitive match.
        """
        # Most dependency names are lowercased in requirements/pyproject
        key = import_name.lower()
        if key in self.dependencies:
            return self.dependencies[key]
        # Try case-insensitive fallback
        for dep_name, version in self.dependencies.items():
            if dep_name.lower() == key:
                return version
        return None

    def summarize_imports_with_versions(self) -> List[Tuple[str, str, Optional[str]]]:
        """
        Returns a flat list of (filename, imported_package, version_spec or None)
        Useful for reporting or further analysis.
        """
        summary = []
        for fname, imports in self.imports_by_file.items():
            for imp in imports:
                version = self._find_dependency_version(imp)
                summary.append((fname, imp, version))
        return summary
