# config-generator

this config-generator-WebApplication offers you the opportunity to generate configuration files for network devices.

## Install

create a python virtual environment
```bash
python -m venv venv
```

enter the venv  
Windows:
```bash
venv\scripts\activate
```
Linux:
```bash
source myenv/bin/activate
```

install all neccessary modules
```bash
pip install -r requirements.txt
```

navigate to the main applications folder - (in this case)
```
/config-generator/configgenerator/
```

initial Application Setup
```bash
python manage.py migrate
```

run the application (also in the directory of the main Application)
```bash
python manage.py runserver
```