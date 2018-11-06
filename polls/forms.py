from django import forms
from django.forms import formsets
from django.forms import formset_factory

from polls.models import Question, Choice

from django.core.exceptions import ValidationError

class SimpleForm(forms.Form):
    HIGHER  = 0
    PEER    = 1
    AUTO    = 2
    STUDENT = 3

    SURVEY_TYPE_CHOICES = ((HIGHER, "Superiores"),
                           (PEER, "Pares"),
                           (AUTO, "Autoevaluación"),
                           (STUDENT, "Alumnos"))
    
    name = forms.CharField(label="Nombre")
    email = forms.EmailField(label="email", widget=forms.EmailInput(
        attrs={
            "placeholder":"Ingresa el email de GOOGLE, no de otra plataforma",
        }
    ))
    question = forms.ModelMultipleChoiceField(label="Pregunta", queryset=Question.objects)

    def __init__(self, queryset_personalizada, *args, **kwargs):
        super(SimpleForm, self).__init__(*args, **kwargs)
        self.fields['name'].initial = "Fulanito"
        self.fields['question'].queryset = queryset_personalizada        


    class Meta:
        pass
    #     error_messages = {
    #         "name": {'required': "This field is required"},
    #         "description": {'required': "This field is required"},
    #         "category": {'required': "This field is required"},
    #         "user": {'required': "This field is required"},
    #         "country": {'required': "This field is required"},
    #     }
    #     fields = ['name', 'description', 'category', 'user', 'country']
    #     labels = {
    #         "name": "Name",
    #         'description':'Description',
    #         'category': "Category",
    #         'user': 'User',
    #         'country': "Country"
    #     }
    #     widgets = {
    #         'name': forms.TextInput(attrs={
    #             "class":"form-control",
    #             "placeholder":"Write a name here"
    #         }),
    #         'description': forms.Textarea(attrs={
    #             "class":"form-control",
    #             "placeholder":"Add a description here",
    #             'rows':"2",
    #             'cols':"5"
    #         }),
    #         'country': forms.Select(attrs={
    #             'class':"form-control"
    #         })
    #     }
    

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['question', 'choice_text']

        labels = {
            'question':"Pregunta",
            'choice_text': "Texto de la alternativa"
        }

    def __init__(self, user, *args, **kwargs):
        super(ChoiceForm, self).__init__(*args, **kwargs)
        self.fields['question'].queryset = Question.objects.filter(user=user)

class ChoiceFormSet(formsets.BaseFormSet):
    def __init__(self, user, *args, **kwargs):
        self.user = kwargs.get('user')
        super(ChoiceFormSet, self).__init__(*args, **kwargs)
            
    def forms(self):
        """
        Instantiate forms at first property access.
        """
        # DoS protection is included in total_form_count()
        forms = [self._construct_form(i, self.user) for i in range(self.total_form_count())]
        return forms
    


# ModelForm EXAMPLE
# class FieldLinkCreateForm(forms.ModelForm):
#     """Class to create new fieldlink"""
    
#     def __init__(self, *args, **kwargs):
#         super(FieldLinkCreateForm, self).__init__(*args, **kwargs)
#         self.fields["connection"].widget.attrs['style'] = "display:none;"
#         self.fields['bi_field'].widget.attrs['class'] = 'form-control choiceinputfield'
#         self.fields['pp_field'].widget.attrs['class'] = 'form-control choiceinputfield'

#     class Meta:
#         model = FieldLink
#         fields = ['connection', 'pp_field', 'bi_field']
#         labels = {
#             "connection": "",
#             "bi_field": "hitmapBI attribute",
#             "pp_field": "MyHitmap attribute"
#         }

#     def clean(self):
#         cleaned_data = super(FieldLinkCreateForm, self).clean()
#         connection = cleaned_data.get("connection")
#         bi_field = cleaned_data.get("bi_field")
#         pp_field = cleaned_data.get("pp_field")

#         IS_NUMBER = [Field.FLOAT, Field.INTEGER]

#         if connection and bi_field and pp_field:
#             try:
#                 FieldLink.objects.get(connection=connection, bi_field=bi_field, pp_field=pp_field)
#                 raise forms.ValidationError(_("This combination of (Connection, BI attribute, PP attribute) already exists."), code="invalid")
#             except FieldLink.DoesNotExist:
#                 pass
        
#         if bi_field:
#             # pp_field is number but bi_field not.
#             if FieldLink.PP_FIELDS_TYPE[pp_field] in IS_NUMBER and bi_field.datatype not in IS_NUMBER:
#                 raise forms.ValidationError(_("Attribute datatypes not match."), code='invalid')
            
#             # pp_field is different than bi_field
#             elif bi_field.datatype != FieldLink.PP_FIELDS_TYPE[pp_field]:
#                 raise forms.ValidationError(_("Attribute datatypes not match."), code='invalid')
                
#         return cleaned_data


# USING MEDIA CLASS
# class SelectSurveyForm(forms.Form):
#     class Media:
#         js = ('assets/js/plugins/forms/styling/uniform.min.js',
#               'assets/js/plugins/forms/selects/select2.min.js',
#               'assets/js/pages/form_inputs.js',
#               'assets/js/pages/all_widgets.js')
        
#     survey = forms.ModelChoiceField(queryset=Survey.objects.all(), label="Seleccionar encuesta", widget=WIDGET_SELECT, required=False)




############################
######   FORMSETS   ########
############################

# class NewImportFormStep2FormSet(forms.formsets.BaseFormSet):
#     PLACE_FIELDS = [
#             'codigo',
#             'longitud',
#             'latitud',
#             'nombre',
#             'direccion',
#             'fecha de apertura',
#     ]

#     REQUIRED_FIELDS_TO_CREATE_PLACES = [
#         'codigo',
#         'longitud',
#         'latitud',
#         'nombre',
#         'direccion',        
#     ]
    
#     def __init__(self, *args, **kwargs):
#         self.column_choices = kwargs.pop('column_choices')
#         self.import_object = kwargs.pop('import_object')
#         super(NewImportFormStep2FormSet, self).__init__(*args, **kwargs)
    
#     @cached_property
#     def forms(self):
#         """
#         Instantiate forms at first property access.
#         """
#         # DoS protection is included in total_form_count()
#         forms = [self._construct_form(i, column_choices=self.column_choices) for i in range(self.total_form_count())]
#         return forms
    
#     def get_metadata_sheet(self):
#         metadata = []
#         for form in self.forms:
#             d = form.cleaned_data
#             column = d['column']
#             import_as = d['import_as']
#             description = d.get('description', '')
#             if import_as != None:
#                 metadata.append(
#                     {'nombre':column,
#                      'tipo de dato':import_as,
#                      'description':description
#                     })
#         return metadata

#     def clean(self):
#         if any(self.errors):
#             return

#         assigned_placefields = []
#         duplicates = False

#         for form in self.forms:
#             d = form.cleaned_data
#             action = d.get('import_as')
#             if action in self.PLACE_FIELDS and action in assigned_placefields:
#                 raise ValidationError(_("Can't repeat option when is not a datatype option."), code="invalid")
#             elif action in self.PLACE_FIELDS:
#                 assigned_placefields.append(action)

#         if self.import_object.is_for_upload and 'codigo' not in assigned_placefields:
#             raise ValidationError(_("You must link 'Unique code' to a column."), code="invalid")
        
#         if not self.import_object.is_for_upload:
#             for required_field in self.REQUIRED_FIELDS_TO_CREATE_PLACES:
#                 if required_field not in assigned_placefields:
#                     raise ValidationError(_("You must assing 'Unique code', 'Longitude', 'Latitude', 'Name', 'Address' to a column"), code="invalid")

#         return self.cleaned_data


