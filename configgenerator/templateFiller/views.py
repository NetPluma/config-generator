from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
import json
import jinja2
import yaml

# For Excel Interaction
import pandas

# forms

from .forms import ExcelUploadForm

# Create your views here.

#======================== Custom import =====================

#import templateHelper

def index(request):
    template = loader.get_template("templateFiller/templateFiller.html")
    context = { }
    return HttpResponse(template.render(context, request))

def generate_from_excel(request):
    template = loader.get_template("templateFiller/excelConfig.html")
    form = ExcelUploadForm()
    context = {'form': form}
    return HttpResponse(template.render(context, request))

# AJAX - posting Excel, reading content and save it to session
def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the form

            # get file from request => print(raw_excel_file) -> gibt den Dateinamen zurück
            raw_excel_file = request.FILES['excel_file']

            # Read the Excel Data
            excel_content = pandas.read_excel(raw_excel_file)

            # Turn Excel Spreadsheet to Dict
            spreadsheet_dict = excel_content.to_dict(orient='records')
            request.session['spreadsheet_dict'] = spreadsheet_dict
            # Return a JSON response for Ajax requests
            return JsonResponse({'message': 'Success!','message': 'Spreadsheet received'}, status=200)

    return JsonResponse({'status': 'error', 'message': 'Invalid form'}, status=400)

# AJAX - posting YAML and Jinja Template    
def generate_config(request):
    if request.method == "POST":
        data = json.loads(request.body)
        yaml_content = data.get('yaml_content')
        jinja_content = data.get('jinja_content')
        try: 
            parsed_yaml_dict = yaml.safe_load(yaml_content)
        except yaml.YAMLError:
            return JsonResponse({'status': 'error', 'message': 'Invalid YAML'}, status=422)
        jinja_environment = jinja2.Environment()
        template = jinja_environment.from_string(jinja_content)
        resulting_config = template.render(parsed_yaml_dict)
        
        print(yaml_content,"\n\n\n" ,jinja_content,"\n\n\n",resulting_config)


        return JsonResponse({'status': 'success', 'message': 'Data received', 'data': resulting_config}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


# AJAX - generate multiple configs 
def generate_multiple_config(request):
    if request.method == "POST":
        data = json.loads(request.body)
        yaml_content = data.get('yaml_content')
        jinja_content = data.get('jinja_content')
        try: 
            parsed_yaml_dict = yaml.safe_load(yaml_content)
        except yaml.YAMLError:
            return JsonResponse({'status': 'error', 'message': 'Invalid YAML'}, status=422)
        
        # setup jinja environment
        jinja_environment = jinja2.Environment()
        template = jinja_environment.from_string(jinja_content)

        # update dict entries from excel with the content from yaml files
        for individual_dict in request.session['spreadsheet_dict']:
            individual_dict.update(parsed_yaml_dict)        
            resulting_config = template.render(individual_dict)
            print(f"Resulting config {resulting_config}")
        print(f"SESSION UPDATED DICT {request.session['spreadsheet_dict']}")
        
        return JsonResponse({'status': 'success', 'message': 'Data received', 'data': resulting_config}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)