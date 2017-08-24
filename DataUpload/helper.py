# coding=utf-8
import datetime
import uuid
import xlrd

from abc import ABCMeta, abstractmethod

from decimal import Decimal

from DataUpload.models import UsuarioFolio
from ERP.models import Concept_Input, Unit, LineItem

'''
    Clase Objeto BD
     Esta clase se encarga de leer un archivo basándose en una serie de columnas
     que recibe en su constructor.

     Al instanciar el objeto, este también recibe el nombre de una clase.
     Con esta información se crearán dinámicamente objetos de dicha clase y se salvarán a la base de datos.

'''


class FileInterface:
    book = None

    def __init__(self, file_path):
        self.book = xlrd.open_workbook(file_path)

    def getElementList(self):
        elementList = []
        sheet = self.book.sheet_by_index(0)  # Get the first sheet

        i = 1
        while True:
            try:
                elements = sheet.row_values(i);
                elementList.append(elements)
                i += 1
            except IndexError:
                break

        return elementList


class DBObject:
    '''
    columns define las columnas del archivo CSV. Es importante definirlas bien y que tengan los mismos nombres que
    las propiedades definidas por el modelo, para automaticamente asignarlas y guardar a la base de datos.
    '''
    columns = []

    parent_nodes = []
    current_indent = 0

    LINE_ITEM_KEY_COL = 0
    LINE_ITEM_DESCRIPTION_COL = 1
    CONCEPT_KEY_COL = 2
    CONCEPT_DESCRIPTION_COL = 3
    UNIT_COL = 4
    QUANTITY_COL = 5
    UNIT_PRICE_COL = 6

    INPUT_TYPE = 'I'
    CONCEPT_TYPE = 'C'

    '''
        Indent length in spaces
    '''
    INDENT_LENGTH = 3

    '''
    object_class: define la clase del modelo con la que estamos trabajando.
    '''
    object_class = None

    '''
    Constructor.
    nombre_clase (pendiente): nombre de la clase que define al modelo.
    args* lista de columnas del archivo CSV. Estas tienen que tener el mismo nombre que las propiedades definidas por el
     modelo (nombre_clase)
    '''

    def __init__(self, username):
        self.columns = ['id', 'partida', 'clave_concepto', 'concepto', 'fecha_inicio', 'dias_calendario',
                        'fecha_termino', 'porcentaje', 'costo']
        self.username = username
        print 'cols' + str(self.columns)

    '''
    Método save:
    Éste método guardará a la base de datos los objetos apoyándose del modelo y de la lista columns.
    Se leerán los atributos definidos por el modelo, y con ayuda de la lista columns se tomara el valor correcto.
    El tipo correcto se leerá desde el modelo.
    '''

    def save(self, folio, record):
        # First, we get each all the attributes.
        line_item_key = record[self.LINE_ITEM_KEY_COL]
        line_item_description = record[self.LINE_ITEM_DESCRIPTION_COL].encode('utf-8')
        concept_key = record[self.CONCEPT_KEY_COL].encode('utf-8')
        concept_description = record[self.CONCEPT_DESCRIPTION_COL].encode('utf-8')
        unit = record[self.UNIT_COL].encode('utf-8')
        quantity = Decimal(record[self.QUANTITY_COL].replace(',',''))
        unit_price = Decimal(record[self.UNIT_PRICE_COL][1:].replace(',',''))


        
        unit_qs = Unit.objects.filter(abbreviation=unit.upper())

        if len(unit_qs) == 0:
            unit_obj = Unit(abbreviation=unit.upper(),
                            quantification='C',
                            name=unit.upper())
            unit_obj.save()
        else:
            unit_obj = unit_qs[0]

        line_item_qs = LineItem.objects.filter(key=line_item_key.upper())

        if len(line_item_qs) == 0:
            line_item_obj = LineItem(key=line_item_key.upper(),
                                     project_id=2,
                                     parent_line_item=None,
                                     description=line_item_description)
            line_item_obj.save()
        else:
            line_item_obj = line_item_qs[0]

        input = Concept_Input(
            line_item=line_item_obj,
            unit=unit_obj,
            key=concept_key,
            description=concept_description,
            quantity=quantity,
            unit_price=unit_price,
            type=self.INPUT_TYPE
        )

        print input
        input.save()

    '''
   Método file_format_is_valid:
   file: the filed translated to a two-dimensional array of values.

   This method receives a matrix of values and determines if everything is correct and it can be uploaded.
   '''

    def file_format_is_valid(self, file):
        # Check if line items exist
        # Check if units exist
        return True

    '''
    Método save_all:
    nombre_archivo: nombre del archivo csv.

    Este método abre el archivo csv, y guarda línea por línea a la base de datos dependiendo del modelo
    '''

    def save_all(self, nombre_archivo):
        folio = str(uuid.uuid4())
        try:
            file = FileInterface(nombre_archivo)
        except:
            raise Exception('Ha habido un problema leyendo el archivo')
        recordList = file.getElementList()

        if not self.file_format_is_valid(recordList):
            raise ErrorDataUpload("El formato de archivo no es válido")

        try:
            for record in recordList:
                # print 'Single record:' + str(record)
                if(record[0] != ""):
                    self.save(folio, record)

        except Exception, e:
            # self.object_class.objects.filter(folio=folio).delete()
            raise e
        return folio

    '''
    Método process_line
    Este método se encarga de procesar una línea del archivo CSV, y guardar los elementos en un arreglo.
    '''

    def process_line(self, line):
        return line.replace('\r\n', '').replace('\n', '').split(",")


class ErrorDataUpload(Exception):
    pass
