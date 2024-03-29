# File Parse & Transform

Parse and transform a structured flat file into various formats: xml, xls, csv, txt.
All rules and settings for Parsing & Transformation are defined in json config file.

***Parsing***
- Defines certain fields that have to be transformed
- Restricts exported dataset with a list of values
- Validates certain fields against specific datatype (date, time, number)
- Reorders the exported fields
- Rejects unstructured parts of the file

***Transformation***
- Defines output file (path, extensions)
- Defines fields titles handling (include or not)
- Defines separator (eg for CSV)
- Defines rowid handling (add or not)

**Prerequisite**
- File should have defined structure (it can be some log file or migration structured data file)
- Fields separator should be defined, else blank will be used as a separator

***File example: <JobDaemon.log>***

![image](https://user-images.githubusercontent.com/80430638/221964288-662047b3-5ecb-4ffd-9ea8-0fc978ab005b.png)

***Sctructure***
**- 4 fields are defined:**
   - Date (date)
   - Time (datetime)
   - MesageType (string)
   - MessageText (string)

> Separator is Blank (null)

> Config file <flat.json>

***Transformation settings example***

![image](https://user-images.githubusercontent.com/80430638/221964664-07f0d22c-00ff-4f68-bb2d-f2a434caf183.png)

Defines the data export settings (eg: export type, filenames, files elements, some other constraints):

**- input:** hash, that describes input file to be transformed (filename and fields separator, if any)

**- filename:** input filename. If no path provided then path is current dir, ie "./"

**- separator:** fields separator of input file, possible values: (“\t“ - tab, “|“ - pipe, null - blank)

**- path:** directory, where all output files will be stored (used, if not explicitly set per type hash below)
 - it is possible to use UNIX (“/“) style (it will be converted to Win style if running from Win)
 - if path starts with root (/work/) this will be automatically substituted with c:\work in Win
 
**- output:** hash, that defines exported type's setting. Keys in types hashes are not mandatory.
 
 - *filename:* output filename. If not defined, input filename is used with extension (ext). If file is defined, but without full dir, then global path in previous key (path) will be used
 
 - *incl_titles:* includes fields titles, defined in fields/title setting (see Parsing Rules below) 
   - **true =>** export also fields titles in exported file
   - **false =>** export data without titles (default)
 
 - *ext:* file extension. Used only if filename is not provided explicitly. If ext key is not given, then “type“ is used as extension (ie for xls: extension will be xls and not xlsx)
 
 - *skip:* avoid exporting
   - **true =>** skip exporting to the given format
   - **false =>** do export (default)
 
 - *separator:* fields separator on output file (utilized only in csv export). Default: blank
 
 - *element:* xml root element name (default: Log)
 
 - *SubElement:* xml subelement name (default: Data)

**- incl_rowid:** add extra field “rowid“ (row counter) as the first column in the exported file
   - **true =>** add rowid fields in the beginning
   - **false =>** do not add rowid and leave as it is (default)

***Parse settings***

![image](https://user-images.githubusercontent.com/80430638/221968574-1a460224-b1bf-4f55-8880-cd790b4298a2.png)

Defines the dataset to be transformed, with validation rules and data restriction. All settings are wrapped in the list of fields. The fields in the list are sorted based on defined file structure. Every field has its out setting/rule as a hash, that handles parsing. All keys are mandatory.

**- id:** sort no that handles field's position in the exported file

**- title:** field's title, that can be included in export (see incl_title key in Transformation rules)

**- export:** decides if the field should be transferred
   - **true =>** export the given field
   - **false =>** do not export

**- filter:** list of values, restrict the exported data and defines the dataset. From the example above: Export where Date = 10.07.2019 AND MessageType in ('INFO', 'ERROR'). If export is null then no restriction applied against the given field

**- type:** defines field's type and validation settings. This helps to reject all unstructered part of file (as in the sample input file, seen on the first page).
   - **validate=yes =>** validate the given field value against type and format
   - **validate=no =>** do not validate the field (all rows will go through)

***Setup the environmen***
- Python 3.9
- for xls integration, install openpyxl module (all other used modules are part of python installation)
- create /work/transformation and put there flat.json, parse.py, transform.py and main.py source files
- create subdirs: ./input and ./output
![image](https://user-images.githubusercontent.com/80430638/221971016-4c0745b8-e2bc-4567-9b3c-0a25d0964eae.png)
- put JobDaemon.log file into ./input directory
![image](https://user-images.githubusercontent.com/80430638/221971793-76462985-c54a-48da-85f6-01b95fe7b544.png)
- run the script
![image](https://user-images.githubusercontent.com/80430638/221972038-f1dfcad6-378b-4951-9454-4c307c9d4a1f.png)
![image](https://user-images.githubusercontent.com/80430638/221972089-04ecda52-19ac-4e80-b1d9-5dd4e0fd9493.png)

> Results:
- XLS
![image](https://user-images.githubusercontent.com/80430638/221973581-6f65c7e9-0ec9-49d3-ac4f-00d5334ce3b6.png)
- Flat
![image](https://user-images.githubusercontent.com/80430638/221973760-03df3bb6-f714-4f2c-9d44-81c80d4fe49b.png)
- XML
![image](https://user-images.githubusercontent.com/80430638/221973892-608bf780-419e-40f9-baf0-ee910ed094bf.png)





