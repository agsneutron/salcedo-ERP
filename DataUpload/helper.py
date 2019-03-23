# coding=utf-8
import uuid

from django.utils.encoding import python_2_unicode_compatible

import django
import xlrd
from decimal import Decimal

from _mysql_exceptions import IntegrityError
from django.db import transaction
from django.db.models import Q, Count

from ERP.models import Concept_Input, Unit, LineItem, Project, ContratoContratista, ContractConcepts, Estimate
from SalcedoERP.lib.SystemLog import SystemException, LoggingConstants

import locale

#locale.setlocale(locale.LC_ALL, 'en_CA.UTF-8')
#locale.setlocale(locale.LC_ALL, 'en_CA.UTF-8')


# locale.currency(1000, grouping=True)
# español para windows
#locale.setlocale(locale.LC_ALL, "")



# Mac
#locale.setlocale(locale.LC_ALL, 'en_CA.UTF-8')


# español para linux
#locale.setlocale(locale.LC_ALL, "es_MX.utf8")


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
        self.book = xlrd.open_workbook(file_contents=file_path.read())

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


@python_2_unicode_compatible
class DBObject(object):
    """ Assists in saving information to the database, specifically for models:
        - LineItem
        - ConceptInput
    """

    def __str__(self):
        return 'dbobj'

    def __init__(self, user_id):
        """ Initializes the DBObject instance.
        :param username: The username that will make changes to the database.
        """

        self.user_id = user_id

    class InputConstants:
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

    class ConceptConstants:
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

    class LineItemConstants:
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

            print 'max level: ' + str(record_list_length - 1)
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
        def get_top_parent_key(cls, record):
            """ Locates the key of the parent of a line item on a particular record and returns it.
            :param record: a line item record obtained from a file, in the form of a one-dimensional array.
            :return: The key of the parent line item of the line item associated with the record, if it has one.
                     None, if the line item does not have a parent.
            """

            for i in range(0, cls.max_level - 1):
                if record[i] != "":
                    return record[i]

            return None

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

    def save_all(self, file_path, model, project_id=None):
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

        try:

            if model == self.CONCEPT_UPLOAD or model == self.INPUT_UPLOAD:
                # Handle concepts and inputs
                self.save_all_concept_input(record_list, model, project_id)
            elif model == self.LINE_ITEM_UPLOAD:
                # Handle line items
                print 'the project id is: ' + str(project_id)
                self.save_all_line_items(record_list, project_id)
            else:
                raise ErrorDataUpload(
                    u'El parámetro model no es correcto. Este parámetro debe estar definido por una consante válida.',
                    LoggingConstants.CRITICAL, self.user_id)
        except django.db.utils.IntegrityError as e:

            raise e

    def save_all_concept_input(self, record_list, model, project_id):
        """ Save a set of concept or input records
        :param record_list: list of concepts or inputs.
        """
        try:
            for record in record_list:
                # Iterate over each record
                if record[0] != "":
                    # Validate that the record is not empty
                    # Save the record

                    self.save_concept_input(record, model, project_id)

        except Exception, e:
            raise e

    def save_all_line_items(self, record_list, project_id):

        print 'Saving all line_items'
        self.LineItemConstants.set_max_level(len(record_list[0]))

        try:
            for record in record_list:

                print record

                if record[self.LineItemConstants.get_max_level()] != "":
                    print 'will save'
                    self.save_line_item(record, project_id)

        except Exception, e:
            raise e

    def save_line_item(self, record, project_id):
        # First, we get each all the attributes.
        line_item_parent_key = self.LineItemConstants.get_parent_key(record)
        line_item_top_parent_key = self.LineItemConstants.get_top_parent_key(record)
        line_item_key = self.LineItemConstants.get_key(record)
        line_item_description = self.LineItemConstants.get_description(record)

        line_item_has_parent = line_item_parent_key is not None

        parent_id = None
        top_parent_id = None

        # If the file defines a parent for the line item, we will check if it exists.
        if line_item_has_parent:
            line_item_qs = LineItem.objects.filter(Q(key=str(line_item_parent_key).upper().replace('.0', '')) & Q(project_id=project_id))
            if line_item_parent_key is not None and len(line_item_qs) == 0:
                raise ErrorDataUpload(
                    'No existe la partida padre con clave ' + str(line_item_parent_key).upper().replace('.0', '') + ' para la partida ' + line_item_key + '.',
                    LoggingConstants.ERROR, self.user_id)
            else:
                parent_id = line_item_qs[0].id
                print '1 el padre es ' + str(line_item_qs[0].id)

            # Now we'll check if the top parent exists
            if line_item_top_parent_key is not None:
                line_item_qs = LineItem.objects.filter(Q(key=str(line_item_top_parent_key).upper().replace('.0', '')) & Q(project_id=project_id))
                if line_item_top_parent_key is not None and len(line_item_qs) == 0:
                    raise ErrorDataUpload(
                        'No existe la partida padre con clave ' + str(line_item_top_parent_key).upper().replace('.0', '') + ' para la partida ' + line_item_key + '.',
                        LoggingConstants.ERROR, self.user_id)
                else:
                    top_parent_id = line_item_qs[0].id

        else:
            top_parent_id = None

        # Now we will validate that a line item with a duplicated key is not being added.
        # We will do that by first checking if the key already exists on the database.
        # If the key already exists, we have to make sure the description is also the same.

        line_item_validation_qs = LineItem.objects.filter(Q(key=str(line_item_key).upper().replace('.0', '')) & Q(project_id=project_id))
        if len(line_item_validation_qs) != 0:
            # The key already exists. Make sure the description is the same for both instances.
            old_description = line_item_validation_qs[0].description
            new_description = line_item_description


            print 'there were items on the validation qs'
            print line_item_validation_qs[0]

            if old_description != new_description:
                project_key = Project.objects.filter(Q(pk=project_id))[0].key

                raise ErrorDataUpload(
                    u"Problema al guardar la partida " + str(line_item_key).upper().replace('.0', '') + u" para el proyecto " + project_key
                    + u". Esta partida ya existe y se intentó agregar con una descripción diferente. La operación ha sido cancelada.",
                    LoggingConstants.ERROR, self.user_id)

        else:
            line_item_obj = LineItem(key=str(line_item_key).upper().replace('.0', ''),
                                     project_id=project_id,
                                     parent_line_item_id=parent_id,
                                     top_parent_line_item_id=top_parent_id,
                                     description=line_item_description)
            line_item_obj.save()
            print 'saved line item ----- '

    def concept_has_been_estimated(self, concept_id):
        # Check if there are contracts with the concept
        contracts = ContractConcepts.objects.filter(concept_id=concept_id).values('contractlineitem__contrato_id')

        if concept_id == 3792:
            debug = True
        else:
            debug = False

        if debug:
            print '-----'
            print 'Contracts:'
            print contracts

        for contract in contracts:
            # Check if there are estimates with the contract
            contract_id = contract['contractlineitem__contrato_id']
            estimates = Estimate.objects.filter(contractlineitem__contrato_id=contract_id)

            if len(estimates) > 0:
                return True

        return False

    '''
        Método save:
        Éste método guardará a la base de datos los objetos apoyándose del modelo y de la lista columns.
        Se leerán los atributos definidos por el modelo, y con ayuda de la lista columns se tomara el valor correcto.
        El tipo correcto se leerá desde el modelo.
    '''

    def save_concept_input(self, record, model, project_id):
        # First, we get each all the attributes.
        line_item_key = record[self.ConceptConstants.LINE_ITEM_KEY_COL]
        # line_item_description = record[self.ConceptConstants.LINE_ITEM_DESCRIPTION_COL].encode('utf-8')  # Not used
        concept_key = str(record[self.ConceptConstants.CONCEPT_KEY_COL]).encode('utf-8')
        concept_description = str(record[self.ConceptConstants.CONCEPT_DESCRIPTION_COL]).encode('utf-8')
        unit = str(record[self.ConceptConstants.UNIT_COL]).encode('utf-8')
        quantity = Decimal(record[self.ConceptConstants.QUANTITY_COL])
        #.replace(',', '')
        # unit_price = Decimal(record[self.ConceptConstants.UNIT_PRICE_COL][1:].replace(',', ''))
        unit_price = Decimal(record[self.ConceptConstants.UNIT_PRICE_COL])
        #.replace(',', '')

        # Check if the unit exists. If not, add it.
        unit_qs = Unit.objects.filter(abbreviation=str(unit.upper()))
        if len(unit_qs) == 0:
            # The unit does not exist. Add it.
            unit_obj = Unit(abbreviation=str(unit.upper()),
                            quantification='C',
                            name=str(unit.upper()))
            unit_obj.save()
        else:
            # The unit exists. Use it.
            unit_obj = unit_qs[0]

        # Now we're going to check if the line item provided for the concept exists.
        line_item_qs = LineItem.objects.filter(Q(key=str(line_item_key).upper().replace('.0', '')) & Q(project_id=project_id))
        if len(line_item_qs) == 0:
            # The line item does not exist. Raise an exception to be displayed to the user.
            model_names = {
                self.CONCEPT_UPLOAD: 'concepto',
                self.INPUT_UPLOAD: 'insumo'
            }
            raise ErrorDataUpload(
                u"Se intentó agregar un " + model_names[
                    model] + "(" + concept_key + ") correspondiente a una partida que no existe (" + str(line_item_key) + ").",
                LoggingConstants.ERROR, self.user_id)
        else:
            # The line item exists. Use it.
            line_item_obj = line_item_qs[0]

        # Now We'll check that (line_item_id, concept_key) does not already exist.
        # If it already exists, we have to check the following:
        #  - If it has been estimated, unit, price and quantity have to be the same.
        #  - If it has NOT been estimated, we have to update the values.
        concepts_validation_qs = Concept_Input.objects.filter(Q(line_item_id=line_item_obj.id) & Q(key=concept_key))

        if len(concepts_validation_qs) != 0:
            old_concept = concepts_validation_qs[0]
            concept_has_been_estimated = self.concept_has_been_estimated(old_concept.id)

            if concept_has_been_estimated:

                errors = []  # This is only to create the error message, in case it exists

                # Check unit is the same:
                old_unit = old_concept.unit.abbreviation
                new_unit = str(unit.upper())

                if old_unit != new_unit:
                    errors.append('unidad')

                # Check price is the same:
                old_price = old_concept.unit_price
                new_price = unit_price

                if old_price != new_price:
                    errors.append('precio')

                # Check quantity is the same
                old_quantity = old_concept.quantity
                new_quantity = quantity

                if old_quantity != new_quantity:
                    errors.append('cantidad')

                if len(errors) > 0:
                    # There are errors. Create message and throw an exception.
                    message_properties = ''
                    for i in range(0, len(errors)):
                        message_properties += errors[i]
                        if i <= len(errors) - 3:
                            message_properties += ', '
                        if i == len(errors) - 2:
                            message_properties += ' y '

                    if len(errors) == 1:
                        error_message = u'Error al guardar el concepto ' + concept_key + u' para la partida ' \
                                        + line_item_obj.key + u'. Este concepto ya ha sido estimado y se ha intentado cambiar la propiedad ' + message_properties + u'.'
                    else:
                        error_message = u'Error al guardar el concepto ' + concept_key + u' para la partida ' \
                                        + line_item_obj.key + u'. Este concepto ya ha sido estimado y se han intentado cambiar las propiedades ' + message_properties + u'.'
                    # Data already exists. Raise an error to be displayed to the user.
                    raise ErrorDataUpload(error_message, LoggingConstants.ERROR, self.user_id)
            else:
                # Concept has not been estimated. Update its data and move on.
                new_unit = unit_obj
                new_price = unit_price
                new_quantity = quantity

                # Update values
                old_concept.unit = new_unit
                old_concept.unit_price = new_price
                old_concept.quantity = new_quantity

                # Save the concept
                old_concept.save()





        else:
            # The concept or input did not exist, we just have to create it and save it to the database.
            concept_input = Concept_Input(
                line_item=line_item_obj,
                unit=unit_obj,
                key=concept_key,
                description=concept_description,
                quantity=quantity,
                unit_price=unit_price,
                type=self.CONCEPT_INPUT_TYPES[model]
            )
            concept_input.save()


class ErrorDataUpload(SystemException):
    def __init__(self, message, priority, user_id):
        SystemException.__init__(self, message, LoggingConstants.OPERATION_LOGIC, priority, user_id)
