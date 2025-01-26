import os

from databricks.sdk import WorkspaceClient
from unitycatalog.client import (
    ApiClient,
    Configuration,
    CatalogsApi,
    SchemasApi,
    CreateSchema,
    CreateCatalog,
    TablesApi,
    CreateTable,
    ColumnInfo,
)

_api_instance: ApiClient | None = None


class SystemCatalogError(Exception):
    def __init__(self, message="Cannot migrate system catalog"):
        super().__init__(message)


def get_host_url() -> str:
    """Get the Unity Catalog host URL.

    Returns:
        str: The Unity Catalog host URL. Defaults to http://localhost:8080/api/2.1/unity-catalog.

    """
    if host_url := os.environ.get("UC_HOST_URL"):
        return host_url

    return "http://localhost:8080/api/2.1/unity-catalog"


def get_uc_client(token: str = None) -> ApiClient:
    global _api_instance
    if _api_instance is None or _api_instance.rest_client.pool_manager.closed:
        config = Configuration(host=get_host_url())
        _api_instance = ApiClient(
            configuration=config,
            header_name="Authorization",
            header_value=f"Bearer {token}",
        )
    return _api_instance


async def create_catalog(
    workspace_client: WorkspaceClient, catalogs_api: CatalogsApi, name: str
):
    """Create a catalog in Unity Catalog"""
    if name == "system":
        raise SystemCatalogError
    c = workspace_client.catalogs.get(name)
    await catalogs_api.create_catalog(CreateCatalog(name=name, comment=c.comment))


async def create_schema(
    workspace_client: WorkspaceClient, schemas_api: SchemasApi, name: str
):
    """Create a schema in Unity Catalog"""
    s = workspace_client.schemas.get(full_name=name)
    if s.catalog_name == "system":
        raise SystemCatalogError()
    await schemas_api.create_schema(
        CreateSchema(
            name=s.name,
            catalog_name=s.catalog_name,
            comment=s.comment,
            properties=s.properties,
        )
    )


async def create_table(
    workspace_client: WorkspaceClient, tables_api: TablesApi, name: str
):
    """Create a table in Unity Catalog"""
    t = workspace_client.tables.get(full_name=name)
    if t.catalog_name == "system":
        raise SystemCatalogError
    await tables_api.create_table(
        CreateTable(
            name=t.name,
            catalog_name=t.catalog_name,
            schema_name=t.schema_name,
            table_type=t.table_type.value,
            data_source_format=t.data_source_format.value,
            columns=[ColumnInfo.model_validate(c.as_dict()) for c in t.columns],
            storage_location=t.storage_location,
            comment=t.comment,
            properties=t.properties,
        )
    )
