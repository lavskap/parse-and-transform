# File Parse & Transform

Parse and transform a structured flat file into various formats: xml, xls, csv, txt.
All rules and settings for Parsing & Transformation are defined in json config file.

**Parsing**
- Defines certain fields that have to be transformed
- Restricts exported dataset with a list of values
- Validates certain fields against specific datatype (date, time, number)
- Reorders the exported fields
- Rejects unstructured parts of the file

**Transformation**
- Defines output file (path, extensions)
- Defines fields titles handling (include or not)
- Defines separator (eg for CSV)
- Defines rowid handling (add or not)

**Prerequisite**
- File should have defined structure (it can be some log file or migration structured data file)
- Fields separator should be defined, else blank will be used as a separator

**File example: <JobDaemon.log>**
![image](https://user-images.githubusercontent.com/80430638/221964288-662047b3-5ecb-4ffd-9ea8-0fc978ab005b.png)

**Sctructure**
(4 fields are defined):
 - Date (date)
 - Time (datetime)
 - MesageType (string)
 - MessageText (string)
Separator is Blank (null)
Config file <flat.json>

**Transformation settings example**
![image](https://user-images.githubusercontent.com/80430638/221964664-07f0d22c-00ff-4f68-bb2d-f2a434caf183.png)
Defines the data export settings (eg: export type, filenames, files elements, some other constraints)

**- input:** hash, that describes input file to be transformed (filename and fields separator, if any)

**- filename:** input filename. If no path provided then path is current dir, ie "./"

**- separator:** fields separator of input file, possible values: (“/t“ - tab, “|“ - pipe, null - blank)

**- path:** directory, where all output files will be stored (used, if not explicitly set per type hash 
below)
 - it is possible to use UNIX (“/“) style (it will be converted to Win style if running from Win)
 - if path starts with root (/work/) this will be automatically substituted with c:\work in Win
 
**- output:** hash, that defines exported type's setting. Keys in types hashes are not mandatory.
 
 *-filename:* output filename. If not defined, input filename is used with extension (ext). If file
 is defined, but without full dir, then global path in previous key (path) will be used
 
 *-incl_titles:* includes fields titles, defined in fields/title setting (see Parsing Rules below) 
 true => export also fields titles in exported file
 false => export data without titles (default)
 
 *-ext:* file extension. Used only if filename is not provided explicitly. If ext key is not given, 
 then “type“ is used as extension (ie for xls: extension will be xls and not xlsx)
 
 *-skip:* avoid exporting
 true => skip exporting to the given format
 false => do export (default)
 
 *-separator:* fields separator on output file (utilized only in csv export). Default: blank
 
 *-element:* xml root element name (default: Log)
 
 *-SubElement:* xml subelement name (default: Data)

**- incl_rowid:** add extra field “rowid“ (row counter) as the first column in the exported file
 true => add rowid fields in the beginning
 false => do not add rowid and leave as it is (default)
