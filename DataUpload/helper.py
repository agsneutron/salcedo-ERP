# coding=utf-8
import datetime
import uuid
import xlrd

from abc import ABCMeta, abstractmethod

from DataUpload.models import UsuarioFolio

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

    ID_COL = 0
    LINE_ITEM_COL = 1
    CONCEPT_KEY_COL = 2
    CONCEPT_COL = 3
    START_DATE_COL = 4
    CALENDAR_DAYS_COL = 5
    END_DATE_COL = 6
    PERCENTAGE_COL = 7
    COST_COL = 8

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
        # print "Saving: " + str(record)
        # First, we have to identify whether we are dealing with a line item, compound concept or a single one.
        is_line_item = record[self.LINE_ITEM_COL] == '-'

        if is_line_item:
            print 'Partida'

        else:
            print 'Concepto'

        # Get end set indent level
        concept = record[self.CONCEPT_COL]
        indent = 0
        for i in range(0, len(concept)):
            if concept[i] != ' ':
                break
            indent += 1
        indent /= self.INDENT_LENGTH

        self.current_indent = indent

        print 'Indent Level: ' + str(indent)



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

        print recordList

        try:
            for record in recordList:
                # print 'Single record:' + str(record)
                self.save(folio, record)
                '''
                uf = UsuarioFolio()
                uf.usuario = self.nombre_usuario
                uf.folio = folio
                uf.save()'''
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