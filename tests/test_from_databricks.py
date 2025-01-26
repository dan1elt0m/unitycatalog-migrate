import pytest
from unittest.mock import patch, MagicMock

from databricks.sdk.service.catalog import (
    ColumnInfo,
    SchemaInfo,
    TableInfo,
    ColumnTypeName,
    TableType,
    DataSourceFormat,
)

from unitycatalog_migrate.from_databricks import (
    migrate_catalog,
    migrate_schema,
    migrate_table,
)


@pytest.mark.asyncio
@patch("unitycatalog_migrate.from_databricks.WorkspaceClient")
async def test_migrate_catalog(mock_workspace_client, catalogs_api):
    mock_workspace = MagicMock()
    mock_workspace.catalogs.get.return_value = MagicMock(
        name="test_catalog", comment="Test Catalog"
    )
    mock_workspace_client.return_value = mock_workspace

    result = await migrate_catalog(
        names=["test_catalog"], profile="default", token="test_token"
    )
    assert result is None
    mock_workspace.catalogs.get.assert_called_once_with("test_catalog")
    test_cat = await catalogs_api.get_catalog("test_catalog")

    assert test_cat.name == "test_catalog"
    assert test_cat.comment == "Test Catalog"


@pytest.mark.asyncio
@patch("unitycatalog_migrate.from_databricks.WorkspaceClient")
async def test_migrate_schema(mock_workspace_client, schemas_api, test_catalog):
    mock_workspace = MagicMock()
    mock_workspace.schemas.get.return_value = SchemaInfo(
        name="test_schema",
        full_name="test_catalog.test_schema",
        catalog_name="test_catalog",
        comment="Test Schema",
    )
    mock_workspace_client.return_value = mock_workspace

    result = await migrate_schema(names=["test_catalog.test_schema"])
    assert result is None
    mock_workspace.schemas.get.assert_called_once_with(
        full_name="test_catalog.test_schema"
    )
    test_schema = await schemas_api.get_schema(full_name="test_catalog.test_schema")

    assert test_schema.name == "test_schema"
    assert test_schema.catalog_name == "test_catalog"
    assert test_schema.comment == "Test Schema"


@pytest.mark.asyncio
@patch("unitycatalog_migrate.from_databricks.WorkspaceClient")
async def test_migrate_table(mock_workspace_client, tables_api, test_schema):
    mock_workspace = MagicMock()
    mock_workspace.tables.get.return_value = TableInfo(
        name="test_table",
        catalog_name="test_catalog",
        schema_name="test_schema",
        table_type=TableType.EXTERNAL,
        data_source_format=DataSourceFormat.DELTA,
        columns=[
            ColumnInfo(
                name="col1",
                type_name=ColumnTypeName.STRING,
                type_text="STRING",
                type_json='{"name":"col1","type":"string"}',
                comment="col1",
                position=0,
            )
        ],
        storage_location="",
        comment="Test Table",
        properties={},
    )
    mock_workspace_client.return_value = mock_workspace

    result = await migrate_table(["test_catalog.test_schema.test_table"])
    assert result is None
    mock_workspace.tables.get.assert_called_once_with(
        full_name="test_catalog.test_schema.test_table"
    )
    test_table = await tables_api.get_table(
        full_name="test_catalog.test_schema.test_table"
    )

    assert test_table.name == "test_table"
    assert test_table.catalog_name == "test_catalog"
    assert test_table.schema_name == "test_schema"
    assert test_table.comment == "Test Table"
