from django import forms

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()

    # custom validation for validating the Filetype of the submitted file
    def clean_excel_file(self):
        # Accessing the file from the cleaned_data dictionary
        file = self.cleaned_data['excel_file']
        # Checking if the filename ends with .xlsx
        if not file.name.endswith('.xlsx'):
            # Raising a validation error if the file is not an Excel file.
            raise forms.ValidationError("Only .xlsx files are allowed.")
        # If the file passes the check, return it.
        return file
