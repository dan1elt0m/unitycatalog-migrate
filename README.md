# Unity Catalog Migrator

Unity Catalog Migrator is a tool to migrate catalogs, schemas, and tables from Databricks to Unity Catalog.

## Features

- Migrate catalogs from Databricks to Unity Catalog
- Migrate schemas from Databricks to Unity Catalog
- Migrate tables from Databricks to Unity Catalog

## Requirements

- Python 3.9 or higher
- Databricks SDK
- Typer
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
ucm databricks migrate-catalog --names catalog1 catalog2 --profile <databricks-profile> 
```

### Migrate Schemas
```shell
ucm databricks migrate-schemas --catalog catalog1 --profile <databricks-profile> 
```

### Migrate Tables
```shell
ucm databricks migrate-tables --catalog catalog1 --schema schema1 --profile <databricks-profile>  
```