class Parse:
    """
    Translates settings from JSON format into set of list and dictionaries.
    Parsing and validation if the config file
    """

    def __init__(self, conf, conf_dict):

        # Parse Conf Dictionary
        self.conf = conf
        self.conf_dict = conf_dict
        self.error_msg = None
        self.input = None
        self.path = None
        self.output = None
        self.fields = None
        self.fields_id = None
        self.fields_export = None
        self.fields_filter = None
        self.fields_title = None
        self.fields_title_sorted = None
        self.fields_id_exp = None
        self.fields_title_exp = None
        self.fields_type = None

    def validate_flat_config(self):
        # parsing rules

        # input key to be parsed
        if not self.conf_dict.get('input'):
            self.error_msg = f'"input" key is not defined in {self.conf}'
            return False
        # input filename should be provided
        elif not self.conf_dict.get('input').get("filename"):
            self.error_msg = f'"input filename" field is not defined in input key of {self.conf}'
            return False
        else:
            self.input = self.conf_dict.get('input')  # dictionary of input data

        # output path to be parsed
        if self.conf_dict.get('path'):
            self.path = self.conf_dict.get("path")
        else:
            self.path = "./"

        # output file, if none than take name from input file
        if not self.conf_dict.get('output'):
            self.error_msg = f'"input" key is not defined in {self.conf}'
            return False
        else:
            self.output = self.conf_dict.get('output')  # list of dictionaries that define output formats

        # fields - list of fields settings in input file
        if not self.conf_dict.get('fields'):
            self.error_msg = f'"fields" field is not defined in {self.conf}'
            return False
        else:
            self.fields = self.conf_dict.get('fields')

        # check if all needed fields attribute filled
        if not all("id" in d for d in self.fields):
            self.error_msg = f'"id" field is not defined in "fields" tag in {self.conf} '
            return False
        if not all("title" in d for d in self.fields):
            self.error_msg = f'"title" field is not defined in "fields" tag in {self.conf}'
            return False
        elif not all("export" in d for d in self.fields):
            self.error_msg = f'"export" field is not defined in "fields" tag in {self.conf}'
            return False
        elif not all("filter" in d for d in self.fields):
            self.error_msg = f'"filter" field is not defined in "fields" tag in {self.conf}'
            return False
        elif not all("type" in d for d in self.fields):
            self.error_msg = f'"type" field is not defined in "fields" tag in {self.conf}'
            return False
        else:
            """
            file structure: field's title, visibility, filter/restriction, type validation
            attributes that are in list format with the same length as every line in parsed file
            """
            self.fields_id = (list(map(lambda d: d['id'], self.fields)))  # list of sorted id
            self.fields_title = (list(map(lambda d: d['title'], self.fields)))  # list of titles
            self.fields_export = (list(map(lambda d: d['export'], self.fields)))  # transform or not
            self.fields_filter = (list(map(lambda d: d['filter'], self.fields)))  # restrict against str value
            self.fields_type = (list(map(lambda d: d['type'], self.fields)))  # type definition and validation

            # sort and filter based on self.fields_show
            self.fields_id_exp = [v[1] for v in zip(self.fields_export, self.fields_id) if v[0] is True]
            self.fields_title_exp = [v[1] for v in zip(self.fields_export, self.fields_title) if v[0] is True]

            """
            sort based on self.fields_id_shown
            eg: field_id_shown = [2,1,4]. field_name_shown = ["Date","MessageType","MessageText"]
            fields_name_sorted expected to be ["MessageType", "Date","MessageText"]
            """
            self.fields_title_sorted = [el for _, el in sorted(zip(self.fields_id_exp, self.fields_title_exp))]

            return True
