# File Parse & Transform

Parse and transform a structured flat file into various formats: xml, xls, csv, txt.
All rules and settings for Parsing & Transformation are defined in json config file.

**Parsing:
- Defines certain fields that have to be transformed
- Restricts exported dataset with a list of values
- Validates certain fields against specific datatype (date, time, number)
- Reorders the exported fields
- Rejects unstructured parts of the file

Read [Official Docu](https://squidfunk.github.io/mkdocs-material/getting-started/)

**Transformation:
- Defines output file (path, extensions)
- Defines fields titles handling (include or not)
- Defines separator (eg for CSV)
- Defines rowid handling (add or not)

**Prerequisite:
- File should have defined structure (it can be some log file or migration structured data file)
- Fields separator should be defined, else blank will be used as a separator

**File example: <JobDaemon.log>

