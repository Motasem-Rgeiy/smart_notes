from reportlab.platypus import SimpleDocTemplate , Paragraph , Spacer , Table , PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.graphics.shapes import Drawing, Line
from reportlab.lib import colors
from datetime import datetime
from io import BytesIO , StringIO
import json
import csv





def pdf_generation(note_objs):
        

     buffer = BytesIO()

       
       
     
     fileName = SimpleDocTemplate(buffer , pagesize = letter)
     styles = getSampleStyleSheet()
     content=  []

     for note_obj in note_objs:
        
        created_at = datetime.fromisoformat(f"{str(note_obj.created_at)}")
        updated_at = datetime.fromisoformat(f"{str(note_obj.updated_at)}")
        created_at_only = created_at.date()
        updated_at_only = updated_at.date()

        if not note_obj.category:
             category_name = None
        else:
             category_name = note_obj.category.name


        content.append(Table([[Paragraph('Title:', styles['Heading3']), Paragraph(f'{note_obj.title}', styles['Normal'])]], colWidths=[130, 150] , hAlign='LEFT'))
        content.append(Spacer(1 , 12))
        content.append(Table([[Paragraph('Category:', styles['Heading3']), Paragraph(f'{category_name}', styles['Normal'])]], colWidths=[130, 150] , hAlign='LEFT'))
        content.append(Spacer(1 , 12))
        content.append(Table([[Paragraph('Created:', styles['Heading3']), Paragraph(f'{created_at_only}', styles['Normal'])]], colWidths=[130, 150] , hAlign='LEFT'))
        content.append(Spacer(1 , 12))
        content.append(Table([[Paragraph('Last Modified:', styles['Heading3']), Paragraph(f'{updated_at_only}', styles['Normal'])]], colWidths=[130, 150] , hAlign='LEFT'))
        content.append(Spacer(1 , 12))
        # Drawing(width, height)
        line = Drawing(400, 10)
        # Line(x1, y1, x2, y2, strokeColor, strokeWidth)
        line.add(Line(0, 5, 400, 5, strokeColor=colors.black, strokeWidth=1))

        content.append(line)
        content.append(Paragraph('Content', styles['Heading3']))
        content.append(Spacer(1 , 5))
        content.append(Paragraph(f'{note_obj.description}', styles['Normal']))
        content.append(PageBreak())


        
     fileName.build(content)
     buffer.seek(0)

     return buffer
    



def txt_generation(note_obj):
    text_buffer = StringIO()
    text_buffer.write(f'{note_obj.description}')
    buffer = BytesIO(text_buffer.getvalue().encode('utf-8'))
    buffer.seek(0)
    return buffer





def json_generation(note_objs):
     data = {}
     for note_obj in note_objs:
          if not note_obj.category:
               category_name = None
          else:
               category_name = note_obj.category.name
          data[note_obj.pk] = {
               'title':note_obj.title,
               'category':category_name,
               'description':note_obj.description,
               'created_at': str(note_obj.created_at),
               'updated_at': str(note_obj.updated_at),
          }
          
          json_str = json.dumps(data , indent=4)
     buffer = BytesIO(json_str.encode('utf-8'))
     buffer.seek(0)
     return buffer





def csv_generation(note_objs):
        
        csv_buffer = StringIO()
        csvWriter = csv.writer(csv_buffer)

        for note_obj in note_objs:
          if not note_obj.category:
               category_name = None
          else:
               category_name = note_obj.category.name

          row = [note_obj.title , category_name , note_obj.description , note_obj.created_at , note_obj.updated_at]
          csvWriter.writerow(row)
        buffer = BytesIO(csv_buffer.getvalue().encode('utf-8'))
        buffer.seek(0)
        return buffer
