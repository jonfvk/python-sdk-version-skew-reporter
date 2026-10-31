from typing import Set, Dict, List, Optional

class HighRiskPackageHighlighter:
    """
    Identifies and highlights high-risk packages (e.g., SDKs) among version-skewed dependencies.
    """
    # A basic list of high-risk package name substrings (case-insensitive)
    # This can be extended or made configurable in the future.
    HIGH_RISK_KEYWORDS = [
        'sdk', 'client', 'api', 'boto3', 'google-cloud', 'azure', 'openai',
        'firebase', 'twilio', 'stripe', 'aws', 'gcp', 'adk', 'agentkit', 'insight',
        'datadog', 'sentry', 'segment', 'snowflake', 'bigquery', 'pandasai',
        'anthropic', 'vertexai', 'langchain', 'pinecone', 'weaviate', 'milvus',
        'elasticsearch', 'opensearch', 'supabase', 'prisma', 'neo4j', 'redis',
        'kafka', 'confluent', 'pubsub', 'rabbitmq', 'celery', 'airflow',
        'dagster', 'prefect', 'mlflow', 'huggingface', 'transformers', 'llama',
        'llamaindex', 'cohere', 'replicate', 'modal', 'ray', 'dask', 'fastapi',
        'grpc', 'protobuf', 'requests', 'httpx', 'aiohttp', 'pyjwt', 'authlib',
        'oauth', 'jwt', 'msal', 'okta', 'auth0', 'passport', 'passportjs',
        'passport-python', 'passport-sdk', 'passport-client', 'passport-api',
    ]

    @classmethod
    def is_high_risk(cls, package_name: str) -> bool:
        """
        Returns True if the package name matches any high-risk keyword.
        """
        name = package_name.lower()
        for kw in cls.HIGH_RISK_KEYWORDS:
            if kw in name:
                return True
        return False

    @classmethod
    def highlight_skewed_packages(
        cls,
        skewed_packages: Dict[str, Set[Optional[str]]]
    ) -> List[str]:
        """
        Returns a list of package names from skewed_packages that are high-risk.
        """
        return [pkg for pkg in skewed_packages if cls.is_high_risk(pkg)]

    @classmethod
    def annotate_skew_details(
        cls,
        skew_details: List[tuple]
    ) -> List[dict]:
        """
        Given skew_details [(package_name, [(source, version_spec), ...]), ...],
        returns a list of dicts with 'package', 'is_high_risk', and 'sources'.
        """
        result = []
        for pkg, sources in skew_details:
            result.append({
                'package': pkg,
                'is_high_risk': cls.is_high_risk(pkg),
                'sources': sources
            })
        return result
