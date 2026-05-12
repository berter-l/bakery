from django.http import HttpResponse, FileResponse
from ninja import Router
from fpdf import FPDF
import io

from reports.services import create_report

router = Router(tags=["reports"])


@router.get('reports/')
def report(request):
    return create_report()
