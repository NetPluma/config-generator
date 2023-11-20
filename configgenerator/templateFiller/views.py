from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
import json
import jinja2
import yaml
# Create your views here.

#======================== Custom import =====================

#import templateHelper

def index(request):
    template = loader.get_template("templateFiller/templateFiller.html")
    context = { }
    return HttpResponse(template.render(context, request))

def generate_from_excel(request):
    template = loader.get_template("templateFiller/excelConfig.html")
    context = { }
    return HttpResponse(template.render(context, request))

def upload_excel(request):
    return

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