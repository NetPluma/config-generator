from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
import json
import jinja2
import yaml
import datetime
import os
# For Excel Interaction
import pandas

# forms
from .forms import ExcelUploadForm
from .templateHelper import check_mac_formatting
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
# AJAX - generate multiple configs for devices and also prepares the dhcp configuration
def generate_multiple_config(request):
    if request.method == "POST":
        generated_config_count = 0

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
        except yaml.YAMLError:
            # return an error if the yaml structure is wrong and therefore cant be used for the jinja template rendering
            return JsonResponse({'status': 'error', 'message': 'Invalid YAML'}, status=422)
        
        # setup jinja environment
        jinja_environment = jinja2.Environment()
        template = jinja_environment.from_string(jinja_content)
        
        with open(f"input/dhcp_config.j2", 'r') as dhcp_template_file:
            dhcp_template = jinja_environment.from_string(dhcp_template_file.read())

        # update dict entries from excel with the content from yaml files
        # the list contains a dict for every entry in an excel file (so a dict for every device)
        # every dict gets the the content from the YAML file

        # Getting the current date and formatting it as a string
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        with open(f"output/{current_date}_DHCP_Config.cfg", 'a') as dhcp_config_file:
            # generate a config for each specified device
            for individual_dict in request.session['spreadsheet_dict']:
                individual_dict.update(converted_yaml_dict)
                device_name = f"{individual_dict['hostname']}"

                # Take corrective measures IF the formatting of data wrong
                individual_dict['mac'], individual_dict['mac_without_colon'] = check_mac_formatting(individual_dict['mac'])

                # render a new config
                resulting_config = template.render(individual_dict)
                # write the finished config to the file system
                with open(f"output/{device_name}_{individual_dict['mac_without_colon']}.cfg", 'w') as file:
                    file.write(resulting_config)

                dhcp_config_entry = dhcp_template.render(individual_dict)
                # Add an entry to the dhcp config file for this device
                dhcp_config_file.write(dhcp_config_entry)
                
                # for Metadata
                generated_config_count += 1    

        return JsonResponse({'status': 'success', 'message': f"Successfully created {generated_config_count} Configs", 'data': generated_config_count}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Only POST allowed'}, status=405)
