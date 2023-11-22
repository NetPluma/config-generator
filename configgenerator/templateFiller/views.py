from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
import json
import jinja2
import yaml
import datetime

# For Excel Interaction
import pandas

# forms

from .forms import ExcelUploadForm

# Create your views here.

#======================== Custom import =====================

#import templateHelper

#======================== Index Page =====================
def index(request):
    template = loader.get_template("templateFiller/templateFiller.html")
    context = { }
    return HttpResponse(template.render(context, request))



#======================== Excel Config Page =====================
def generate_from_excel(request):
    template = loader.get_template("templateFiller/excelConfig.html")
    # Document upload form
    form = ExcelUploadForm()
    context = {'form': form}
    return HttpResponse(template.render(context, request))



#======================== Upload Page for Excel-Spreadsheet =====================
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



#======================== Generate a single config =====================
# AJAX - posting YAML and Jinja Template    
def generate_config(request):
    if request.method == "POST":
        # prepare data from yaml and j2 input editors
        data = json.loads(request.body)
        yaml_content = data.get('yaml_content')
        jinja_content = data.get('jinja_content')
        try: 
            # checking the yaml structure for validity
            parsed_yaml_dict = yaml.safe_load(yaml_content)
        except yaml.YAMLError:
            # return an error if the yaml structure is wrong and therefore cant be used for the jinja template rendering
            return JsonResponse({'status': 'error', 'message': 'Invalid YAML'}, status=422)
        # setup jinja environment and render the template
        jinja_environment = jinja2.Environment()
        template = jinja_environment.from_string(jinja_content)
        resulting_config = template.render(parsed_yaml_dict)
        
        #print(yaml_content,"\n\n\n" ,jinja_content,"\n\n\n",resulting_config)

        return JsonResponse({'status': 'success', 'message': 'Data received', 'data': resulting_config}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)


#======================== Generate multiple config from spreadsheet =====================
# AJAX - generate multiple configs 
def generate_multiple_config(request):
    if request.method == "POST":
        # prepare data from yaml and j2 input editors
        data = json.loads(request.body)
        yaml_content = data.get('yaml_content')
        jinja_content = data.get('jinja_content')
        try:
            # checking the yaml structure for validity
            parsed_yaml = yaml.safe_load(yaml_content)
            converted_yaml_dict = {}
            for dict in parsed_yaml:
                converted_yaml_dict.update(dict)
            print(f"Combined DICT {converted_yaml_dict}\n\n")    
        except yaml.YAMLError:
            # return an error if the yaml structure is wrong and therefore cant be used for the jinja template rendering
            return JsonResponse({'status': 'error', 'message': 'Invalid YAML'}, status=422)
        
        # setup jinja environment
        jinja_environment = jinja2.Environment()
        template = jinja_environment.from_string(jinja_content)

        # update dict entries from excel with the content from yaml files
        # the list contains a dict for every entry in an excel file (so a dict for every device)
        # every dict gets the the content from the YAML file
        print(f"YAML: {converted_yaml_dict}")
        print(type(converted_yaml_dict))

        for individual_dict in request.session['spreadsheet_dict']:
            print(f"Device dict from spreadsheet {individual_dict}")
            individual_dict.update(converted_yaml_dict)        
            resulting_config = template.render(individual_dict)
            print(f"Resulting config {resulting_config}")

            # Getting the current date and formatting it as a string
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            with open(f"output/{current_date}_SWIS-SW{individual_dict['switch_number']}.txt", 'w') as file:
                file.write(resulting_config)
        #print(f"SESSION UPDATED DICT {request.session['spreadsheet_dict']}")
        
        return JsonResponse({'status': 'success', 'message': 'Data received', 'data': resulting_config}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Only POST allowed'}, status=405)
