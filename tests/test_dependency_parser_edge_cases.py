import unittest
from python_sdk_version_skew_reporter.dependency_parser import DependencyParser

class TestDependencyParserEdgeCases(unittest.TestCase):
    def test_requirements_txt_with_extras(self):
        content = """
        requests[security]==2.25.1
        numpy>=1.19.0; python_version<'3.10'
        pandas
        # comment
        flask[async]>=2.0.0; platform_system=='Linux'
        """
        deps = DependencyParser.parse_requirements_txt(content)
        # Extras and environment markers should not break parsing
        self.assertIn('requests', deps)
        self.assertEqual(deps['requests'], '==2.25.1')
        self.assertIn('numpy', deps)
        self.assertEqual(deps['numpy'], '>=1.19.0')
        self.assertIn('pandas', deps)
        self.assertIsNone(deps['pandas'])
        self.assertIn('flask', deps)
        self.assertEqual(deps['flask'], '>=2.0.0')

    def test_pyproject_toml_with_extras_and_markers(self):
        content = '''
[project.dependencies]
requests = {version = ">=2.25.0", extras = ["security"]}
numpy = {version = ">=1.19.0", markers = "python_version<'3.10'"}
pandas = ">=1.2.0"

[tool.poetry.dependencies]
flask = {version = ">=2.0.0", extras = ["async"], markers = "platform_system=='Linux'"}
pytest = "^6.2.5"
'''
        deps = DependencyParser.parse_pyproject_toml(content)
        # Should extract at least the base package names and version specs
        self.assertIn('requests', deps)
        self.assertEqual(deps['requests'], '>=2.25.0')
        self.assertIn('numpy', deps)
        self.assertEqual(deps['numpy'], '>=1.19.0')
        self.assertIn('pandas', deps)
        self.assertEqual(deps['pandas'], '>=1.2.0')
        self.assertIn('flask', deps)
        self.assertEqual(deps['flask'], '>=2.0.0')
        self.assertIn('pytest', deps)
        self.assertEqual(deps['pytest'], '^6.2.5')

    def test_requirements_txt_with_complex_lines(self):
        content = """
        # Multiple extras and markers
        fastapi[all,dev]>=0.70.0; python_version>='3.7'
        uvicorn[standard]==0.15.0
        """
        deps = DependencyParser.parse_requirements_txt(content)
        self.assertIn('fastapi', deps)
        self.assertEqual(deps['fastapi'], '>=0.70.0')
        self.assertIn('uvicorn', deps)
        self.assertEqual(deps['uvicorn'], '==0.15.0')

    def test_pyproject_toml_dependencies_array_with_extras(self):
        content = '''
[project]
dependencies = [
  "requests[security]>=2.25.0",
  "numpy>=1.19.0; python_version<'3.10'",
  "flask[async]>=2.0.0; platform_system=='Linux'"
]
'''
        deps = DependencyParser.parse_pyproject_toml(content)
        self.assertIn('requests', deps)
        self.assertEqual(deps['requests'], '>=2.25.0')
        self.assertIn('numpy', deps)
        self.assertEqual(deps['numpy'], '>=1.19.0')
        self.assertIn('flask', deps)
        self.assertEqual(deps['flask'], '>=2.0.0')

if __name__ == '__main__':
    unittest.main()
