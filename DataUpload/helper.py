# coding=utf-8
import uuid
from aetypes import Enum

import xlrd
from decimal import Decimal

from django.db import transaction

from ERP.models import Concept_Input, Unit, LineItem
from SalcedoERP.lib.SystemLog import SystemException, LoggingConstants


class FileInterface(object):
    """ Reads .xls files and converts them to lists.

    Attributes:
        file_path: the path of the file that must be read.

    """

    # The book from which the data will be read
    book = None

    def __init__(self, file_path):
        """ Inits the FileInterface object with a file.
        :param file_path: the path of the file with which the object will be initialized.
        """
        self.book = xlrd.open_workbook(file_path)

    def get_element_list(self):
        """ Obtains an list containing all the records of the first sheet of the object's file.
        :return: A list containing all the records of the first sheet of the object's file.
        """

        # Create empty array so that we fill it later.
        element_list = []

        # Get the first sheet
        sheet = self.book.sheet_by_index(0)

        # We start on row 1, because the established format does not include a header.
        i = 0
        while True:
            try:
                # Read the whole row at once
                elements = sheet.row_values(i);
                # Add the row to the list
                element_list.append(elements)
                i += 1
            except IndexError:
                # We're done reading.
                break

        # Return all the rows read.
        return element_list


class DBObject(object):
    """ Assists in saving information to the database, specifically for models:
        - LineItem
        - ConceptInput
    """

    def __init__(self, user_id):
        """ Initializes the DBObject instance.
        :param username: The username that will make changes to the database.
        """
        self.user_id = user_id

    class InputConstants(Enum):
        """ Contains a series of constants that help locate information of inputs on a record list.
        """
        # The following constants are the column numbers for different attributes of an Input instance
        LINE_ITEM_KEY_COL = 0
        LINE_ITEM_DESCRIPTION_COL = 1
        CONCEPT_KEY_COL = 2
        CONCEPT_DESCRIPTION_COL = 3
        UNIT_COL = 4
        QUANTITY_COL = 5
        UNIT_PRICE_COL = 6

    class ConceptConstants(Enum):
        """ Contains a series of constants that help locate information of concepts on a record list.
        """
        # The following constants are the column numbers for different attributes of a Concept instance
        LINE_ITEM_KEY_COL = 0
        LINE_ITEM_PARENT_COL = 1
        LINE_ITEM_DESCRIPTION_COL = 1
        CONCEPT_KEY_COL = 2
        CONCEPT_DESCRIPTION_COL = 3
        UNIT_COL = 4
        QUANTITY_COL = 5
        UNIT_PRICE_COL = 6

    class LineItemConstants(Enum):
        """ Contains a series of constants and methods that help locate information of line items on a record list.
        """
        # The following constants are the column numbers for different attributes of a Line Instance instance
        LINE_ITEM_PARENT_KEY_COL = 0
        LINE_ITEM_KEY_COL = 1
        LINE_ITEM_DESCRIPTION_COL = 2

        # Specifies the maximum level of nested Line Items that the specified project will have
        max_level = 0

        @classmethod
        def set_max_level(cls, record_list_length):
            """ Sets the maximum level of Line Items that the specified project will have
            :param record_list_length: The length of the first row of the file used for the upload of line items.
            :return: The maximum level of line items the specified project will have.
            """
            cls.max_level = record_list_length - 1

        @classmethod
        def get_max_level(cls):
            """ Gets the maximum level of line items the specified project will have.
            :return: The maximum level of line items the specified project will have.
            """
            return cls.max_level

        @classmethod
        def get_description(cls, record):
            """ Locates the description of a line item on a particular record and returns it.
            :param record: a line item record obtained from a file, in the form of a one-dimensional array.
            :return: The description of the line item associated with the record.
            """
            return record[cls.max_level]

        @classmethod
        def get_parent_key(cls, record):
            """ Locates the key of the parent of a line item on a particular record and returns it.
            :param record: a line item record obtained from a file, in the form of a one-dimensional array.
            :return: The key of the parent line item of the line item associated with the record, if it has one.
                     None, if the line item does not have a parent.
            """
            if record[cls.max_level - 2] == "":
                return None
            return record[cls.max_level - 2]

        @classmethod
        def get_key(cls, record):
            """ Locates the key of a line item on a particular record and returns it.
            :param record: a line item record obtained from a file, in the form of a one-dimensional array.
            :return: The key of the line item associated with the record.
            """
            return record[cls.max_level - 1]

    # The following constants help specify the type of information that will be read from the file.
    INPUT_UPLOAD = 0  # Input records will be read.
    CONCEPT_UPLOAD = 1  # Concept records will be read.
    LINE_ITEM_UPLOAD = 2  # Line Item records will be read.

    # In the database, the type of a Concept_Input must be a char equal to 'I' or 'C'. This dictionary helps get
    # such constants.
    CONCEPT_INPUT_TYPES = {
        INPUT_UPLOAD: 'I',
        CONCEPT_UPLOAD: 'C'
    }

    def save_all(self, file_path, model):
        """ Saves to the database all the records contained on a file.
        :param file_path: The path of the file from which the data will be read.
        :param model: The model to which the information on the file is associated. This model should be one of the
               following constants:
                    - INPUT_UPLOAD; if the data corresponds to inputs.
                    - CONCEPT_UPLOAD: if the data corresponds too concepts.
                    - LINE_ITEM_UPLOAD: if the data corresponds to line items.
        :raises ErrorDataUpload: In one of the following scenarios:
                - The file specified by file_path is not found.
                - The format of the file specified by file_path is not correct.
                - There's an inconsistency on the information provided.
                - The model specified is not one of the following constants:
                    - INPUT_UPLOAD; if the data corresponds to inputs.
                    - CONCEPT_UPLOAD: if the data corresponds too concepts.
                    - LINE_ITEM_UPLOAD: if the data corresponds to line items.
        """

        try:
            # Read the file.
            file_obj = FileInterface(file_path)
        except:
            # The file does not exist.
            raise ErrorDataUpload('Ha habido un problema leyendo el archivo', LoggingConstants.ERROR, self.user_id)

        # Obtain the element list for the file.
        record_list = file_obj.get_element_list()

        if model == self.CONCEPT_UPLOAD or model == self.INPUT_UPLOAD:
            # Handle concepts and inputs
            self.save_all_concept_input(record_list)
        elif model == self.LINE_ITEM_UPLOAD:
            # Handle line items
            self.save_all_line_items(record_list)
        else:
            raise ErrorDataUpload(
                'El parámetro model no es correcto. Este parámetro debe estar definido por una consante válida.',
                LoggingConstants.CRITICAL, self.user_id)

    def save_all_concept_input(self, record_list):
        folio = str(uuid.uuid4())

        try:
            for record in record_list:
                # print 'Single record:' + str(record)
                if record[0] != "":
                    self.save_concept_input(folio, record, Concept_Input)

        except Exception, e:
            # self.object_class.objects.filter(folio=folio).delete()
            raise e
        return folio

    def save_all_line_items(self, record_list):
        folio = str(uuid.uuid4())
        self.LineItemConstants.set_max_level(len(record_list[0]))

        try:
            for record in record_list:
                # print 'Single record:' + str(record)
                if record[self.LineItemConstants.get_max_level()] != "":
                    self.save_line_item(record)

        except Exception, e:
            # self.object_class.objects.filter(folio=folio).delete()
            raise e
        return folio

    def save_line_item(self, record):
        # First, we get each all the attributes.
        line_item_parent_key = self.LineItemConstants.get_parent_key(record)
        line_item_key = self.LineItemConstants.get_key(record)
        line_item_description = self.LineItemConstants.get_description(record)

        line_item_has_parent = line_item_parent_key is not None

        if line_item_has_parent:
            line_item_qs = LineItem.objects.filter(key=line_item_parent_key.upper())
            if line_item_parent_key is not None and len(line_item_qs) == 0:
                raise ErrorDataUpload('No existe la partida padre', LoggingConstants.ERROR, self.user_id)
            else:
                parent_id = line_item_qs[0].id
        else:
            parent_id = None

        line_item_obj = LineItem(key=line_item_key.upper(),
                                 project_id=2,
                                 parent_line_item_id=parent_id,
                                 description=line_item_description)
        # with transaction.atomic():
        line_item_obj.save()


'''
    Método save:
    Éste método guardará a la base de datos los objetos apoyándose del modelo y de la lista columns.
    Se leerán los atributos definidos por el modelo, y con ayuda de la lista columns se tomara el valor correcto.
    El tipo correcto se leerá desde el modelo.
'''


def save_concept_input(self, folio, record, model):
    # First, we get each all the attributes.
    line_item_key = record[self.ENUM_DICT[model].LINE_ITEM_KEY_COL]
    line_item_description = record[self.ENUM_DICT[model].LINE_ITEM_DESCRIPTION_COL].encode('utf-8')
    concept_key = record[self.ENUM_DICT[model].CONCEPT_KEY_COL].encode('utf-8')
    concept_description = record[self.ENUM_DICT[model].CONCEPT_DESCRIPTION_COL].encode('utf-8')
    unit = record[self.ENUM_DICT[model].UNIT_COL].encode('utf-8')
    quantity = Decimal(record[self.ENUM_DICT[model].QUANTITY_COL].replace(',', ''))
    unit_price = Decimal(record[self.ENUM_DICT[model].UNIT_PRICE_COL][1:].replace(',', ''))

    # print unit_price

    unit_qs = Unit.objects.filter(abbreviation=unit.upper())

    if len(unit_qs) == 0:
        unit_obj = Unit(abbreviation=unit.upper(),
                        quantification='C',
                        name=unit.upper())
        #with transaction.atomic():
        unit_obj.save()
    else:
        unit_obj = unit_qs[0]

    line_item_qs = LineItem.objects.filter(key=line_item_key.upper())

    if len(line_item_qs) == 0:
        line_item_obj = LineItem(key=line_item_key.upper(),
                                 project_id=2,
                                 parent_line_item=None,
                                 description=line_item_description)
        #with transaction.atomic():
        line_item_obj.save()
    else:
        line_item_obj = line_item_qs[0]

    concept_input = Concept_Input(
        line_item=line_item_obj,
        unit=unit_obj,
        key=concept_key,
        description=concept_description,
        quantity=quantity,
        unit_price=unit_price,
        type=self.CONCEPT_INPUT_TYPES[model]
    )
    #with transaction.atomic():
    concept_input.save()


class ErrorDataUpload(SystemException):
    def __init__(self, message, priority, user_id):
        SystemException.__init__(self, message, LoggingConstants.DATA_UPLOAD, priority, user_id)
