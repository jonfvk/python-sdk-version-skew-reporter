from typing import Dict, Optional, List, Set, Tuple

class VersionSkewDetector:
    """
    Detects multiple versions of the same package in dependency specifications.
    Given a mapping of package names to lists of version specifiers (from multiple sources),
    flags packages that have more than one distinct version specifier.
    """
    def __init__(self, dependencies_by_source: Dict[str, Dict[str, Optional[str]]]):
        """
        dependencies_by_source: {source_name: {package_name: version_spec or None}}
        Example:
            {
                'requirements.txt': {'foo': '==1.2.3', 'bar': '>=2.0'},
                'pyproject.toml': {'foo': '>=1.0', 'baz': None}
            }
        """
        self.dependencies_by_source = dependencies_by_source

    def detect_skew(self) -> Dict[str, Set[Optional[str]]]:
        """
        Returns a dict: {package_name: set of version specifiers}
        Only includes packages with more than one distinct version specifier.
        None is treated as a version (i.e., unspecified).
        """
        # Aggregate all version specs for each package across sources
        package_versions: Dict[str, Set[Optional[str]]] = {}
        for source, deps in self.dependencies_by_source.items():
            for pkg, ver in deps.items():
                pkg_lc = pkg.lower()
                if pkg_lc not in package_versions:
                    package_versions[pkg_lc] = set()
                package_versions[pkg_lc].add(ver)
        # Only keep packages with more than one version spec
        skewed = {pkg: vers for pkg, vers in package_versions.items() if len(vers) > 1}
        return skewed

    def skew_details(self) -> List[Tuple[str, List[Tuple[str, Optional[str]]]]]:
        """
        Returns a list of (package_name, [(source, version_spec), ...])
        Only for packages with version skew.
        """
        # First, detect skewed packages
        skewed = self.detect_skew()
        details = []
        for pkg in skewed:
            pkg_details = []
            for source, deps in self.dependencies_by_source.items():
                if pkg in deps:
                    pkg_details.append((source, deps[pkg]))
            details.append((pkg, pkg_details))
        return details
