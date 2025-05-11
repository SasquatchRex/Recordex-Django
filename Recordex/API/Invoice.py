from django.template.defaultfilters import center
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from .models import Invoice, InvoiceItem
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from PIL import Image, ImageDraw, ImageFont
import os
from decimal import Decimal
from django.conf import settings
import re
from django.http import FileResponse,HttpResponseNotFound

from .serializers import InvoiceItemSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_invoice(request):
    data = request.data

    with transaction.atomic():
        invoice = Invoice.objects.create(
            creator = request.user,
            date = data["Date"],

            to_Name = data["To Name"],
            to_PAN = data["To PAN"],
            from_Name = data["From Name"],
            from_PAN = data["From PAN"],

            Total=Decimal(data['Total']),
            VAT_Amount=Decimal(data['VAT Amount']),
            Discount_Percentage=Decimal(data['Discount Percentage']),
            Total_Amount=Decimal(data['Total Amount']),
            Taxable_Amount = Decimal(data['Taxable Amount']),
            Remarks=data['Remarks']
        )

        for item in data['Invoice Items']:
            InvoiceItem.objects.create(
                invoice=invoice,
                HS_Code=item.get('H.S Code'),
                Name=item['Name'],
                Quantity=Decimal(item['Quantity']),
                Rate=Decimal(item['Rate']),
                Unit = item['Unit'],
                Amount=Decimal(item['Amount'])
            )

    return Response({'message': 'Invoice created successfully','id': invoice.id},status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def invoice_list(request):
    from_date = request.GET.get('from')
    to_date = request.GET.get('to')

    invoices = Invoice.objects.all()

    if from_date and to_date:
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)
        if from_date and to_date:
            invoices = invoices.filter(date__range=(from_date, to_date))


    data = [
        {
            "id": invoice.id,
            "creator": invoice.creator.username if invoice.creator else None,
            "date": str(invoice.date.date()),
            "To Name": invoice.to_Name,
            "To PAN" : invoice.to_PAN,

            "From Name" : invoice.from_Name,
            "From PAN" : Decimal(invoice.from_PAN),

            "Total" : Decimal(invoice.Total),
            "VAT Amount" : Decimal(invoice.VAT_Amount),
            "Discount Percentage" : Decimal(invoice.Discount_Percentage),
            "Total Amount" : Decimal(invoice.Total_Amount),
            "Taxable Amount" : Decimal(invoice.Taxable_Amount),
            "Remarks": str(invoice.Remarks),

            # "items" : [{
            #     "HS Code" :item.HS_Code,
            #     "Name" : str(item.Name),
            #     "Quantity" : Decimal(item.Quantity),
            #     "Rate": Decimal(item.Rate),
            #     "Unit": str(item.Unit),
            #     "Amount": Decimal(item.Amount)
            #
            # }
            # for item in invoice.Items.all()
            # ]

        }
        for invoice in invoices
    ]

    return JsonResponse(data, safe=False)



@api_view(['POST','GET'])
def billPreview(request):
    export_path = os.path.join(settings.BASE_DIR, "static", "export", "preview.png")
    if request.method =="POST":
        print(request)
        data = request.data

        image_path = os.path.join(settings.BASE_DIR, "static", 'bill.png')
        image = Image.open(image_path)

        namepos = (359,504)
        datepos = (1343,395)
        billdatepos = (1343,455)
        SNpos =150 #800
        HSpos = 200
        itempos = 370
        qtypos = 920
        unitpos = 1030
        ratepos = 1145
        amountpos =1335
        remarkspos = (168,1764)
        starting_y = 800
        multiply_y = 1

        SN = 1


        draw = ImageDraw.Draw(image)
        font_size = 40
        font_path = "arial.ttf"
        text_color = (0,0,0)
        font1 = ImageFont.truetype("arial.ttf", 40)
        font2 = ImageFont.truetype("arial.ttf", 24)
        font3 = ImageFont.truetype("arial.ttf", 32)

        discount_amount = (float(data["Discount Percentage"]) * float(data['Total']) /100).__round__(2)



        draw.text(namepos, data['To Name'], fill=text_color, font=font3)
        draw.text(datepos, str(data['Date']), fill=text_color, font=font3)
        draw.text(billdatepos, str(data['Date']), fill=text_color, font=font3)
        draw_text_in_box(draw, number_to_words(float(data['Total Amount'])), font3, box=(168,1764, 1000, 1900))

        draw_text_in_box(draw, str(int(float(data['Total']))), font3, box=(amountpos,1725, 1483, 1736),center=True)
        draw_text_in_box(draw, str(int((int(float(data['Total'])) - float(data['Total'])) * 100)), font3,box=(1500, 1725, 1550, 1725), center=True)

        draw_text_in_box(draw, str(int(discount_amount)), font3, box=(amountpos,1770, 1483, 1770),center=True)
        draw_text_in_box(draw, str(int((int(discount_amount) - discount_amount) * 100)), font3,box=(1500, 1770, 1550, 1770), center=True)

        draw_text_in_box(draw, str(int(float(data['Taxable Amount']))), font3, box=(amountpos,1815, 1483, 1815),center=True)
        draw_text_in_box(draw, str(int((int(float(data['Taxable Amount'])) - float(data['Taxable Amount'])) * 100)), font3,box=(1500, 1815, 1550, 1815), center=True)

        draw_text_in_box(draw, str(int(float(data['VAT Amount']))), font3, box=(amountpos,1860, 1483, 1860),center=True)
        draw_text_in_box(draw, str(-int((int(float(data['VAT Amount'])) - float(data['VAT Amount'])) * 100)), font3,box=(1500, 1860, 1550, 1860), center=True)

        draw_text_in_box(draw, str(int(float(data['Total Amount']))), font3, box=(amountpos,1905, 1483, 1905),center=True)
        draw_text_in_box(draw, str(- int((int(float(data['Total Amount'])) - float(data['Total Amount'])) * 100)), font3,box=(1500, 1905, 1550, 1905), center=True)


        # serializer = dataItemSerializer(data.Items.all(),many=True)

        for item in data['Invoice Items']:
            multiply_y = 1
            # draw.text((SNpos,starting_y), str(SN), fill=text_color, font=font2)
            # draw.text((HSpos,starting_y), str(item['HS_Code']), fill=text_color, font=font2)

            lines_SN = draw_text_in_box(draw, str(SN), font2, box=(SNpos, starting_y, 180, starting_y),center=True)
            lines_HS =draw_text_in_box(draw, str(item['H.S Code']), font2, box=(HSpos, starting_y, 340, starting_y),center=True)
            lines_Name= draw_text_in_box(draw, str(item['Name']), font2, box=(itempos, starting_y, 880, 1700),center=False)
            lines_Qty =draw_text_in_box(draw, str(item['Quantity']), font2, box=(qtypos, starting_y, 1000, starting_y),center=True)
            lines_Unit =draw_text_in_box(draw, str(item['Unit']), font2, box=(unitpos, starting_y, 1115, starting_y),center=True)
            lines_Rate =draw_text_in_box(draw, str(item['Rate']), font2, box=(ratepos, starting_y, 1300, starting_y),center=True)
            lines_Amount =draw_text_in_box(draw, str(int(float(item['Amount']))), font2, box=(amountpos, starting_y, 1483, starting_y),center=True)
            lines_Paise =draw_text_in_box(draw, str(int((int(float(item['Amount'])) - float(item['Amount']))*100)), font2, box=(1500, starting_y, 1550, starting_y),center=True)

            multiply_y = max(lines_SN, lines_HS, lines_Name, lines_Qty, lines_Unit, lines_Rate, lines_Amount, lines_Paise)


            starting_y += (32*multiply_y)
            SN +=1




        # safe_name = re.sub(r'[\\/*?:"<>|]', "_", data['To Name'])
        # export_filename = f"{safe_name}_{data['Total Amount']}.png"
        # export_path = os.path.join(settings.BASE_DIR, "static", "export", "preview".png)
        image.save(export_path)
        return Response({'status': 'Image generated successfully'},status=status.HTTP_200_OK)

    elif request.method == 'GET':
        if os.path.exists(export_path):
            return FileResponse(open(export_path, 'rb'), content_type='image/png')
        else:
            return HttpResponseNotFound('Image not found')


@api_view(['GET'])
def billGenerator(request,pk):
    invoice = get_object_or_404(Invoice,pk=pk)

    image_path = os.path.join(settings.BASE_DIR, "static", 'bill.png')
    image = Image.open(image_path)

    namepos = (359,504)
    datepos = (1343,395)
    billdatepos = (1343,455)
    SNpos =150 #800
    HSpos = 200
    itempos = 370
    qtypos = 920
    unitpos = 1030
    ratepos = 1145
    amountpos =1335
    remarkspos = (168,1764)
    starting_y = 800
    multiply_y = 1

    SN = 1


    draw = ImageDraw.Draw(image)
    font_size = 40
    font_path = "arial.ttf"
    text_color = (0,0,0)
    font1 = ImageFont.truetype("arial.ttf", 40)
    font2 = ImageFont.truetype("arial.ttf", 24)
    font3 = ImageFont.truetype("arial.ttf", 32)

    discount_amount = (invoice.Discount_Percentage * invoice.Total /100).__round__(2)



    draw.text(namepos, invoice.to_Name, fill=text_color, font=font3)
    draw.text(datepos, str(invoice.date.date()), fill=text_color, font=font3)
    draw.text(billdatepos, str(invoice.date.date()), fill=text_color, font=font3)
    draw_text_in_box(draw, number_to_words(invoice.Total_Amount), font3, box=(168,1764, 1000, 1900))

    draw_text_in_box(draw, str(int(float(invoice.Total))), font3, box=(amountpos,1725, 1483, 1736),center=True)
    draw_text_in_box(draw, str(int((int(float(invoice.Total)) - float(invoice.Total)) * 100)), font3,box=(1500, 1725, 1550, 1725), center=True)

    draw_text_in_box(draw, str(int(discount_amount)), font3, box=(amountpos,1770, 1483, 1770),center=True)
    draw_text_in_box(draw, str(int((int(discount_amount) - discount_amount) * 100)), font3,box=(1500, 1770, 1550, 1770), center=True)

    draw_text_in_box(draw, str(int(float(invoice.Taxable_Amount))), font3, box=(amountpos,1815, 1483, 1815),center=True)
    draw_text_in_box(draw, str(int((int(float(invoice.Taxable_Amount)) - float(invoice.Taxable_Amount)) * 100)), font3,box=(1500, 1815, 1550, 1815), center=True)

    draw_text_in_box(draw, str(int(float(invoice.VAT_Amount))), font3, box=(amountpos,1860, 1483, 1860),center=True)
    draw_text_in_box(draw, str(-int((int(float(invoice.VAT_Amount)) - float(invoice.VAT_Amount)) * 100)), font3,box=(1500, 1860, 1550, 1860), center=True)

    draw_text_in_box(draw, str(int(float(invoice.Total_Amount))), font3, box=(amountpos,1905, 1483, 1905),center=True)
    draw_text_in_box(draw, str(- int((int(float(invoice.Total_Amount)) - float(invoice.Total_Amount)) * 100)), font3,box=(1500, 1905, 1550, 1905), center=True)


    serializer = InvoiceItemSerializer(invoice.Items.all(),many=True)

    for item in serializer.data:
        multiply_y = 1
        # draw.text((SNpos,starting_y), str(SN), fill=text_color, font=font2)
        # draw.text((HSpos,starting_y), str(item['HS_Code']), fill=text_color, font=font2)

        lines_SN = draw_text_in_box(draw, str(SN), font2, box=(SNpos, starting_y, 180, starting_y),center=True)
        lines_HS =draw_text_in_box(draw, str(item['HS_Code']), font2, box=(HSpos, starting_y, 340, starting_y),center=True)
        lines_Name= draw_text_in_box(draw, str(item['Name']), font2, box=(itempos, starting_y, 880, 1700),center=False)
        lines_Qty =draw_text_in_box(draw, str(item['Quantity']), font2, box=(qtypos, starting_y, 1000, starting_y),center=True)
        lines_Unit =draw_text_in_box(draw, str(item['Unit']), font2, box=(unitpos, starting_y, 1115, starting_y),center=True)
        lines_Rate =draw_text_in_box(draw, str(item['Rate']), font2, box=(ratepos, starting_y, 1300, starting_y),center=True)
        lines_Amount =draw_text_in_box(draw, str(int(float(item['Amount']))), font2, box=(amountpos, starting_y, 1483, starting_y),center=True)
        lines_Paise =draw_text_in_box(draw, str(int((int(float(item['Amount'])) - float(item['Amount']))*100)), font2, box=(1500, starting_y, 1550, starting_y),center=True)

        multiply_y = max(lines_SN, lines_HS, lines_Name, lines_Qty, lines_Unit, lines_Rate, lines_Amount, lines_Paise)


        starting_y += (32*multiply_y)
        SN +=1




    safe_name = re.sub(r'[\\/*?:"<>|]', "_", invoice.to_Name)
    export_filename = f"{safe_name}_{invoice.Total_Amount}.png"
    export_path = os.path.join(settings.BASE_DIR, "static", "export", export_filename)
    image.save(export_path)

    if os.path.exists(export_path):
        return FileResponse(open(export_path, 'rb'), content_type='image/png')
    else:
        return HttpResponseNotFound('Image not found')




def get_text_width(text, font):
    bbox = font.getbbox(text)
    return bbox[2] - bbox[0]

def draw_text_in_box(draw, text, font, box, fill=(0, 0, 0), line_spacing=5, center=False):
    x1, y1, x2, y2 = box
    max_width = x2 - x1
    words = text.split()
    lines = []
    line = []

    # Word wrapping logic
    for word in words:
        test_line = ' '.join(line + [word])
        w = get_text_width(test_line, font)
        if w <= max_width:
            line.append(word)
        else:
            lines.append(line)
            line = [word]
    if line:
        lines.append(line)

    y_text = y1
    line_height = font.getbbox('Hg')[3] - font.getbbox('Hg')[1]

    for i, line in enumerate(lines):
        is_last_line = i == len(lines) - 1
        line_text = ' '.join(line)

        if center:
            line_width = get_text_width(line_text, font)
            x_text = x1 + (max_width - line_width) // 2
            draw.text((x_text, y_text), line_text, font=font, fill=fill)
        elif is_last_line or len(line) == 1:
            draw.text((x1, y_text), line_text, font=font, fill=fill)
        else:
            total_words_width = sum(get_text_width(word, font) for word in line)
            space_count = len(line) - 1
            total_spacing = max_width - total_words_width
            space_width = total_spacing // space_count
            extra_space = total_spacing % space_count

            x_text = x1
            for j, word in enumerate(line):
                draw.text((x_text, y_text), word, font=font, fill=fill)
                word_width = get_text_width(word, font)
                if j < space_count:
                    x_text += word_width + space_width + (1 if j < extra_space else 0)
                else:
                    x_text += word_width

        y_text += line_height + line_spacing

    return len(lines)





def number_to_words(n):
    ones = [
        '', 'One', 'Two', 'Three', 'Four', 'Five', 'Six',
        'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve',
        'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen',
        'Eighteen', 'Nineteen'
    ]
    tens = [
        '', '', 'Twenty', 'Thirty', 'Forty', 'Fifty',
        'Sixty', 'Seventy', 'Eighty', 'Ninety'
    ]
    units = [
        (10000000, 'Crore'),
        (100000, 'Lakh'),
        (1000, 'Thousand'),
        (100, 'Hundred')
    ]

    def two_digit_words(n):
        if n < 20:
            return ones[n]
        else:
            return tens[n // 10] + (' ' + ones[n % 10] if n % 10 != 0 else '')

    def convert(n):
        if n == 0:
            return 'Zero'
        parts = []
        for value, name in units:
            q, n = divmod(n, value)
            if q:
                parts.append(convert(q) + ' ' + name)
        if n >= 100:
            q, r = divmod(n, 100)
            parts.append(ones[q] + ' Hundred')
            if r:
                parts.append('and ' + two_digit_words(r))
        elif n > 0:
            parts.append(two_digit_words(n))
        return ' '.join(parts)

    rupees = int(n)
    paise = round((n - rupees) * 100)

    rupee_part = convert(rupees).strip()
    paise_part = convert(paise).strip() if paise else ''

    if rupees and paise:
        return f"{rupee_part} Rupees and {paise_part} Paisa only"
    elif rupees:
        return f"{rupee_part} Rupees only"
    elif paise:
        return f"{paise_part} Paisa only"
    else:
        return "Zero Rupees only"












