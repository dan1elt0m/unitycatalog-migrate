import os
import pytest_asyncio
from testcontainers.core.container import DockerContainer
import logging
from testcontainers.core.waiting_utils import wait_for_logs
from unitycatalog.client import (
    Configuration,
    ApiClient,
    CatalogsApi,
    SchemasApi,
    TablesApi,
    CreateCatalog,
    CreateSchema,
)

logging.basicConfig(level=logging.INFO)

version = "0.2.1"
unity_catalog_container = DockerContainer(f"godatadriven/unity-catalog:{version}")


@pytest_asyncio.fixture(scope="function")
def unity_catalog():
    unity_catalog_container.with_exposed_ports(8080).start()
    wait_for_logs(unity_catalog_container, version, 30)
    yield
    unity_catalog_container.stop()


@pytest_asyncio.fixture(scope="function")
async def api_client(unity_catalog) -> ApiClient:
    logging.debug("Getting exposed port...")
    port = unity_catalog_container.get_exposed_port(8080)
    logging.debug(f"Exposed port: {port}")
    host_url = f"http://{unity_catalog_container.get_container_host_ip()}:{port}/api/2.1/unity-catalog"
    os.environ["UC_HOST_URL"] = host_url
    config = Configuration(host=host_url)
    yield ApiClient(config)


@pytest_asyncio.fixture(scope="function")
async def catalogs_api(api_client) -> CatalogsApi:
    async with api_client as client:
        yield CatalogsApi(client)


@pytest_asyncio.fixture(scope="function")
async def schemas_api(api_client) -> SchemasApi:
    yield SchemasApi(api_client)


@pytest_asyncio.fixture(scope="function")
async def tables_api(api_client) -> TablesApi:
    yield TablesApi(api_client)


@pytest_asyncio.fixture(scope="function")
async def test_catalog(catalogs_api):
    yield await catalogs_api.create_catalog(
        CreateCatalog(name="test_catalog", comment="Test Catalog")
    )


@pytest_asyncio.fixture(scope="function")
async def test_schema(schemas_api, test_catalog):
    yield await schemas_api.create_schema(
        CreateSchema(
            catalog_name="test_catalog", name="test_schema", comment="Test Catalog"
        )
    )
