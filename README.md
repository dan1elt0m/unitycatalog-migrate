[![test](https://github.com/dan1elt0m/unitycatalog-migrate/actions/workflows/test.yml/badge.svg)](https://github.com/dan1elt0m/unitycatalog-migrate/actions/workflows/test.yml)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fdan1elt0m%2Funitycatalog-migrate%2Fmain%2Fpyproject.toml)

<p align="center">
    <b>🚀 UCM - OSS Unity Catalog Migration Assistant</b>
</p>> 

**Disclaimer: This project is unofficial and not affiliated with or endorsed by the official Unity Catalog team.**

UCM is a CLI that provides commands for migrating catalogs, schemas, and tables from Databricks to Unity Catalog. 


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
```shell
ucm migrate-catalog NAMES... --profile <databricks-profile> 
```

### Migrate Schemas
```shell
ucm migrate-schema FULL_NAMES... --profile <databricks-profile> 
```
where FULL_NAMES are in the format `catalog.schema`

### Migrate Tables
```shell
ucm migrate-table FULL_NAMES..  --profile <databricks-profile>  
```
where FULL_NAMES are in the format `catalog.schema.table`

## Configuration

The Unity Catalog Migrator uses the following environment variables:
- UC_HOST_URL: The URL of the Unity Catalog server. Default is `http://localhost:8080/api/2.1/unity-catalog`.
- UC_TOKEN: The token to authenticate with the Unity Catalog server. Default is `None`. You can also pass the token as
    an argument to the command.

## Example
```shell
# First migrate catalog and schema
ucm migrate-catalog catalog1 --profile DATABRICKS_TEST
ucm migrate-schema catalog1.schema1 --profile DATABRICKS_TEST

# Use Databricks CLI to get all tables of schema
table_names=$(databricks tables list catalog1 schema1 --profile DATABRICKS_TEST | awk 'NR>1 {print $1}' | paste -sd ' ' -)
# Migrate the tables to Unity Catalog using 
echo $table_names | xargs ucm migrate-table --profile DATABRICKS_TEST 
```

### Not supported:
- system tables 
- Variant datatype

### Wishlist
- migrate functions command
- migrate models command
- update existing tables (sync)

## Contributing
- Contributions are welcome. Please fork and make a PR and I'll take a look asap.
- Star the repo if you like it.
