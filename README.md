# Unity Catalog Migrator

Unity Catalog Migrator is a tool to migrate catalogs, schemas, and tables from Databricks to Unity Catalog.

## Requirements

- Python 3.9 or higher
- Databricks configuration file: https://docs.databricks.com/en/dev-tools/auth/config-profiles.html 

## Installation

To install the Unity Catalog Migrator, you can use the following commands:

```shell
pip install unitycatalog-migrate
```

## Usage

### Migrate Catalogs
To migrate catalogs, use the following command:

```shell
ucm migrate-catalog NAMES... --profile <databricks-profile> 
```

### Migrate Schemas
```shell
ucm migrate-schema NAMES... --profile <databricks-profile> 
```

### Migrate Tables
```shell
ucm migrate-table NAMES..  --profile <databricks-profile>  
```

## Configuration

The Unity Catalog Migrator uses the following environment variables:
- UC_HOST_URL: The URL of the Unity Catalog server. Default is `http://localhost:8080/api/2.1/unity-catalog`.
- UC_TOKEN: The token to authenticate with the Unity Catalog server. Default is `None`.

## Example
```shell
# Use Databricks CLI to get tables from catalog1.schema1 and migrates
table_names=$(databricks tables list catalog1 schema1 --profile DATABRICKS_TEST | awk 'NR>1 {print $1}' | paste -sd ' ' -)

# Migrate the tables to Unity Catalog using ucm
echo $table_names | xargs ucm migrate-table --profile DATABRICKS_TEST 
```

## Remarks
### Not supported:
- system tables 
- Variant datatype

## Contributing
- Contributions are welcome. Fork and make a PR and I'll take a look asap.
