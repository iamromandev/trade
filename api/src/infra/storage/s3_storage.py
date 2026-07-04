from src.infra.storage.base import BaseFileStorage


class S3FileStorage(BaseFileStorage):
    def __init__(
        self,
        bucket: str,
        endpoint_url: str | None = None,
        region: str = "us-east-1",
        access_key_id: str | None = None,
        secret_access_key: str | None = None,
    ):
        self._bucket = bucket
        self._endpoint = endpoint_url
        self._region = region
        self._access_key = access_key_id
        self._secret_key = secret_access_key
        self._client = None

    async def _get_client(self):
        if self._client is None:
            import aioboto3

            session = aioboto3.Session()
            self._client = await session.client(
                "s3",
                endpoint_url=self._endpoint,
                region_name=self._region,
                aws_access_key_id=self._access_key,
                aws_secret_access_key=self._secret_key,
            ).__aenter__()
        return self._client

    async def put(self, key: str, content: bytes) -> str:
        self._validate_key(key)
        client = await self._get_client()
        ct = self._infer_content_type(key)
        await client.put_object(Bucket=self._bucket, Key=key, Body=content, ContentType=ct)
        return key

    async def get(self, key: str) -> bytes | None:
        self._validate_key(key)
        client = await self._get_client()
        try:
            obj = await client.get_object(Bucket=self._bucket, Key=key)
            return await obj["Body"].read()
        except Exception:
            return None

    async def delete(self, key: str) -> bool:
        self._validate_key(key)
        client = await self._get_client()
        try:
            await client.delete_object(Bucket=self._bucket, Key=key)
            return True
        except Exception:
            return False

    async def url(self, key: str) -> str:
        return f"s3://{self._bucket}/{key}"
