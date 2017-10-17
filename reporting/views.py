# coding=utf-8
from django.db.models.query_utils import Q
from django.http.response import HttpResponse

from ERP import api
from ERP.models import AccessToProject, Project, LineItem
from reporting import api
from ERP.lib.utilities import Utilities
from lib.financial_advance_report import FinancialAdvanceReport
from lib.estimate_reports import EstimateReports
from lib.estimate_report_for_contractors import EstimateReportsForContractors
from django.shortcuts import render, redirect, render_to_response
from django.views.generic import View

from reporting import lib
from reporting.lib.physical_financial_advance_report import PhysicalFinancialAdvanceReport
from reporting.lib.estimate_report_by_single_contractor import EstimateReportsBySingleContractor
from reporting.lib.budget_report_by_contractor import BudgetReportsByContractor


def report(request):
    return render(request, 'reporting/report.html')


# class GetFinancialReport()


def testView(request):
    json = {
        "global_total_programmed": "5555198.2944",
        "line_items": [
            {
                "sub_line_items": [],
                "name": "PRELIMINARES",
                "parent_key": "",
                "total_programmed": "123946.3889",
                "general_estimated_sum": "0",
                "total_pending": "123046.3889",
                "general_pending_sum": "0",
                "greatest_parent": "",
                "key": "1.1",
                "concepts": [
                    {
                        "concept_key": "005-48",
                        "total_pending": "61980.8014",
                        "total_estimated": "900.0",
                        "total_programmed": "62880.8014"
                    },
                    {
                        "concept_key": "3.1.B1",
                        "total_pending": "3017.5000",
                        "total_estimated": "0.00",
                        "total_programmed": "3017.5000"
                    },
                    {
                        "concept_key": "GCAISC-0042",
                        "total_pending": "58048.0875",
                        "total_estimated": "0.00",
                        "total_programmed": "58048.0875"
                    }
                ],
                "general_programmed_sum": "0",
                "total_estimated": "900.0"
            },
            {
                "sub_line_items": [],
                "name": "LIMPIEZA",
                "parent_key": "",
                "total_programmed": "28141.1182",
                "general_estimated_sum": "0",
                "total_pending": "28141.1182",
                "general_pending_sum": "0",
                "greatest_parent": "",
                "key": "1.10",
                "concepts": [
                    {
                        "concept_key": "005-48",
                        "total_pending": "14627.1874",
                        "total_estimated": "0.00",
                        "total_programmed": "14627.1874"
                    },
                    {
                        "concept_key": "LIMP-001",
                        "total_pending": "13513.9308",
                        "total_estimated": "0.00",
                        "total_programmed": "13513.9308"
                    }
                ],
                "general_programmed_sum": "0",
                "total_estimated": "0.00"
            },
            {
                "sub_line_items": [],
                "name": "CIMENTACION",
                "parent_key": "",
                "total_programmed": "859748.8780",
                "general_estimated_sum": "0",
                "total_pending": "859748.8780",
                "general_pending_sum": "0",
                "greatest_parent": "",
                "key": "1.2",
                "concepts": [
                    {
                        "concept_key": "03002003",
                        "total_pending": "140935.3725",
                        "total_estimated": "0.00",
                        "total_programmed": "140935.3725"
                    },
                    {
                        "concept_key": "093-04",
                        "total_pending": "36592.2900",
                        "total_estimated": "0.00",
                        "total_programmed": "36592.2900"
                    },
                    {
                        "concept_key": "093-05B",
                        "total_pending": "131729.8500",
                        "total_estimated": "0.00",
                        "total_programmed": "131729.8500"
                    },
                    {
                        "concept_key": "0936-09B",
                        "total_pending": "19666.9200",
                        "total_estimated": "0.00",
                        "total_programmed": "19666.9200"
                    },
                    {
                        "concept_key": "094-101C",
                        "total_pending": "233758.5000",
                        "total_estimated": "0.00",
                        "total_programmed": "233758.5000"
                    },
                    {
                        "concept_key": "AB-VS-CIM01",
                        "total_pending": "22939.6500",
                        "total_estimated": "0.00",
                        "total_programmed": "22939.6500"
                    },
                    {
                        "concept_key": "AB-VS-CIM02",
                        "total_pending": "34457.2655",
                        "total_estimated": "0.00",
                        "total_programmed": "34457.2655"
                    },
                    {
                        "concept_key": "AB-VS-CIM03",
                        "total_pending": "13828.9600",
                        "total_estimated": "0.00",
                        "total_programmed": "13828.9600"
                    },
                    {
                        "concept_key": "AB-VS-CIM04",
                        "total_pending": "58081.9200",
                        "total_estimated": "0.00",
                        "total_programmed": "58081.9200"
                    },
                    {
                        "concept_key": "ARLISC-003",
                        "total_pending": "22362.8160",
                        "total_estimated": "0.00",
                        "total_programmed": "22362.8160"
                    },
                    {
                        "concept_key": "BP-006-1",
                        "total_pending": "48454.4340",
                        "total_estimated": "0.00",
                        "total_programmed": "48454.4340"
                    },
                    {
                        "concept_key": "CIM-006",
                        "total_pending": "13122.4000",
                        "total_estimated": "0.00",
                        "total_programmed": "13122.4000"
                    },
                    {
                        "concept_key": "KC-CON01",
                        "total_pending": "83818.5000",
                        "total_estimated": "0.00",
                        "total_programmed": "83818.5000"
                    }
                ],
                "general_programmed_sum": "0",
                "total_estimated": "0.00"
            },
            {
                "sub_line_items": [],
                "name": "ESTRUCTURA",
                "parent_key": "",
                "total_programmed": "2712831.6388",
                "general_estimated_sum": "0",
                "total_pending": "2712831.6388",
                "general_pending_sum": "0",
                "greatest_parent": "",
                "key": "1.3",
                "concepts": [
                    {
                        "concept_key": "013-14G1",
                        "total_pending": "6019.6800",
                        "total_estimated": "0.00",
                        "total_programmed": "6019.6800"
                    },
                    {
                        "concept_key": "03002003",
                        "total_pending": "42105.8560",
                        "total_estimated": "0.00",
                        "total_programmed": "42105.8560"
                    },
                    {
                        "concept_key": "076-07D",
                        "total_pending": "5358.0000",
                        "total_estimated": "0.00",
                        "total_programmed": "5358.0000"
                    },
                    {
                        "concept_key": "AB-VS-EST01",
                        "total_pending": "720000.0000",
                        "total_estimated": "0.00",
                        "total_programmed": "720000.0000"
                    },
                    {
                        "concept_key": "AB-VS-EST02",
                        "total_pending": "897384.7972",
                        "total_estimated": "0.00",
                        "total_programmed": "897384.7972"
                    },
                    {
                        "concept_key": "AB-VS-EST03",
                        "total_pending": "233264.3072",
                        "total_estimated": "0.00",
                        "total_programmed": "233264.3072"
                    },
                    {
                        "concept_key": "AB-VS-EST04",
                        "total_pending": "328095.9022",
                        "total_estimated": "0.00",
                        "total_programmed": "328095.9022"
                    },
                    {
                        "concept_key": "AB-VS-EST05",
                        "total_pending": "60026.1480",
                        "total_estimated": "0.00",
                        "total_programmed": "60026.1480"
                    },
                    {
                        "concept_key": "ARCISC-0090",
                        "total_pending": "68104.3647",
                        "total_estimated": "0.00",
                        "total_programmed": "68104.3647"
                    },
                    {
                        "concept_key": "GCAISC-0045",
                        "total_pending": "102492.2756",
                        "total_estimated": "0.00",
                        "total_programmed": "102492.2756"
                    },
                    {
                        "concept_key": "ISC-0058",
                        "total_pending": "10681.2174",
                        "total_estimated": "0.00",
                        "total_programmed": "10681.2174"
                    },
                    {
                        "concept_key": "LAC-C20",
                        "total_pending": "160587.4942",
                        "total_estimated": "0.00",
                        "total_programmed": "160587.4942"
                    },
                    {
                        "concept_key": "SUSSISC-0015",
                        "total_pending": "1462.0800",
                        "total_estimated": "0.00",
                        "total_programmed": "1462.0800"
                    },
                    {
                        "concept_key": "SUSSISC-009C",
                        "total_pending": "77249.5163",
                        "total_estimated": "0.00",
                        "total_programmed": "77249.5163"
                    }
                ],
                "general_programmed_sum": "0",
                "total_estimated": "0.00"
            },
            {
                "sub_line_items": [],
                "name": "ACABADOS",
                "parent_key": "",
                "total_programmed": "466288.6535",
                "general_estimated_sum": "0",
                "total_pending": "466288.6535",
                "general_pending_sum": "0",
                "greatest_parent": "",
                "key": "1.4",
                "concepts": [
                    {
                        "concept_key": "068-01",
                        "total_pending": "11633.3553",
                        "total_estimated": "0.00",
                        "total_programmed": "11633.3553"
                    },
                    {
                        "concept_key": "068-06",
                        "total_pending": "35215.6599",
                        "total_estimated": "0.00",
                        "total_programmed": "35215.6599"
                    },
                    {
                        "concept_key": "068-06B",
                        "total_pending": "54690.4872",
                        "total_estimated": "0.00",
                        "total_programmed": "54690.4872"
                    },
                    {
                        "concept_key": "068-07",
                        "total_pending": "3437.8476",
                        "total_estimated": "0.00",
                        "total_programmed": "3437.8476"
                    },
                    {
                        "concept_key": "068-11",
                        "total_pending": "62979.3408",
                        "total_estimated": "0.00",
                        "total_programmed": "62979.3408"
                    },
                    {
                        "concept_key": "068-51",
                        "total_pending": "15852.6480",
                        "total_estimated": "0.00",
                        "total_programmed": "15852.6480"
                    },
                    {
                        "concept_key": "084-02B",
                        "total_pending": "69521.1008",
                        "total_estimated": "0.00",
                        "total_programmed": "69521.1008"
                    },
                    {
                        "concept_key": "AB-VS-ACA01",
                        "total_pending": "13988.0000",
                        "total_estimated": "0.00",
                        "total_programmed": "13988.0000"
                    },
                    {
                        "concept_key": "DSCO-013",
                        "total_pending": "15758.0744",
                        "total_estimated": "0.00",
                        "total_programmed": "15758.0744"
                    },
                    {
                        "concept_key": "KA-CON08",
                        "total_pending": "21054.1820",
                        "total_estimated": "0.00",
                        "total_programmed": "21054.1820"
                    },
                    {
                        "concept_key": "LAMB-001",
                        "total_pending": "16448.7888",
                        "total_estimated": "0.00",
                        "total_programmed": "16448.7888"
                    },
                    {
                        "concept_key": "MDT-001",
                        "total_pending": "138760.0695",
                        "total_estimated": "0.00",
                        "total_programmed": "138760.0695"
                    },
                    {
                        "concept_key": "ULSISC-0050B",
                        "total_pending": "6949.0992",
                        "total_estimated": "0.00",
                        "total_programmed": "6949.0992"
                    }
                ],
                "general_programmed_sum": "0",
                "total_estimated": "0.00"
            },
            {
                "sub_line_items": [],
                "name": "CARPINTERÍA",
                "parent_key": "",
                "total_programmed": "571757.4810",
                "general_estimated_sum": "0",
                "total_pending": "571757.4810",
                "general_pending_sum": "0",
                "greatest_parent": "",
                "key": "1.5",
                "concepts": [
                    {
                        "concept_key": "AB-VS-CAR01",
                        "total_pending": "81359.0200",
                        "total_estimated": "0.00",
                        "total_programmed": "81359.0200"
                    },
                    {
                        "concept_key": "AB-VS-CAR02",
                        "total_pending": "97448.7900",
                        "total_estimated": "0.00",
                        "total_programmed": "97448.7900"
                    },
                    {
                        "concept_key": "AB-VS-CAR03",
                        "total_pending": "18032.4020",
                        "total_estimated": "0.00",
                        "total_programmed": "18032.4020"
                    },
                    {
                        "concept_key": "AB-VS-CAR04",
                        "total_pending": "68969.5890",
                        "total_estimated": "0.00",
                        "total_programmed": "68969.5890"
                    },
                    {
                        "concept_key": "AB-VS-CAR05",
                        "total_pending": "115000.0000",
                        "total_estimated": "0.00",
                        "total_programmed": "115000.0000"
                    },
                    {
                        "concept_key": "ACA-005B",
                        "total_pending": "18981.8300",
                        "total_estimated": "0.00",
                        "total_programmed": "18981.8300"
                    },
                    {
                        "concept_key": "CLOSET-01",
                        "total_pending": "171965.8500",
                        "total_estimated": "0.00",
                        "total_programmed": "171965.8500"
                    }
                ],
                "general_programmed_sum": "0",
                "total_estimated": "0.00"
            },
            {
                "sub_line_items": [],
                "name": "HERRERÍA",
                "parent_key": "",
                "total_programmed": "44856.9560",
                "general_estimated_sum": "0",
                "total_pending": "44856.9560",
                "general_pending_sum": "0",
                "greatest_parent": "",
                "key": "1.6",
                "concepts": [
                    {
                        "concept_key": "BAR-001",
                        "total_pending": "28834.0598",
                        "total_estimated": "0.00",
                        "total_programmed": "28834.0598"
                    },
                    {
                        "concept_key": "BAR-SP01",
                        "total_pending": "7289.9162",
                        "total_estimated": "0.00",
                        "total_programmed": "7289.9162"
                    },
                    {
                        "concept_key": "ISC-0078",
                        "total_pending": "8732.9800",
                        "total_estimated": "0.00",
                        "total_programmed": "8732.9800"
                    }
                ],
                "general_programmed_sum": "0",
                "total_estimated": "0.00"
            },
            {
                "sub_line_items": [],
                "name": "INSTALACIÓN ELÉCTRICA",
                "parent_key": "",
                "total_programmed": "317019.7900",
                "general_estimated_sum": "0",
                "total_pending": "317019.7900",
                "general_pending_sum": "0",
                "greatest_parent": "",
                "key": "1.7",
                "concepts": [
                    {
                        "concept_key": "048-01D",
                        "total_pending": "487.3200",
                        "total_estimated": "0.00",
                        "total_programmed": "487.3200"
                    },
                    {
                        "concept_key": "049-02",
                        "total_pending": "252.6800",
                        "total_estimated": "0.00",
                        "total_programmed": "252.6800"
                    },
                    {
                        "concept_key": "05000006",
                        "total_pending": "18200.0000",
                        "total_estimated": "0.00",
                        "total_programmed": "18200.0000"
                    },
                    {
                        "concept_key": "092-04.5",
                        "total_pending": "1520.8500",
                        "total_estimated": "0.00",
                        "total_programmed": "1520.8500"
                    },
                    {
                        "concept_key": "AB-VS-IE01",
                        "total_pending": "37748.7600",
                        "total_estimated": "0.00",
                        "total_programmed": "37748.7600"
                    },
                    {
                        "concept_key": "AB-VS-IE02",
                        "total_pending": "5271.9000",
                        "total_estimated": "0.00",
                        "total_programmed": "5271.9000"
                    },
                    {
                        "concept_key": "AB-VS-IE03",
                        "total_pending": "11663.1000",
                        "total_estimated": "0.00",
                        "total_programmed": "11663.1000"
                    },
                    {
                        "concept_key": "AB-VS-IE04",
                        "total_pending": "35407.5000",
                        "total_estimated": "0.00",
                        "total_programmed": "35407.5000"
                    },
                    {
                        "concept_key": "AB-VS-IE05",
                        "total_pending": "26939.7000",
                        "total_estimated": "0.00",
                        "total_programmed": "26939.7000"
                    },
                    {
                        "concept_key": "AB-VS-IE06",
                        "total_pending": "12933.2000",
                        "total_estimated": "0.00",
                        "total_programmed": "12933.2000"
                    },
                    {
                        "concept_key": "AB-VS-IE07",
                        "total_pending": "18804.7600",
                        "total_estimated": "0.00",
                        "total_programmed": "18804.7600"
                    },
                    {
                        "concept_key": "AB-VS-IE08",
                        "total_pending": "60405.3000",
                        "total_estimated": "0.00",
                        "total_programmed": "60405.3000"
                    },
                    {
                        "concept_key": "AB-VS-IE09",
                        "total_pending": "5756.4000",
                        "total_estimated": "0.00",
                        "total_programmed": "5756.4000"
                    },
                    {
                        "concept_key": "AB-VS-IE10",
                        "total_pending": "4688.8000",
                        "total_estimated": "0.00",
                        "total_programmed": "4688.8000"
                    },
                    {
                        "concept_key": "AB-VS-IE11",
                        "total_pending": "4618.4000",
                        "total_estimated": "0.00",
                        "total_programmed": "4618.4000"
                    },
                    {
                        "concept_key": "INS-002",
                        "total_pending": "14317.6000",
                        "total_estimated": "0.00",
                        "total_programmed": "14317.6000"
                    },
                    {
                        "concept_key": "INS-005",
                        "total_pending": "6579.5200",
                        "total_estimated": "0.00",
                        "total_programmed": "6579.5200"
                    },
                    {
                        "concept_key": "ISC-051",
                        "total_pending": "51424.0000",
                        "total_estimated": "0.00",
                        "total_programmed": "51424.0000"
                    }
                ],
                "general_programmed_sum": "0",
                "total_estimated": "0.00"
            },
            {
                "sub_line_items": [],
                "name": "INSTALACIÓN HIDROSANITARIA",
                "parent_key": "",
                "total_programmed": "354465.9700",
                "general_estimated_sum": "0",
                "total_pending": "354465.9700",
                "general_pending_sum": "0",
                "greatest_parent": "",
                "key": "1.8",
                "concepts": [
                    {
                        "concept_key": "040-93",
                        "total_pending": "19450.2400",
                        "total_estimated": "0.00",
                        "total_programmed": "19450.2400"
                    },
                    {
                        "concept_key": "094-48B",
                        "total_pending": "18535.8000",
                        "total_estimated": "0.00",
                        "total_programmed": "18535.8000"
                    },
                    {
                        "concept_key": "094-55",
                        "total_pending": "1328.3600",
                        "total_estimated": "0.00",
                        "total_programmed": "1328.3600"
                    },
                    {
                        "concept_key": "AB-VS-IHA14",
                        "total_pending": "9799.7900",
                        "total_estimated": "0.00",
                        "total_programmed": "9799.7900"
                    },
                    {
                        "concept_key": "AB-VS-IHS01",
                        "total_pending": "14748.7200",
                        "total_estimated": "0.00",
                        "total_programmed": "14748.7200"
                    },
                    {
                        "concept_key": "AB-VS-IHS02",
                        "total_pending": "12348.9100",
                        "total_estimated": "0.00",
                        "total_programmed": "12348.9100"
                    },
                    {
                        "concept_key": "AB-VS-IHS03",
                        "total_pending": "362.0800",
                        "total_estimated": "0.00",
                        "total_programmed": "362.0800"
                    },
                    {
                        "concept_key": "AB-VS-IHS04",
                        "total_pending": "27945.8500",
                        "total_estimated": "0.00",
                        "total_programmed": "27945.8500"
                    },
                    {
                        "concept_key": "AB-VS-IHS05",
                        "total_pending": "10587.2000",
                        "total_estimated": "0.00",
                        "total_programmed": "10587.2000"
                    },
                    {
                        "concept_key": "AB-VS-IHS06",
                        "total_pending": "7491.8400",
                        "total_estimated": "0.00",
                        "total_programmed": "7491.8400"
                    },
                    {
                        "concept_key": "AB-VS-IHS07",
                        "total_pending": "6840.7200",
                        "total_estimated": "0.00",
                        "total_programmed": "6840.7200"
                    },
                    {
                        "concept_key": "AB-VS-IHS08",
                        "total_pending": "14405.8600",
                        "total_estimated": "0.00",
                        "total_programmed": "14405.8600"
                    },
                    {
                        "concept_key": "AB-VS-IHS09",
                        "total_pending": "26141.3600",
                        "total_estimated": "0.00",
                        "total_programmed": "26141.3600"
                    },
                    {
                        "concept_key": "AB-VS-IHS10",
                        "total_pending": "17124.5400",
                        "total_estimated": "0.00",
                        "total_programmed": "17124.5400"
                    },
                    {
                        "concept_key": "AB-VS-IHS11",
                        "total_pending": "81086.0000",
                        "total_estimated": "0.00",
                        "total_programmed": "81086.0000"
                    },
                    {
                        "concept_key": "AB-VS-IHS12",
                        "total_pending": "6912.3700",
                        "total_estimated": "0.00",
                        "total_programmed": "6912.3700"
                    },
                    {
                        "concept_key": "AB-VS-IHS13",
                        "total_pending": "9255.2300",
                        "total_estimated": "0.00",
                        "total_programmed": "9255.2300"
                    },
                    {
                        "concept_key": "DSCO-026",
                        "total_pending": "169.8800",
                        "total_estimated": "0.00",
                        "total_programmed": "169.8800"
                    },
                    {
                        "concept_key": "GCAISC-0043",
                        "total_pending": "1549.4300",
                        "total_estimated": "0.00",
                        "total_programmed": "1549.4300"
                    },
                    {
                        "concept_key": "INS-003",
                        "total_pending": "28801.1500",
                        "total_estimated": "0.00",
                        "total_programmed": "28801.1500"
                    },
                    {
                        "concept_key": "INS-004",
                        "total_pending": "15837.5900",
                        "total_estimated": "0.00",
                        "total_programmed": "15837.5900"
                    },
                    {
                        "concept_key": "ISC-018",
                        "total_pending": "3207.7900",
                        "total_estimated": "0.00",
                        "total_programmed": "3207.7900"
                    },
                    {
                        "concept_key": "TIN-001",
                        "total_pending": "4624.5400",
                        "total_estimated": "0.00",
                        "total_programmed": "4624.5400"
                    },
                    {
                        "concept_key": "ULS-113",
                        "total_pending": "15910.7200",
                        "total_estimated": "0.00",
                        "total_programmed": "15910.7200"
                    }
                ],
                "general_programmed_sum": "0",
                "total_estimated": "0.00"
            },
            {
                "sub_line_items": [],
                "name": "EQUIPO",
                "parent_key": "",
                "total_programmed": "76141.4200",
                "general_estimated_sum": "0",
                "total_pending": "76141.4200",
                "general_pending_sum": "0",
                "greatest_parent": "",
                "key": "1.9",
                "concepts": [
                    {
                        "concept_key": "AB-VS-EQ01",
                        "total_pending": "7685.8200",
                        "total_estimated": "0.00",
                        "total_programmed": "7685.8200"
                    },
                    {
                        "concept_key": "AB-VS-EQ02",
                        "total_pending": "24353.2200",
                        "total_estimated": "0.00",
                        "total_programmed": "24353.2200"
                    },
                    {
                        "concept_key": "AB-VS-EQ03",
                        "total_pending": "44102.3800",
                        "total_estimated": "0.00",
                        "total_programmed": "44102.3800"
                    },
                    {
                        "concept_key": "AB-VS-EQ04",
                        "total_pending": "0.0000",
                        "total_estimated": "0.00",
                        "total_programmed": "0.0000"
                    }
                ],
                "general_programmed_sum": "0",
                "total_estimated": "0.00"
            }
        ],
        "global_total_pending": "5554298.2944",
        "global_total_estimated": "900.0"
    }

    FinancialAdvanceReport.generate_report(json)

    # return HttpResponse('Done')
    # return render(request, 'DataUpload/carga.html')


class GetFinancialReport(View):
    def get(self, request):
        project_id = request.GET.get('project_id')
        #detail_level = request.GET.get('detail_level')
        # Due to requirements issues, the detail level is no longer required to be dynamic. The report, from now on,
        # will be exported grouped by line_item.
        show_concepts = True


        # The next block is to force the second level of line items to work with the report. Keep in mind this won't work
        # on further versions
        # Block to delete:
        selected_line_items_array = api.ReportingUtilities.get_first_two_line_item_levels(project_id)
        # Ends block to delete.

        report_json = api.FinancialHistoricalProgressReport.get_report(project_id, selected_line_items_array)

        # return HttpResponse(Utilities.json_to_dumps(report_json),'application/json; charset=utf-8')

        file = FinancialAdvanceReport.generate_report(report_json, show_concepts)
        return file


class GetPhysicalFinancialAdvanceReport(View):
    def get(self, request):
        project_id = request.GET.get('project_id')
        detail_level = request.GET.get('detail_level')

        if detail_level == "c":
            show_concepts = True
        else:
            show_concepts = False

        # The next block is to force the second level of line items to work with the report. Keep in mind this won't work
        # on further versions
        # Block to delete:
        selected_line_items_array = api.ReportingUtilities.get_first_two_line_item_levels(project_id)
        # Ends block to delete.


        report_json = api.PhysicalFinancialAdvanceReport.get_report(project_id, selected_line_items_array)

        #return HttpResponse(Utilities.json_to_dumps(report_json),'application/json; charset=utf-8')

        file = PhysicalFinancialAdvanceReport.generate_report(report_json, show_concepts)
        return file

        #return HttpResponse(Utilities.json_to_dumps({}),'application/json; charset=utf-8')


class GetMainDashboard(View):
    def get(self, request):

        response_by_project = []
        access_set = AccessToProject.objects.filter(user__id=request.user.erpuser.id)
        for access in access_set:

            structured_response = {}

            response = api.PhysicalFinancialAdvanceReport.get_biddings_report(access.project.id)

            total_programmed = 0
            total_estimated = 0
            total_paid_estimated = 0
            for year in response:
                for month in year['months']:
                    total_programmed += month['month_program']
                    total_estimated += month['month_estimate']
                    total_paid_estimated += month['month_paid_estimate']

            percentaje_paid_estimated = 0
            percentaje_estimated = 0
            if total_programmed > 0:
                percentaje_paid_estimated = round((total_paid_estimated * 100 / total_programmed), 2)
                percentaje_estimated = round((total_estimated * 100 / total_programmed), 2)

            structured_response['schedule'] = response
            structured_response['general'] = {
                "general_programmed": total_programmed,
                "general_estimated": total_estimated,
                "general_paid_estimated": total_paid_estimated,
                "percentaje_paid_estimated": percentaje_paid_estimated,
                "percentaje_estimated": percentaje_estimated,
                "project_name" : access.project.nombreProyecto,
                "project_key" : access.project.key,
                "project_latitud" : access.project.latitud,
                "project_longitud" : access.project.longitud,
                "project_id" : access.project.id
            }

            response_by_project.append(structured_response)


        return HttpResponse(Utilities.json_to_dumps(response_by_project), 'application/json; charset=utf-8')


class GetDashboardByProject(View):
    def get(self, request):

        project_id = request.GET.get('project_id')
        project = Project.objects.get(pk=project_id)

        structured_response = {}
        response = api.PhysicalFinancialAdvanceReport.get_biddings_report(project.id)

        total_programmed = 0
        total_estimated = 0
        total_paid_estimated = 0
        for year in response:
            for month in year['months']:
                total_programmed += month['month_program']
                total_estimated += month['month_estimate']
                total_paid_estimated += month['month_paid_estimate']

        percentaje_paid_estimated=0
        percentaje_estimated = 0
        if total_programmed > 0:
            percentaje_paid_estimated = round((total_paid_estimated * 100 / total_programmed), 2)
            percentaje_estimated = round((total_estimated * 100 / total_programmed), 2)

        structured_response['schedule'] = response
        structured_response['general'] = {
            "general_programmed": total_programmed,
            "general_estimated": total_estimated,
            "general_paid_estimated": total_paid_estimated,
            "percentaje_paid_estimated": percentaje_paid_estimated,
            "percentaje_estimated": percentaje_estimated,
            "project_name" : project.nombreProyecto,
            "project_key" : project.key,
            "project_latitud" : project.latitud,
            "project_longitud" : project.longitud,
            "project_id" : project.id
        }

        return HttpResponse(Utilities.json_to_dumps(structured_response), 'application/json; charset=utf-8')


# Report to retrieve the json for every estimate in a project.
class GetEstimatesReportJson(View):
    def get(self, request):

        project_id = request.GET.get('project_id')
        response = api.EstimatesReport.getReport(project_id)

        return HttpResponse(Utilities.json_to_dumps(response), 'application/json; charset=utf-8')


class GetEstimatesReport(View):
    def get(self, request):
        project_id = request.GET.get('project_id')

        # Due to requirements issues, the detail level is no longer required to be dynamic. The report, from now on,
        # will be exported grouped by line_item.
        show_concepts = True

        responseJson = api.EstimatesReport.getReport(project_id)

        # return HttpResponse(Utilities.json_to_dumps(report_json),'application/json; charset=utf-8')

        file = EstimateReports.generate_report(responseJson, show_concepts)
        return file




class GetEstimateReportForContractors(View):
    def get(self, request):
        project_id = request.GET.get('project_id')

        information_json = api.EstimateReportForContractors.get_report(project_id)
        #return HttpResponse(Utilities.json_to_dumps(information_json),'application/json; charset=utf-8')

        file = EstimateReportsForContractors.generate_report(information_json)

        return file


class GetEstimateReportBySingleContractor(View):
    def get(self, request):
        project_id = request.GET.get('project_id')
        contractor_id = request.GET.get('contractor_id')

        information_json = api.EstimateReportBySingleContractor.get_report(project_id, contractor_id)
        #return HttpResponse(Utilities.json_to_dumps(information_json),'application/json; charset=utf-8')

        file = EstimateReportsBySingleContractor.generate_report(information_json)

        return file

class GetBudgetByContractorReport(View):
    def get(self, request):
        project_id = request.GET.get('project_id')
        contractor_id = request.GET.get('contractor_id')

        information_json = api.GetBudgetByContractorReport.get_report(project_id, contractor_id)
        #return HttpResponse(Utilities.json_to_dumps(information_json),'application/json; charset=utf-8')

        file = BudgetReportsByContractor.generate_report(information_json)

        return file

