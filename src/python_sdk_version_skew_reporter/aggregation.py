from typing import Dict, Set, Optional, List, Tuple

class VersionSkewAggregator:
    """
    Aggregates and formats version skew findings for reporting.
    Consumes the output of VersionSkewDetector and produces structured summaries.
    """
    def __init__(self, 
                 skewed_packages: Dict[str, Set[Optional[str]]],
                 skew_details: List[Tuple[str, List[Tuple[str, Optional[str]]]]]):
        """
        skewed_packages: {package_name: set of version specifiers}
        skew_details: [(package_name, [(source, version_spec), ...]), ...]
        """
        self.skewed_packages = skewed_packages
        self.skew_details = skew_details

    def format_skew_summary(self) -> str:
        """
        Returns a formatted string summarizing all version skew findings.
        Example output:
            Version Skew Detected:
            - package1: versions found: ==1.0.0, >=1.0, None
              Sources:
                requirements.txt: ==1.0.0
                pyproject.toml: >=1.0
                pyproject.toml: None
            - package2: versions found: ==2.0.0, ==2.1.0
              Sources:
                requirements.txt: ==2.0.0
                requirements-dev.txt: ==2.1.0
        """
        if not self.skewed_packages:
            return "No version skew detected."
        lines = ["Version Skew Detected:"]
        for pkg, sources in self.skew_details:
            versions = {ver if ver is not None else "(unspecified)" for _, ver in sources}
            lines.append(f"- {pkg}: versions found: {', '.join(sorted(versions))}")
            lines.append("  Sources:")
            for source, ver in sources:
                ver_str = ver if ver is not None else "(unspecified)"
                lines.append(f"    {source}: {ver_str}")
        return "\n".join(lines)

    def as_dict(self) -> List[Dict[str, object]]:
        """
        Returns a list of dicts for programmatic use, e.g.:
        [
            {
                'package': 'foo',
                'versions': ['==1.0.0', '>=1.0', None],
                'sources': [ {'source': 'requirements.txt', 'version': '==1.0.0'}, ... ]
            },
            ...
        ]
        """
        result = []
        for pkg, sources in self.skew_details:
            versions = [ver for _, ver in sources]
            result.append({
                'package': pkg,
                'versions': versions,
                'sources': [ {'source': src, 'version': ver} for src, ver in sources ]
            })
        return result
