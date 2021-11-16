"""
Routines for transformation fata into different files
Performs validation of line, rejecting unstructured data
"""

# modules for data export
from openpyxl import Workbook
import csv
import xml.etree.ElementTree as Et

# modules for data validation
import time as str2time
from datetime import datetime as str2date

# os specific
import os
import ntpath


def is_date(vd, key_format):
    # date validation
    try:
        str2date.strptime(vd, key_format)
        return True
    except ValueError:
        return False


def is_time(vt, key_format):
    # time validation
    try:
        str2time.strptime(vt, key_format)
        return True
    except ValueError:
        return False


def is_number(vn, _):
    # number validation
    try:
        float(vn)
        return True
    except ValueError:
        return False


def validate_data(fields_type, line_lst):
    """
    record validation
    validate data based on fields / type key in config file
    do combine defined fields_type list, that is parse object attribute, and extracted line list
    eg. fields_type = [["date", "validate=yes", "%d.%m.%Y"], ["string", "validate=no", null]]
        line_lst = ["10.07.2019", "DEBUG"]
    z = [(["date", "validate=yes", "%d.%m.%Y"], "10.07.2019"), (["string", "validate=no", null], "DEBUG")]
    """
    z = list(zip(fields_type, line_lst))  # combine types list and extracted field's list
    if not line_lst:  # ignore empty lines
        return False

    """ 
    matching type defined in config with the type of extracted fields
    returns True if all elements in list are True
    eg: z = [(["date", "validate=yes", "%d.%m.%Y"], "10.07.2019"), (["string", "validate=no", null], "DEBUG")]
        x[0][0] = "date"
        x[1] = "10.07.2019"
        x[0][2] = "%d.%m.%Y"
        "is_" + x[0][0]](x[1], x[0][2] = is_date("10.07.2019","%d.%m.%Y")
    """
    return all(
        [
            globals()["is_" + x[0][0]](x[1], x[0][2])  # dynamic call to is_dat / is_time / is_number with format
            if x[0][1] == "validate=yes"  # do dynamic call above ONLY IF validate=yes
            else x[0][1] == "validate=no"  # if validate=no then it always returns True
            for x in z  # for all elements in combined list (see above)
        ]
    )


def process(parse, include_titles=False, include_rowid=False):
    # process the input file

    f = open(unx2win(parse.input.get("filename")), mode="r")  # Open input file

    rowid = 0
    if include_titles:  # First - return titles if needed (ie for xls, csv)
        if include_rowid:
            parse.fields_title_sorted.insert(0, "RowId")
        yield parse.fields_title_sorted

    # Now go through all the line in the file
    for line in f:
        # here create list from line string and format it based on config file fields
        line_lst = line.rstrip('\n').split(parse.input.get("separator"), len(parse.fields_id) - 1)

        z = zip(parse.fields_filter, line_lst)  # combined lists of filters and current list
        """
        do line validation: 
        type validation if defined and do a match against predefined filters
        return only those lines that get matched
        """
        if validate_data(parse.fields_type, line_lst) and all([True if v[0] is None else v[1] in v[0] for v in z]):
            # here remove the fields with export = false setting
            line_lst_exp = [v[1] for v in zip(parse.fields_export, line_lst) if v[0] is True]

            # here sort elements according to fields_id_shown
            line_lst_sorted = [el for _, el in sorted(zip(parse.fields_id_exp, line_lst_exp))]

            # if rowid to be added then adjust list
            if include_rowid:
                rowid += 1
                line_lst_sorted.insert(0, str(rowid))

            # return the list element, ie restructured line
            yield line_lst_sorted

    # close the file
    f.close()


def export(parse, key, val):
    """
    export to various types
    key is format type => txt, xls, csv or xml
    val is dictionary of setup for corresponding type (eg filename, skipping, separator, etc)
    """

    # first, check if export to specific type is to be skipped or not
    if val.get("skip"):
        print(f"Export to {key} was skipped")
        return

    # General settings
    # if ext is not explicitly set then take key as ext
    ext = val.get("ext") if val.get("ext") else key
    # take file name from config if provided, else use input filename with extension from config
    fn = val.get("filename") if val.get("filename") else os.path.basename(parse.input.get("filename")) + "." + ext

    # check if path exists
    fp = os.path.dirname(fn)
    if fp and not os.path.exists(unx2win(fp)):  # output filename provided with dir path which does not exist
        print(f"Export to {key} was not performed. Dir {fp} does not exist.")
        return
    elif not fp:  # output filename provided without dir path
        # check if path exists
        if not os.path.exists(unx2win(parse.path)):
            print(f"Output directory {unx2win(parse.path)} does not exist.")
            return False
        fn = os.path.join(unx2win(parse.path), fn)
    else:  # convert path style from unix to windows
        fn = unx2win(fn)

    # separator, if not defined then blank
    separator = val.get("separator") if val.get("separator") else " "

    # TXT
    if key == "txt":
        # open the file for writing
        f = open(fn, "w")

        # concatenate every list element from process with separator
        for ln in process(parse, val.get("incl_titles"), val.get("incl_rowid")):
            s = separator.join(map(str, ln))
            f.write(s + '\n')

        # save / close the file
        f.close()

    # XLS
    elif key == "xls":
        # create new spreadsheet
        book = Workbook()
        sheet = book.active

        # fill each list element from process into new spreadsheet
        for ln in process(parse, val.get("incl_titles"), val.get("incl_rowid")):
            sheet.append(ln)

        # save filled workbook
        book.save(fn)

    # CSV
    elif key == "csv":
        # open the file for writing
        f = open(fn, 'w', newline='')
        # defined csc conf
        w = csv.writer(f, delimiter=separator)

        # fill each list element from process into new spreadsheet
        for ln in process(parse, val.get("incl_titles"), val.get("incl_rowid")):
            w.writerow(ln)

        # save / close the file
        f.close()

    # XML
    elif key == "xml":
        # Init
        tree = None

        # take xml element name from config if provided, else use "Log"
        el_name = val.get("element") if val.get("element") else "Log"

        # create tree of elements
        el = Et.Element(el_name)

        # take xml sub element name from config if provided, else use "Data"
        sub_element = val.get("SubElement") if val.get("SubElement") else "Data"

        # loop through all list elements from process
        for ln in process(parse, val.get("incl_titles"), val.get("incl_rowid")):
            # create sub elements
            sub_el = Et.SubElement(el, sub_element)

            # go through each element in single list
            for i in range(len(parse.fields_title_sorted)):
                # populate data in subtree
                data = Et.SubElement(sub_el, parse.fields_title_sorted[i])
                data.text = str(ln[i])
            tree = Et.ElementTree(el)

        # save xml file
        tree.write(fn, encoding='utf-8', xml_declaration=True)

    # Print results
    print(f"Export to {key} was complete. File {fn}")


def usage(script):
    help_msg = f"""
Usage:

python {script} -c <config file>

Reads config file in json format and does corresponding parsing and transformation 
against the file provided in the config.

Example: 
python {script} -c ./flat.json
    reads flat.json from the current directory

python {script} -c ./conf/flat.json
    reads flat.json from "conf" subdirectory

python {script} -c c:\\\\work\\\\transformation\\\\flat.json
    reads flat.json from "c:\\work\\transformation" directory

"""
    print(help_msg)


def unx2win(path):
    # convert Unix style dir path to Windows style, eg: "/" into "\\"

    if os.name == "nt":
        new_path = path.replace(os.sep, ntpath.sep)  # replace \ with \\
        pl = list(map(lambda x: "\\" if x == "/" else x, list(new_path)))  # path string to list and replace / with \\
        pl[0] = pl[0].replace("\\", "c:\\")  # update first element to be c:\\ if original unix path started from root /
        return "".join(pl)  # back from updated list to path string
    else:
        return path


def validate_input_file(parse):
    # validate if input file exists

    # check if file exists
    try:
        cf = open(unx2win(parse.input["filename"]), mode="r")
        cf.close()
    except FileNotFoundError:
        parse.error_msg = f'Input file {unx2win(parse.input["filename"])} does not exist.'
        return False
    else:
        return True
