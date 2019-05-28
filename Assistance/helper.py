# coding=utf-8
import datetime
from _mysql import IntegrityError
from datetime import date, datetime, timedelta

import xlrd
from django.db.models.query_utils import Q

from HumanResources.models import Employee, PayrollPeriod, EmployeePositionDescription, EmployeeAssistance, PayrollGroup
from SalcedoERP.lib.SystemLog import SystemException, LoggingConstants


class AssistanceFileInterface(object):
    """ Reads .xls files and converts them to lists.

    Attributes:
        file_path: the path of the file that must be read.

    """

    # The book from which the data will be read
    book = None
    current_user = None

    def __init__(self, file_path, user):
        """ Inits the FileInterface object with a file.
        :param file_path: the path of the file with which the object will be initialized.
        """
        self.book = xlrd.open_workbook(file_contents=file_path.read())
        self.current_user = user
        #self.book = xlrd.open_workbook(file_path)

    def get_element_list(self, file_type, payroll_period):
        """ Obtains an list containing all the records of the first sheet of the object's file.
        :return: A list containing all the records of the first sheet of the object's file.
        """

        # Create empty array so that we fill it later.
        element_list = []
        start_period_date = None
        end_period_date = None
        process_date = None
        #start_payroll_period = datetime.datetime.now()


        if file_type == PayrollGroup.CHECKER_TYPE_AUTOMATIC:
            # Get the first sheet
            sheet = self.book.sheet_by_index(2)
            # Get period to  process and file generated date
            i = 2
        elif file_type == PayrollGroup.CHECKER_TYPE_MANUAL:
            # Get the first sheet
            sheet = self.book.sheet_by_index(0)
            i = 1


        # If the type of assistance check is automatic, check that there are at least 15 columns..
        if file_type == PayrollGroup.CHECKER_TYPE_AUTOMATIC and len(sheet.row_values(0)) < 15:
            error_message = "El formato del archivo cargado es incorrecto para el tipo de carga automática."
            raise ErrorDataUpload(error_message, LoggingConstants.ERROR, self.current_user.id)
        elif file_type == PayrollGroup.CHECKER_TYPE_MANUAL and len(sheet.row_values(0)) != 4:
            error_message = "El formato del archivo cargado es incorrecto para el tipo de carga manual."
            raise ErrorDataUpload(error_message, LoggingConstants.ERROR, self.current_user.id)

        # i = 1  We start on row 1, because the established format does not include a header.
        # i = 3  We start on row 3, because the established format  include a header.

        while True:
            try:
                # Read the whole row at once
                elements = sheet.row_values(i)
                #col_elements = sheet.col_values(i)
                try:
                    if file_type == PayrollGroup.CHECKER_TYPE_AUTOMATIC:
                        # automatic
                        if i == 2:
                            formato_fecha = "%Y-%m-%d"
                            start_payroll_period = payroll_period.start_period
                            #start_payroll_period = datetime.strptime(start_payroll_period, formato_fecha)
                            end_payroll_period = payroll_period.end_period
                            #end_payroll_period = datetime.strptime(end_payroll_period, formato_fecha)

                            elements = sheet.row_values(2)
                            start_period_date = elements[6]
                            start_period_date = datetime.strptime(start_period_date[:10], formato_fecha)
                            end_period_date = elements[6]
                            end_period_date = datetime.strptime(end_period_date[13:], formato_fecha)
                            process_date = datetime.strptime(elements[18], formato_fecha)
                            elements[0] = start_period_date.date()
                            elements[1] = end_period_date.date()
                            elements[2] = start_payroll_period
                            elements[3] = end_payroll_period
                            elements[4] = start_payroll_period.day

                            if start_payroll_period.day == 1 and start_period_date.date() != start_payroll_period:
                                raise TypeError('El periodo del archivo no corresponde al periodo a procesar')
                            elif start_payroll_period.day == 16 and end_period_date.date() != end_payroll_period:
                                raise TypeError('El periodo del archivo no corresponde al periodo a procesar')
                            i += 1
                        else:
                            employee_id = elements[4]
                            elements = sheet.row_values(i+1)
                            elements.append(employee_id)
                            i += 1

                    else:
                        # Manual
                        try:
                            date_as_datetime = datetime.datetime(*xlrd.xldate_as_tuple(elements[1], self.book.datemode))
                            elements[1] = date_as_datetime

                            # Enter time
                            # time_value = xlrd.xldate_as_tuple(elements[2], self.book.datemode)
                            # time_record_obj = time(*time_value[3:])
                            time_record_obj = datetime.time(*xlrd.xldate_as_tuple(elements[2], self.book.datemode)[3:])
                            elements[2] = time_record_obj

                            # Exit time
                            time_record_obj = datetime.time(*xlrd.xldate_as_tuple(elements[3], self.book.datemode)[3:])
                            elements[3] = time_record_obj
                        except ValueError as e:
                            if file_type == PayrollGroup.CHECKER_TYPE_AUTOMATIC:
                                error_message = "El formato del archivo cargado es incorrecto para el tipo de carga automática. Los valores para fechas y horas no son válidos."
                            else:
                                error_message = "El formato del archivo cargado es incorrecto para el tipo de carga manual. Los valores para fechas y horas no son válidos."
                            raise ErrorDataUpload(error_message, LoggingConstants.ERROR, self.current_user.id)
                        #strptime(time_record, "%H:%M").time()

                except TypeError as e:
                    if file_type == PayrollGroup.CHECKER_TYPE_AUTOMATIC:
                        error_message = "El formato del archivo cargado es incorrecto para el tipo de carga" \
                                        " automática. "+ e.message
                    else:
                        error_message = "El formato del archivo cargado es incorrecto para el tipo de carga manual."
                    raise ErrorDataUpload(error_message, LoggingConstants.ERROR, self.current_user.id)
                # Add the row to the list
                element_list.append(elements)
                i += 1
            except IndexError:
                # We're done reading.
                break

        # Return all the rows read.
        return element_list


# Class to manage the creation and save of an Assistance object.
class AssistanceDBObject:

    def __init__(self, current_user, records, payroll_period_id):
        self.current_user = current_user
        self.records = records

        try:
            self.payroll_period = PayrollPeriod.objects.get(pk=payroll_period_id)
        except PayrollPeriod.DoesNotExist:
            error_message = "El periodo con el identificador " + str(payroll_period_id) + " no existe"
            raise ErrorDataUpload(error_message, LoggingConstants.ERROR, self.current_user.id)

    # Function to process the given records one at a time.
    def process_records(self):
        # self.records.pop(0)
        # if checker type is automatic, need to process by row
        if self.payroll_period.payroll_group.checker_type == PayrollGroup.CHECKER_TYPE_AUTOMATIC:
            i = 0

            start_date = datetime.now().date()
            start_day = None

            for record in self.records:
                print record
                if i == 0:
                    start_date = record.pop(0)
                    start_day = record.pop(3)
                else:
                    id_empleado = record.pop()
                    j = 0
                    for element in record:
                        print element
                        automatic_record = []
                        automatic_record.append(id_empleado)
                        automatic_record.append(start_date + timedelta(days=j))
                        automatic_record.append(element[:5])
                        automatic_record.append(element[5:])
                        self.save_assistance_record(automatic_record)
                i += 1
        else:
            for record in self.records:
                self.save_assistance_record(record)

    # Constants that define the value position in the given array.
    class ElementPosition:
        ATM_EMPLOYEE_KEY_COL = 0
        ATM_DATE_COL = 1
        ATM_ENTRY_COL = 2
        ATM_EXIT_COL = 3

        MANUAL_EMPLOYEE_KEY_COL = 0
        MANUAL_DATE_COL = 1
        MANUAL_ENTRY_COL = 2
        MANUAL_EXIT_COL = 3

    class AbsenceConditions:
        MINUTES_TO_BE_ABSENT = 15

    # Method to save create and save each given element.
    def save_assistance_record(self, record):

        if self.payroll_period.payroll_group.checker_type == PayrollGroup.CHECKER_TYPE_AUTOMATIC:
            employee_key = record[self.ElementPosition.ATM_EMPLOYEE_KEY_COL]
            record_date = record[self.ElementPosition.ATM_DATE_COL]
            entry_time_record = record[self.ElementPosition.ATM_ENTRY_COL]
            exit_time_record = record[self.ElementPosition.ATM_EXIT_COL]
            print "Automatic Assistance Upload"

        else:
            employee_key = record[self.ElementPosition.MANUAL_EMPLOYEE_KEY_COL]
            record_date = record[self.ElementPosition.MANUAL_DATE_COL]
            entry_time_record = record[self.ElementPosition.MANUAL_ENTRY_COL]
            exit_time_record = record[self.ElementPosition.MANUAL_EXIT_COL]
            print "Manual Assistance Upload"

        #entry_time_record = datetime.datetime.strptime(entry_time_record.encode('ascii','ignore'), '%H:%M:%S').time()
        #exit_time_record = datetime.datetime.strptime(exit_time_record.encode('ascii','ignore'), '%H:%M:%S').time()

        # Obtaining the related employee by theit key number. If the given employeee does not exist,
        # the system will throw an exception.
        employee_to_save = self.validate_employee_key(employee_key)

        # Validates that the given date is found between the limits of the selected payroll period.
        date_to_save = self.validate_date(record_date, employee_to_save.employee_key)

        # Validates the given fromat for the entry and exit time.
        entry_time_to_save = self.validate_entry_and_exit_time(entry_time_record, employee_to_save.employee_key)
        exit_time_to_save = self.validate_entry_and_exit_time(exit_time_record, employee_to_save.employee_key)

        employee_was_absent = self.check_if_absent(employee_to_save, entry_time_to_save, exit_time_to_save)

        # To check if the assistance exists before saving it.
        assistance_existed = EmployeeAssistance.objects.filter(
            Q(record_date = date_to_save) &
            Q(employee = employee_to_save) &
            Q(payroll_period=self.payroll_period))


        if len(assistance_existed) > 0:
            # If the assistance already existed, lets update the information.
            assistance_obj = assistance_existed[0]
            assistance_obj.entry_time = entry_time_to_save
            assistance_obj.exit_time = exit_time_to_save
            assistance_obj.absence = employee_was_absent

            # Maybe add a message that says that some records where updated.

            assistance_obj.save()

        else:
            assistance_obj = EmployeeAssistance(
                entry_time=entry_time_to_save,
                exit_time=exit_time_to_save,
                record_date = date_to_save,
                employee = employee_to_save,
                payroll_period=self.payroll_period,
                absence=employee_was_absent
            )



            assistance_obj.save()






    def validate_employee_key(self, employee_key):
        """
        Checks if the employee exists based on their employee key.
        :param employee_key: the key to check for.
        :return: employee object.
        """
        try:
            employee = Employee.objects.get(employee_key=employee_key)
            return employee

        except Employee.DoesNotExist:
            error_message = "El empleado con la clave " + str(employee_key) + " no existe."
            raise ErrorDataUpload(error_message, LoggingConstants.ERROR, self.current_user.id)


    def validate_date(self, record_date, employee_key):
        """
        Checks the format of the given date and if it is found between the limit dates of the selected Payroll Period Group.
        :param record_date: the date to be validated.
        :param employee_key: the employee key to raise the detail level in case of error.
        :return: date object.
        """

        # Obtaining the date object from the obtained record date.
        error_message = "Ha habido un error con el formato de la fecha " + str(record_date) + " para el registro del" + \
                        " empleado con la clave " + str(employee_key)
        date_to_save = record_date

        '''if type(record_date) is float:
            try:
                date_to_save = datetime.datetime.fromtimestamp(record_date)
            except ValueError:
                raise ErrorDataUpload(error_message, LoggingConstants.ERROR, self.current_user.id)
        else:
            try:
                date_to_save = datetime.datetime.strptime(record_date, "%d/%m/%Y").date()
            except ValueError:
                raise ErrorDataUpload(error_message, LoggingConstants.ERROR, self.current_user.id)'''

        # Obtaining the date object from the Payroll Period object.
        start_period = datetime.datetime.combine(self.payroll_period.start_period, datetime.datetime.min.time())
        end_period = datetime.datetime.combine(self.payroll_period.end_period, datetime.datetime.min.time())

        # Checking if the file contains information for the correct Payroll Period date.
        if date_to_save < start_period or date_to_save > end_period:
            error_message = "Se ha tratado de cargar información para el empleado con la clave " + str(employee_key) +\
                            " en la fecha " + str(date_to_save) + " que no corresponde al periodo seleccionado."
            raise ErrorDataUpload(error_message, LoggingConstants.ERROR, self.current_user.id)

        return date_to_save


    def validate_entry_and_exit_time(self, time_record, employee_key):
        if time_record is '' or time_record is None:
            return None

        time_record_obj = time_record

        '''
        try:
            time_record_obj = datetime.datetime.strptime(time_record, "%H:%M").time()

        except ValueError:
            error_message = "Ha habido un error con el formato de la hora " + str(time_record) + " para el registro del" + \
                            " empleado con la clave " + str(employee_key)
            raise ErrorDataUpload(error_message, LoggingConstants.ERROR, self.current_user.id)
        '''
        return time_record_obj


    def check_if_absent(self, employee, entry_time_record, exit_time_record):


        if entry_time_record is None or exit_time_record is None:
            return True

        employee_position = EmployeePositionDescription.objects.get(employee_id=employee.id)

        position_entry_time = employee_position.entry_time
        position_exit_time = employee_position.departure_time

        entry_diff = datetime.datetime.combine(date.today(), entry_time_record) - datetime.datetime.combine(date.today(), position_entry_time)
        exit_diff = datetime.datetime.combine(date.today(), position_exit_time) - datetime.datetime.combine(date.today(), exit_time_record)

        arrived_minutes_late = entry_diff.total_seconds() / 60
        left_minutes_early = exit_diff.total_seconds() / 60

        '''
        print "Employee " + str(employee.employee_key) + " was absent?"
        print "------- Entry -------"
        print "Should entry: " + str(position_entry_time)
        print "Actual entry time: " + str(entry_time_record)
        print "Entry difference: " + str(arrived_minutes_late)

        print "------- Exit  -------"
        print "Should exit: " + str(position_exit_time)
        print "Actual exit time: " + str(exit_time_record)
        print "Entry difference: " + str(left_minutes_early)
        '''

        absent = False
        if arrived_minutes_late > self.AbsenceConditions.MINUTES_TO_BE_ABSENT or \
                        left_minutes_early > self.AbsenceConditions.MINUTES_TO_BE_ABSENT:
            absent = True

        return absent



class ErrorDataUpload(SystemException):
    def __init__(self, message, priority, user_id):
        SystemException.__init__(self, message, LoggingConstants.OPERATION_LOGIC, priority, user_id)

