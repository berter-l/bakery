import io
from datetime import date, timedelta, timezone, datetime

from django.db.models import Count, Avg
from django.db.models import Sum, Q
from django.http import FileResponse
from fpdf import FPDF
from ninja import Router

from orders.models import Order, OrderItem


class PDF(FPDF):
    def header(self):
        today = date.today()
        one_month = timedelta(days=30)
        self.add_font(family='Roboto', fname='Roboto-Italic-VariableFont_wdth.ttf')
        self.set_font("Roboto", size=16)
        self.cell(30, 10, f"BAKERY SHOP - отчет о продажах с {today - one_month} по {today} ", align="C", center=True,
                  new_x="LMARGIN",
                  new_y="NEXT")
        self.line(x1=20, y1=20, x2=190, y2=20)
        self.ln(20)


def create_report():
    utc_now = datetime.now(timezone.utc)
    one_month = timedelta(days=30)
    TABLE_DATA = [
        ['название товара', 'количество (штук)', 'общая сумма (руб)'],
    ]
    data = OrderItem.objects.filter(Q(
        created_at__gte=(utc_now - one_month)) &
                                    Q(created_at__lte=utc_now)).select_related('product').values(
        'product__name'
    ).annotate(
        final_price=Sum('price'),
        quantity=Sum('quantity'),
        count=Count('id')
    ).order_by('-count')
    for item in data:
        TABLE_DATA.append([
            item['product__name'],
            str(item['quantity']),
            str(float(item['final_price']))
        ])

    buffer = io.BytesIO()
    pdf = PDF()
    pdf.add_page()
    pdf.add_font(family='Roboto', fname='Roboto-Italic-VariableFont_wdth.ttf', style='B')
    pdf.set_font("Roboto", size=16)
    pdf.cell(text='Отчет о всех проданных товаров за месяц', new_x='LMARGIN', new_y='NEXT', align='L')
    create_table(pdf, TABLE_DATA)
    pdf.ln(20)
    pdf.cell(text='ОБЩАЯ СТАТИСТИКА')
    pdf.ln(10)
    DATA_STAT = [
        ['Всего заказов', 'Общая выручка (руб)', 'Средний чек (руб)', 'Самый дорогой заказ (руб)', 'Самый дешевый '
                                                                                                   'заказ (руб)',
         'Потрачено'
         'бонусов']
    ]

    orders = Order.objects.filter(Q(
        created_at__gte=(utc_now - one_month)) &
                                  Q(created_at__lte=utc_now))
    bonus = sum([x.bonus_count for x in orders])
    ob_viruch = [x.final_price for x in orders]
    ob_suma = [item['final_price'] for item in data]
    DATA_STAT.append([
        str(len(orders)),
        str(sum(ob_viruch)),
        str(sum(ob_viruch) // len(orders)),
        str(max(ob_viruch)),
        str(min(ob_viruch)),
        str(bonus)

    ])
    create_table(pdf, DATA_STAT)
    pdf.ln(10)
    pdf.cell(text='ТОП ПОПУЛЯРНЫХ ТОВАРОВ')
    pdf.ln(10)
    sumator = {item['product__name']: (item['count']) for item in data}
    table = top_table(sumator, pdf)
    create_table(pdf, table)
    pdf.ln(10)
    pdf.cell(text='Доход с каждой категории')
    pdf.ln(10)
    create_table(pdf, top_category_table())
    pdf.output(buffer)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="report.pdf")


def top_table(data, pdf):
    TOP_TABLE = [
        ['Название', 'Количество заказов с этим товаром (штук)']
    ]
    for item in data:
        TOP_TABLE.append([
            item, str(data[item])
        ])
    return TOP_TABLE


def create_table(pdf, table_data):
    with pdf.table(text_align="CENTER") as table:
        for data_row in table_data:
            row = table.row()
            for datum in data_row:
                row.cell(datum)


def top_category_table():
    utc_now = datetime.now(timezone.utc)
    one_month = timedelta(days=30)
    data = data = OrderItem.objects.filter(Q(
        created_at__gte=(utc_now - one_month)) &
                                           Q(created_at__lte=utc_now)).select_related('product',
                                                                                      'product__category').values(
        'product__category__name'
    ).annotate(
        final_price=Sum('price')
    ).order_by('-final_price')
    TOP_CATEGORY_TABLE = [
        ['Название категории', 'Общая сумма покупок']
    ]
    for item in data:
        TOP_CATEGORY_TABLE.append([
            item['product__category__name'],
            str(item['final_price'])])
    return TOP_CATEGORY_TABLE