from typing import Dict, Set, Optional, List, Tuple
from .high_risk import HighRiskPackageHighlighter

class RemediationSuggester:
    """
    Suggests remediation steps for packages with version skew.
    Consumes skewed_packages and skew_details as produced by VersionSkewAggregator.
    """
    def __init__(
        self,
        skewed_packages: Dict[str, Set[Optional[str]]],
        skew_details: List[Tuple[str, List[Tuple[str, Optional[str]]]]]
    ):
        self.skewed_packages = skewed_packages
        self.skew_details = skew_details

    def suggest(self) -> str:
        """
        Returns a formatted string with remediation suggestions for each skewed package.
        High-risk packages are highlighted with extra urgency.
        """
        if not self.skewed_packages:
            return "No remediation needed."
        lines = ["Remediation Suggestions:"]
        high_risk = set(HighRiskPackageHighlighter.highlight_skewed_packages(self.skewed_packages))
        for pkg, sources in self.skew_details:
            is_high_risk = pkg in high_risk
            lines.append(f"- {pkg}{' [HIGH-RISK]' if is_high_risk else ''}:")
            lines.append("  Detected multiple versions:")
            versions = {ver if ver is not None else "(unspecified)" for _, ver in sources}
            lines.append(f"    {', '.join(sorted(versions))}")
            lines.append("  Sources:")
            for source, ver in sources:
                ver_str = ver if ver is not None else "(unspecified)"
                lines.append(f"    {source}: {ver_str}")
            lines.append("  Suggested actions:")
            lines.extend(self._remediation_steps(pkg, sources, is_high_risk))
        return "\n".join(lines)

    def _remediation_steps(self, pkg: str, sources: List[Tuple[str, Optional[str]]], is_high_risk: bool) -> List[str]:
        """
        Returns a list of remediation steps for a single package.
        """
        steps = []
        if is_high_risk:
            steps.append("    * URGENT: Unify to a single version if possible.")
            steps.append("    * Review SDK/library release notes for breaking changes.")
        else:
            steps.append("    * Unify to a single version specifier across all files.")
        steps.append("    * Remove or update duplicate/conflicting entries in dependency files.")
        steps.append("    * If using extras or environment markers, ensure they are consistent.")
        steps.append("    * Run your test suite after making changes to confirm stability.")
        return steps
