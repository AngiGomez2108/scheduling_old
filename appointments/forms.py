from django import forms
from django.forms import Form, ModelChoiceField, ModelForm
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from appointments.models import DocumentType, Person, PersonType, Citation, Place, Process, Department, City, Holiday, Functionary, Constraint

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field, Button, Row, Column, Hidden
from crispy_bootstrap5.bootstrap5 import FloatingField

class PersonSearchForm(Form):
    id_type_doc = ModelChoiceField(queryset = DocumentType.objects.all(), 
                                     widget=forms.Select(attrs={'class':'form-control'
    }))
    identification = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"
    }))

class CitationUpdateForm(ModelForm):
    class Meta:
        model = Citation
        fields =  ['id','status', 'date_creation', 'id_person', 'id_process', 'date', 'time', 'uuid']
        labels = {
             "id_person":"Persona ",
             "id_process": "Trámite ",
             "date":"Fecha ",
             "time":"Hora ",
             "id":"Id Cita ",             
         }
        
        exclude = ['id','uuid', 'status', 'date_creation']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False 
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'offset-1 col-lg-3'
        self.helper.field_class = 'col-lg-7 '
        self.helper.form_method = 'post'
        # self.helper.add_input(Button('back', "Regresar", css_class='btn btn-link me-5', 
         #                            onclick="window.location.href = '{}';".format(reverse('citation-list'))))
        #self.helper.add_input(Submit('submit', 'Actualizar', css_class="btn-success", attrs={'id': 'btnUpdate'}))
        # Agregar el widget HiddenInput al campo 'id'

        self.helper.layout = Layout(
            Field('id_person'),
            Field('id_process'),
            Field('date',title="Fecha", placeholder=""),
            Field('time',title="Hora", placeholder="")
        )

class CitationForm(ModelForm):
    place = ModelChoiceField(queryset = Place.objects.all(), 
                                     widget=forms.Select(attrs={'class':'form-control'
    }))
    id_process = ModelChoiceField(queryset = Process.objects.none(), 
                                     widget=forms.Select(attrs={'class':'form-control'
    }))
    date = forms.DateField()
    id_person = forms.HiddenInput
    time = forms.TimeField
    class Meta:
        model = Citation
        fields = '__all__'

class PersonForm(ModelForm):
    
    class Meta:
        model = Person
        fields = '__all__'
        labels = {
             "id_type_person":"Tipo de persona ",
             "id_type_doc": "Tipo de documento ",
             "identification":"Número documento ",
             "name":"Nombres ",
             "lastname":"Apellidos ",
             "cellphone": "Número de celular ",
             "email":"Correo Electrónico ",
             "address":"Dirección ",        
             "id_depto_address":"Departamento ",
             "id_city_address":"Municipio ",   
         }
        
        exclude = ['id']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False 
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'offset-1 col-md-4'
        self.helper.field_class = 'col-md-6 '
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Siguiente', css_class="btn-success offset-3"))
       
        self.helper.layout = Layout(

            Row(
                Column('id_type_person', css_class='col-md-6'),  # Ajusta la separación a la derecha
            ),
            Row(
                Column('id_type_doc', css_class='col-lg-6 pr-0 '),  # Ajusta la separación a la izquierda
                Column('identification', title="Número de identificación", placeholder="Número de identificación", css_class='col-lg-6 pr-3'),
            ),
            Row(
                Column('name', title="Nombres", placeholder="Nombres", css_class='col-lg-6'),
                Column('lastname', title="Apellidos", placeholder="Apellidos", css_class='col-lg-6'),
            ),
            Row(
                Column('cellphone', title="Número de celular o teléfono", placeholder="Número de celular o teléfono", css_class='col-lg-6'),
                Column('email', title="Correo electrónico", placeholder="correo@email.com", css_class='col-lg-6'),
            ),
            Row(
                Column('address', title="Dirección de Residencia", placeholder="Dirección de Residencia", css_class='col-lg-6'),
                Column('id_depto_address', title="Departamento de residencia", placeholder="Departamento de residencia", css_class='col-lg-6'),
            ),
             Row(
                Column('id_city_address', title="Municipio de residencia", placeholder="Municipio de residencia", css_class='col-lg-6'),
            )
            
        )
    
class PersonUpdateForm(ModelForm):
    
    class Meta:
        model = Person
        fields = '__all__'
        labels = {
             "id_type_person":"Tipo de persona ",
             "id_type_doc": "Tipo de documento ",
             "identification":"Número documento ",
             "name":"Nombres ",
             "lastname":"Apellidos ",
             "cellphone": "Número de celular ",
             "email":"Correo Electrónico ",
             "address":"Dirección ",        
             "id_depto_address":"Departamento ",
             "id_city_address":"Municipio ",   
         }
        
        exclude = ['id']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False 
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'offset-1 col-md-4'
        self.helper.field_class = 'col-md-6 '
        self.helper.form_method = 'post'
       
        self.helper.layout = Layout(

            Row(
                Column('id_type_person', css_class='col-md-6'),  # Ajusta la separación a la derecha
            ),
            Row(
                Column('id_type_doc', css_class='col-lg-6 pr-0 '),  # Ajusta la separación a la izquierda
                Column('identification', title="Número de identificación", placeholder="Número de identificación", css_class='col-lg-6 pr-3'),
            ),
            Row(
                Column('name', title="Nombres", placeholder="Nombres", css_class='col-lg-6'),
                Column('lastname', title="Apellidos", placeholder="Apellidos", css_class='col-lg-6'),
            ),
            Row(
                Column('cellphone', title="Número de celular o teléfono", placeholder="Número de celular o teléfono", css_class='col-lg-6'),
                Column('email', title="Correo electrónico", placeholder="correo@email.com", css_class='col-lg-6'),
            ),
            Row(
                Column('address', title="Dirección de Residencia", placeholder="Dirección de Residencia", css_class='col-lg-6'),
                Column('id_depto_address', title="Departamento de residencia", placeholder="Departamento de residencia", css_class='col-lg-6'),
            ),
             Row(
                Column('id_city_address', title="Municipio de residencia", placeholder="Municipio de residencia", css_class='col-lg-6'),
            )
            
        )

class FunctionaryForm(ModelForm):
    
    class Meta:
        model = Functionary
        fields = '__all__'
        labels = {
             "id_type_doc": "Tipo de documento ",
             "identification":"Número documento ",
             "name":"Nombres ",
             "lastname":"Apellidos ",
             "cellphone": "Número de celular ",
             "email":"Correo Electrónico ", 
             "id_place":"Dependencia: ",
         }
        
        exclude = ['id']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False 
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'offset-1 col-lg-4 h3'
        self.helper.field_class = 'col-lg-6 '
        self.helper.form_method = 'post'
        #self.helper.add_input(Submit('submit', 'Registrar', css_class="btn-success"))
       
        self.helper.layout = Layout(
            Field('id_type_doc'),
            Field('identification',title="Número de identificación", placeholder="Número de identificación"),
            Field('name',title="Nombres", placeholder="Nombres"),
            Field('lastname',title="Apellidos", placeholder="Apellidos"),
            Field('cellphone',title="Número de celular o teléfono", placeholder="Número de celular o teléfono"),
            Field('email',title="Correo electrónico", placeholder="correo@email.com"),
            Field('id_place'),
        )

class DepartmentForm(ModelForm): 
     class Meta:
        model = Department
        fields = ['id','name']
        labels = {
             "id":"Código Dane: ",
             "name":"Nombre: ",
         }
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False 
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'offset-1 col-lg-3'
        self.helper.field_class = 'col-lg-7 '
        self.helper.form_method = 'post'
        #self.helper.add_input(Button('back', "Regresar", css_class='btn btn-link me-5', 
        #                             onclick="window.location.href = '{}';".format(reverse('department-list'))))
        #self.helper.add_input(Submit('submit', 'Registrar', css_class="btn-success"))
        
        self.helper.layout = Layout(
            Field('id',title="Código Dane", placeholder="Código Dane"),
            Field('name',title="Nombre", placeholder="Nombre"),
        )

class CityForm(ModelForm):  
     class Meta:
        model = City
        fields = ['id','id_department','name']
        labels = {
             "id_department":"Departamento",
             "id":"Código Dane: ",
             "name":"Nombre: ",
         }
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False 
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'offset-1 col-lg-3'
        self.helper.field_class = 'col-lg-7 '
        self.helper.form_method = 'post'
        #self.helper.add_input(Button('back', "Regresar", css_class='btn btn-link me-5', 
        #                             onclick="window.location.href = '{}';".format(reverse('city-list'))))
        #self.helper.add_input(Submit('submit', 'Registrar', css_class="btn-success"))    
        self.helper.layout = Layout(
            Field('id_department',title="Departamento", placeholder="Departamento"),
            Field('id',title="Código Dane", placeholder="Código Dane"),
            Field('name',title="Nombre", placeholder="Nombre"),
        )

class DocumentTypeForm(ModelForm): 
     class Meta:
        model = DocumentType
        fields = ['id','name']
        labels = {
             "id":"Código: ",
             "name":"Nombre: ",
         }
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False 
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'offset-1 col-lg-3'
        self.helper.field_class = 'col-lg-7 '
        self.helper.form_method = 'post'
        #self.helper.add_input(Button('back', "Regresar", css_class='btn btn-link me-5', 
        #                             onclick="window.location.href = '{}';".format(reverse('document-type-list'))))
        #self.helper.add_input(Submit('submit', 'Registrar', css_class="btn-success"))
        
        self.helper.layout = Layout(
            Field('id',title="Código", placeholder="Código"),
            Field('name',title="Nombre", placeholder="Nombre"),
        )

class PersonTypeForm(ModelForm): 
     class Meta:
        model = PersonType
        fields = ['name']
        labels = {
             "name":"Nombre: ",
         }
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False 
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'offset-1 col-lg-3'
        self.helper.field_class = 'col-lg-7 '
        self.helper.form_method = 'post'
        #self.helper.add_input(Button('back', "Regresar", css_class='btn btn-link me-5', 
        #                             onclick="window.location.href = '{}';".format(reverse('person-type-list'))))
        #self.helper.add_input(Submit('submit', 'Registrar', css_class="btn-success"))
        
        self.helper.layout = Layout(
            Field('name',title="Nombre", placeholder="Nombre"),
        )

class PlaceForm(ModelForm): 
     class Meta:
        model = Place
        fields = ['name']
        labels = {
             "name":"Nombre: ",
         }
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False 
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'offset-1 col-lg-3'
        self.helper.field_class = 'col-lg-7 '
        self.helper.form_method = 'post'
        #self.helper.add_input(Submit('submit', 'Registrar', css_class="btn-success offset-3"))

        #self.helper.add_input(Button('back', "Regresar", css_class='btn btn-secondary ', 
        #                             onclick="window.location.href = '{}';".format(reverse('place-list'))))
        
        self.helper.layout = Layout(
            Field('name',title="Nombre", placeholder="Nombre"),
        )

class ProcessForm(ModelForm):   
     class Meta:
        model = Process
        fields = ['id','id_place','name','id_functionary', 'time','timetable']
        exclude = ['id']
        labels = {
             "id_place":"Dependencia: ",
             "name":"Nombre de Trámite: ",
             'id_functionary':"Funcionario: ",
             'time':"Tiempo(minutos)",
             'timetable':'',
         }
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False 
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'offset-1 col-lg-4 h2'
        self.helper.field_class = 'col-lg-7 '
        self.helper.form_method = 'post'
        self.helper.attrs = {'onsubmit': 'return validateForm();'}
        #self.helper.add_input(Button('back', "Regresar", css_class='btn btn-secondary', 
        #                             onclick="window.location.href = '{}';".format(reverse('process-list'))))
        #self.helper.add_input(Submit('submit', 'Registrar', css_class="btn-success" ))
        
        self.helper.layout = Layout(
            Row(
                Column('id_place', css_class='col-md-6'),
                Column('name', css_class='col-md-6'),
                Column('id_functionary', css_class='col-md-6'),
                Column('time', css_class='col-md-6'),
            ),
            Hidden('timetable', " ", id='timetable'),
        )

#no se usa
class ConstraintForm(ModelForm):  
    place = ModelChoiceField(queryset = Place.objects.all(), 
                                     widget=forms.Select(attrs={'label':'Dependencia','class':'form-control'
    }))
    id_process = ModelChoiceField(queryset = Process.objects.none(), 
                                     widget=forms.Select(attrs={'class':'form-control'
    }))
    class Meta:
        model = Constraint
        fields = ['id','id_process','day','time']
        exclude = ['id']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False 
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'offset-1 col-lg-4'
        self.helper.field_class = 'col-lg-7 '
        self.helper.form_method = 'post'
        self.helper.add_input(Button('back', "Regresar", css_class='btn btn-link me-5', 
                                     onclick="window.location.href = '{}';".format(reverse('process-list'))))
        self.helper.add_input(Submit('submit', 'Registrar', css_class="btn-success"))
        
      


class HolidayForm(ModelForm):
    class Meta:
        model = Holiday
        fields = ['date']
        labels = {
             "date":"Fecha: ",
         }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False 
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'offset-1 col-lg-3 h3'
        self.helper.field_class = 'col-lg-7 '
        self.helper.form_method = 'post'
        #self.helper.add_input(Submit('submit', 'Registrar', css_class="btn-success offset-3"))

        #self.helper.add_input(Button('back', "Regresar", css_class='btn btn-secondary', 
        #                             onclick="window.location.href = '{}';".format(reverse('holiday-list'))))
        
        self.helper.layout = Layout(
            Field('date',title="Fecha", placeholder="Seleccione una fecha"),
        )

#--- Search Forms
class CitationSearchForm(forms.Form):
    person = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(attrs={'placeholder': 'Nombre'}),
        required=False
    )

    process = forms.ModelChoiceField(
        queryset = Process.objects.all(),
        widget=forms.Select(
            attrs={'label':'Trámite','class':'form-control'}
        ),
        required=False
    )

    date = forms.DateField(
        label="Fecha",
        widget=forms.DateInput(attrs={'class': 'form-control'}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False 
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'offset-1 col-lg-3'
        self.helper.field_class = 'col-lg-7 '
        self.helper.form_method = 'post'
        #self.helper.add_input(Submit('submit', 'Registrar', css_class="btn-success"))
        
        self.helper.layout = Layout(
            Field('person', title="Nombre", placeholder="Nombre"),
            Field('process', title="Trámite"),
            Field('date', title="Fecha", placeholder="Fecha"), 
        )

class CitationCancelForm(forms.Form):

    type_doc = ModelChoiceField(queryset = DocumentType.objects.all(), 
                                     widget=forms.Select(attrs={'class':'form-control'
    }),required=True,
    label="Tipo de documento:")
    

    identification = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", 
    }), required=True,
    label="Identificación:")

    email = forms.EmailField(
        widget=forms.TextInput(attrs={"class": "form-control"
    }),required=True,
    label="Correo electrónico:")

    uuid = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"
    }),required=True,
    label="Código cita:")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False 
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'offset-1 col-lg-3 h2'
        self.helper.field_class = 'col-lg-7 '
        self.helper.form_method = 'post'
        #self.helper.add_input(Submit('submit', 'Registrar', css_class="btn-success"))
        
        self.helper.layout = Layout(
            Field('type_doc', title="Tipo de Documento", required= True),
            Field('identification', title="Número de documento"),
            Field('email', title="Correo electrónico"), 
            Field('uuid', title="Código de la cita"), 
        )

class CitationPersonConsultForm(forms.Form):
    
    STATUS_CHOICES = [
        ('A', 'Abiertas'),
        ('C', 'Cerradas'),
    ]

    type_doc = ModelChoiceField(queryset = DocumentType.objects.all(), 
                                     widget=forms.Select(attrs={'class':'form-control'
    }), label="Tipo de documento:")

    identification = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"
    }), label="Identificación:")

    email = forms.EmailField(
        widget=forms.TextInput(attrs={"class": "form-control"
    }), label="Correo electrónico:")

    status = forms.ChoiceField(choices = STATUS_CHOICES, 
                                     widget=forms.Select(attrs={'class':'form-control'
    }),label="Estado cita:")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False 
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'offset-1 col-lg-3 h2'
        self.helper.field_class = 'col-lg-7 '
        self.helper.form_method = 'post'
        #self.helper.add_input(Submit('submit', 'Registrar', css_class="btn-success"))
        
        self.helper.layout = Layout(
            Field('type_doc', title="Tipo de Documento", required= True),
            Field('identification', title="Número de documento"),
            Field('email', title="Correo electrónico"), 
            Field('status', title="Estado de la cita"), 
        )