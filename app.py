from flask import Flask, render_template_string, request
from lxml import etree
import os

app = Flask(__name__)

def validate_xml(xml_file, xsd_file):
    # Load XML and XSD files
    xml_parser = etree.XMLParser(remove_blank_text=True)
    xml_tree = etree.parse(xml_file, parser=xml_parser)
    xml_schema_doc = etree.parse(xsd_file)
    xml_schema = etree.XMLSchema(xml_schema_doc)
    
    # Validate XML against XSD
    try:
        xml_schema.assertValid(xml_tree)
        return []
    except etree.DocumentInvalid as e:
        return str(e).splitlines()

@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    
    if request.method == 'POST':
        xml_file = request.files['xml'].read()
        xml_path = 'uploaded.xml'
        
        with open(xml_path, 'wb') as file:
            file.write(xml_file)
        
        xsd_path = 'mil_std_6016.xsd'
        errors = validate_xml(xml_path, xsd_path)
        
        # Clean up the uploaded XML file
        os.remove(xml_path)
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>XML Structure Validation Errors</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container">
            <h1 class="mt-4">XML Structure Validation</h1>
            <form method="post" enctype="multipart/form-data" class="mt-4">
                <div class="form-group">
                    <label for="xml">Upload XML File</label>
                    <input type="file" class="form-control-file" id="xml" name="xml" required>
                </div>
                <button type="submit" class="btn btn-primary">Validate</button>
            </form>
            {% if errors %}
                <ul class="list-group mt-4">
                    {% for error in errors %}
                        <li class="list-group-item list-group-item-danger">{{ error }}</li>
                    {% endfor %}
                </ul>
            {% else %}
                <p class="alert alert-success mt-4">XML is valid according to the XSD.</p>
            {% endif %}
        </div>
    </body>
    </html>
    '''
    
    return render_template_string(template, errors=errors)

if __name__ == '__main__':
    app.run(debug=True)