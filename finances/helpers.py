from xhtml2pdf import pisa
from django.template.loader import render_to_string
from io import BytesIO



def render_to_pdf(template_path, context):
    html = render_to_string(template_path, context)

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)

    if pdf.err:
        return None
    
    return result.getvalue()