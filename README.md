# Unity Catalog Migrate

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
```shell
ucm databricks migrate-catalog catalog1 catalog2 --profile <databricks-profile> 
```

### Migrate Schemas
```shell
ucm databricks migrate-schemas catalog1.schema1 catalog1.schema2 --profile <databricks-profile> 
```

### Migrate Tables
```shell
ucm databricks migrate-tables catalog1.schema1.table1 catalog1.schema1.table2  --profile <databricks-profile>  
```

Unity Catalog doesnt support:
- managed tables
- variant datatype
