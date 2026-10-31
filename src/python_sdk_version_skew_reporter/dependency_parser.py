import re
from typing import Dict, Tuple, List, Optional

class DependencyParser:
    """
    Parses requirements.txt and pyproject.toml files for package names and versions.
    Returns a dictionary mapping package names to version specifiers (or None).
    Handles extras and environment markers gracefully.
    """
    @staticmethod
    def parse_requirements_txt(content: str) -> Dict[str, Optional[str]]:
        """
        Parses requirements.txt content.
        Returns dict: {package_name: version_spec or None}
        Handles extras (e.g., requests[security]) and environment markers.
        """
        deps = {}
        # Regex for lines like: package[extras]==1.2.3; marker
        req_line = re.compile(r"^([A-Za-z0-9_.\-]+)(\[[A-Za-z0-9_,\-]+\])?\s*([=<>!~]=[^#;\s]+)?")
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # Remove inline comments
            line = line.split('#', 1)[0].strip()
            # Remove environment markers (after ';')
            line = line.split(';', 1)[0].strip()
            m = req_line.match(line)
            if m:
                name = m.group(1)
                # Ignore extras (m.group(2)), just use base name
                version = m.group(3).strip() if m.group(3) else None
                deps[name.lower()] = version
        return deps

    @staticmethod
    def parse_pyproject_toml(content: str) -> Dict[str, Optional[str]]:
        """
        Parses pyproject.toml content for [project] and [tool.poetry.dependencies].
        Returns dict: {package_name: version_spec or None}
        Handles inline tables, arrays, extras, and markers.
        """
        deps = {}
        in_deps = False
        dep_sections = [
            '[project.dependencies]',
            '[tool.poetry.dependencies]',
            '[project]',
            '[tool.poetry]'
        ]
        current_section = None
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('['):
                current_section = line.lower()
                in_deps = current_section in dep_sections
                continue
            if in_deps:
                # For [project] and [tool.poetry], look for dependencies = [ ... ]
                if line.startswith('dependencies') and '=' in line:
                    # dependencies = ["foo>=1.0", "bar"]
                    dep_list = DependencyParser._extract_list_from_line(line)
                    for dep in dep_list:
                        name, version = DependencyParser._split_dep_string(dep)
                        deps[name.lower()] = version
                # For [project.dependencies] and [tool.poetry.dependencies], parse key = value
                elif '=' in line:
                    # foo = ">=1.0" or foo = {version = ">=1.0", extras = ["security"]}
                    key, val = [x.strip() for x in line.split('=', 1)]
                    name = key.strip('"')
                    val = val.strip()
                    if val.startswith('{') and val.endswith('}'):  # Inline table
                        version = DependencyParser._extract_version_from_inline_table(val)
                        deps[name.lower()] = version
                    else:
                        version = val.strip('"')
                        deps[name.lower()] = version if version else None
        return deps

    @staticmethod
    def _extract_list_from_line(line: str) -> List[str]:
        # Extracts a list from a line like: dependencies = ["foo>=1.0", "bar"]
        m = re.search(r'\[(.*)\]', line)
        if not m:
            return []
        items = m.group(1).split(',')
        result = []
        for item in items:
            item = item.strip().strip('"').strip("'")
            if item:
                result.append(item)
        return result

    @staticmethod
    def _split_dep_string(dep: str) -> Tuple[str, Optional[str]]:
        # Splits 'foo[extra]>=1.0; marker' into ('foo', '>=1.0')
        # Remove environment markers
        dep = dep.split(';', 1)[0].strip()
        # Remove extras
        m = re.match(r'^([A-Za-z0-9_.\-]+)(\[[A-Za-z0-9_,\-]+\])?\s*([=<>!~]=.+)?$', dep)
        if m:
            name = m.group(1)
            version = m.group(3).strip() if m.group(3) else None
            return name, version
        # If no version spec, try to split at first occurrence of comparison operator
        op_match = re.search(r'([=<>!~]=)', dep)
        if op_match:
            idx = op_match.start()
            name = dep[:idx].strip()
            version = dep[idx:].strip()
            # Remove extras from name if present
            name = re.sub(r'\[.*\]', '', name)
            return name, version
        # Otherwise, just base name
        name = dep
        # Remove extras if present
        name = re.sub(r'\[.*\]', '', name)
        return name, None

    @staticmethod
    def _extract_version_from_inline_table(val: str) -> Optional[str]:
        # Parses a TOML inline table string like {version = ">=2.25.0", extras = ["security"]}
        # Returns only the version string (ignoring extras/markers)
        # Find version = "..."
        m = re.search(r'version\s*=\s*([\'\"])([^\'\"]+)\1', val)
        if m:
            return m.group(2)
        # Sometimes version is unquoted (rare)
        m2 = re.search(r'version\s*=\s*([^,}\s]+)', val)
        if m2:
            return m2.group(1)
        # If no version, fallback to None
        return None
