import json
from typing import Any, Dict
from django import http
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView, View
from django.views.generic import TemplateView, FormView
from appointments.models import Person, Citation, Process, Functionary
from appointments.models import Department, City, DocumentType, PersonType, Place, Holiday, Constraint
from appointments.forms import PersonForm, PersonSearchForm, CitationForm, CitationUpdateForm, DepartmentForm, CityForm, DocumentTypeForm, PersonTypeForm, PlaceForm, ProcessForm, ConstraintForm, HolidayForm, FunctionaryForm, CitationSearchForm, CitationCancelForm, CitationPersonConsultForm, PersonUpdateForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from datetime import datetime, timedelta, time
from django.http import Http404

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# Nos sirve para redireccionar despues de una acción revertiendo patrones de expresiones regulares 
from django.urls import reverse
import urllib.parse as urlparse
# Habilitamos el uso de mensajes en Django
from django.contrib import messages 
# Habilitamos los mensajes para class-based views 
from django.contrib.messages.views import SuccessMessageMixin 
# Habilitamos los formularios en Django
from django import forms

from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from django.db.models import ProtectedError
from django.db.models import Q
from .utils import render_to_pdf 
 


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
#------ Constratint
class ConstraintCreateView(CreateView):
    model = Constraint
    form_class = ConstraintForm
    template_name = 'appointment/constraint/create.html'
    def get_success_url(self):
        return reverse('process-list')


#------ Citation
class CitationListView(ListView):
    model = Citation
    template_name = 'citation/list.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        citas = Citation.objects.filter(status='A')
        context["citations"] = citas
        return context

class CitationCreateView(TemplateView):
    template_name = 'appointment/create.html'
    #form=CitationForm
    #form = CitationForm(initial={'id_type_doc': request.GET.get('id_type_doc'),'identification':request.GET.get('identification')})

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        dataRequest = json.loads(request.body) 
        action = dataRequest['action']
        print('**************---->>>>>>>>>>>>>>>>>',action)
        # #print("en PSOT",request.POST['action'])
        try:
             data = []
             if action == 'search_process_id': #si se da en buscar al change de dependencia 
                 for i in Process.objects.filter(id_place=dataRequest['id']):
                     data.append({'id':i.id, 'name':i.name})
                 return JsonResponse(data, safe=False)
             elif action == 'change_date': #si cambia fecha
                 times = []
                 timesSend = []
                 #times.append({"horas":[]})
                 
                 print("dataRequest['date']-->",dataRequest['date'])
                 date_object = datetime.strptime(dataRequest['date'], '%Y-%m-%d')
                 #print("processs.time-->",process.time)
                 if dataRequest['id_process']!= "":
                    process =  Process.objects.get(pk=dataRequest['id_process'])
                    rangeTime = timedelta(minutes=int(process.time))
                    # print("process.timetable--> ",json.loads(process.timetable)[str(date_object.weekday())]) 
                    # print("date_object.weekday()-->",date_object.weekday())
                    times=json.loads(process.timetable)[str(date_object.weekday())]
                    for i in Citation.objects.filter(date=dataRequest['date'], id_process= dataRequest['id_process']      ):
                        hour=int(str(i.time).split(':')[0])
                        minute=str(i.time).split(':')[1]
                        am_pm = 'AM' if hour<12 else 'PM'
                        hour= hour-12 if hour>12 else hour
                        hourstr='0'+str(hour) if hour<10 else str(hour)
                        deleteTime = hourstr +":"+minute+" "+am_pm #hora a eliminar por estar reservada
                        j=0 #indice para recorrer arreglo times
                        #print("times-->",times)
                        for time in times:
                           #print("time-->",time+"----")
                           #print("deleteTime-->",deleteTime+"----")
                           if time==deleteTime:  
                                #print("eliminar.....")
                                times.pop(j)
                           j=j+1
                        #print("data--->****** "+str(hour)+":"+minute+" "+am_pm) 
                        #data.append(str(i.time).split(':')[0])
                    # if date_object.weekday() != 4: #si es diferente a viernes
                    #     timeStart = datetime.strptime('08:00', '%H:%M')
                    #     timeEnd = time(18, 0) 
                    #     noon = time(12,0)
                    #     while timeStart.time() < timeEnd:
                    #        if timeStart.time() < noon or timeStart.time() >= time(14,0):   
                    #             times.append(str(timeStart.time().strftime('%I:%M %p')))
                    #        timeStart += rangeTime
                    # else:
                    #     timeStart = datetime.strptime('07:00', '%H:%M')
                    #     timeEnd = time(15, 0)
                    #     noon = time(12,0)
                    #     while timeStart.time() < timeEnd:
                    #         times.append(str(timeStart.time().strftime('%I:%M %p')))
                    #         timeStart += rangeTime
                 timesSend.append({'times':[times]})
                 return JsonResponse(timesSend, safe=False)
             else: #si se da en registrar 

                # Verificar si ya sacó un cita el mismo día
                citations = Citation.objects.filter(id_person=dataRequest['id_person'], date=dataRequest['date'])
                if (citations.exists()):
                    raise ValueError("Ya sacó una cita para este día")
                form = CitationForm(request.POST or None)
                person=Person.objects.get(id=dataRequest['id_person'])
                process=Process.objects.get(id=dataRequest['id_process'])
                citation = form.save(commit=False)
                citation.id_person = person
                citation.id_process = process
                citation.date = dataRequest['date']
                citation.uuid = dataRequest['uuid']
                print("----- dataRequest['time'] -----", dataRequest['time'])
                citation.time = dataRequest['time']
                citation.save()
                #if form.is_valid():
                #    form.save()		
                messages.success(request, 'Cita registrada correctamente.')
                #    form = CitationForm()
                # else:
                #    messages.error(request, 'Error al insertar factura. Revise los datos.')
                #context = {'form': form }      
                #return render(request, 'factura.html', context)
                data.append({'success':True})
                date = datetime.strptime(citation.date, "%Y-%m-%d")
                citation_date = date.strftime("%d-%m-%Y")
                citation_time = convert_to_12_hour_format2(citation.time)
                send_email(person.email, person.name, person.lastname, citation_date, citation_time, process.name, process.id_place,  process.id_functionary, citation.uuid, citation.id_person.identification ,citation.id_person.id_type_doc.id )
                return JsonResponse(data, safe=False)
        except ValueError as e:
            messages.error(request, 'El usuario ya tiene asignada una cita para este día. No puede sacar más de una cita el mismo día')
            data.append({'success': False})
            data.append({'error': 'El usuario ya tiene asignada una cita para este día. No puede sacar más de una cita el mismo día'})
            return JsonResponse(data, safe=False)
        except Exception as e:
             messages.error(request, 'Error registrar Cita. Favor revise los datos.')
             data.append({'success':False})
             data.append({'error':'Error registrar Cita. Favor revise los datos.'})
             return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        person = Person.objects.get(
                id = self.request.GET.get('id')
            )
        form = CitationForm(initial={'id_type_doc': person.id_type_doc,'identification':person.identification, 'id_person':person})
        context['form'] = form
        context['person'] = person
        return context

class CitationCancelFormView(FormView):
    template_name = 'appointment/person_citation/cancel_citation_form.html' 
    form_class = CitationCancelForm
class CitationCancelView(TemplateView):
    template_name = 'appointment/person_citation/cancel_citation.html'  

    def get(self, request, *args, **kwargs):
        uuid_param = self.request.GET.get('uuid')
        type_doc_param = self.request.GET.get('typedoc')
        identification_param = self.request.GET.get('identification')
        email_param = self.request.GET.get('email')
        citation_id = self.request.GET.get('id')
        if citation_id:
            try:
                obj = Citation.objects.get(id=citation_id)
                obj.delete()
                return JsonResponse({'success': 'Cita cancelada exitosamente'})
            except:
                return JsonResponse({'error': 'La cita no se pudo cancelar, o no existe'})
        else: 
            try:
                citation = Citation.objects.get(uuid=uuid_param, id_person__email=email_param, id_person__identification=identification_param, id_person__id_type_doc=type_doc_param, status="A")
                context = {
                    'nombre_solicitante': citation.id_person.name + " " + citation.id_person.lastname,
                    'identificacion': citation.id_person.identification,
                    'tramite': citation.id_process.name,
                    'fecha_creacion': citation.date_creation,
                    'dependencia': citation.id_process.id_place.name,
                    'funcionario': citation.id_process.id_functionary.name + " " + citation.id_process.id_functionary.lastname,
                    'uuid': citation.uuid,
                    'fecha': citation.date,
                    'hora': citation.time,
                    'citation_id': citation.id
                }
            except Exception as e:
                print(e)
                error_message = "La cita no fue encontrada."
                context = {'error_message': error_message}
            return self.render_to_response(context)

class CitationPersonConsultFormView(FormView):
    template_name = 'appointment/person_citation/citation_person_consult_form.html' 
    form_class = CitationPersonConsultForm

class CitationPersonConsult(ListView): 
    model = Citation
    template_name = 'appointment/person_citation/citation_person_consult.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        typedoc = self.request.GET.get('typedoc')
        identification = self.request.GET.get('identification')
        email = self.request.GET.get('email')
        status = self.request.GET.get('status')
        
        citas = Citation.objects.filter(id_person__email=email, id_person__identification=identification, id_person__id_type_doc=typedoc, status=status)
        context["citations"] = citas
        return context
    
class CloseProcess(View):
    def get(self, request, *args, **kwargs):
        id = self.request.GET.get('id')
        citation = Citation.objects.get(id=id)
        result = {'error': 'El trámite no pudo ser atendido'}
        if citation:
            citation.status = 'C'
            citation.save()  # Guarda los cambios en la base de datos
            result = {'success': 'Trámite atendido correctamente'}
        return JsonResponse(result, safe=False)
    
class CitationUpdateView(UpdateView):
    model = Citation
    form_class = CitationUpdateForm
    template_name = 'citation/update.html'
    success_url ="../list"

    def form_valid(self, form):
        response = super().form_valid(form)
        cleaned_data = form.cleaned_data

        # Imprime los datos en la consola del servidor
        print("Datos validados del formulario:", cleaned_data)
    
        data = {'message': 'Registro actualizado correctamente.'}
        return JsonResponse(data)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {'error': 'Error al actualizar el registro. Verifica los datos.'}
        return JsonResponse(data, status=400)

    #def post(self, request, *args, **kwargs):
        # Obtén el formulario con los datos de la solicitud POST
    #    pass 


   
class CitationDetail(DetailView): 
    model = Citation
    template_name = 'citation/detail.html'

# class CitationDeleteView(DeleteView):
#     model = Citation
#     success_url = "../list"
#     template_name = 'citation/delete.html'
#     def form_valid(self, form):
#         try:
#             return super().form_valid(form)
#         except ProtectedError as e:
#             messages.warning(self.request, f"No es posible eliminar la cita '{self.object}' porque está siendo referenciada por otra tabla.")
#             return self.form_invalid(None)


class CitationDeleteView(DeleteView):
    model = Citation
    success_url = "../list"
    template_name = 'citation/delete.html'
    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            return JsonResponse({'success': 'Registro eliminado exitosamente'})
        except Exception as e:
            return JsonResponse({'error': f'Error al eliminar el registro: {str(e)}'}, status=500)
        

#------- Person
class PersonListView(ListView):
    model = Person
    template_name = 'person/list.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context
    
class PersonSearchView(TemplateView):
    template_name = 'person/search_person.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

        
    def post(self, request, *args, **kwargs):
        data = {}
        register_person=False
        #person=Person
        
        id_type_doc = request.POST['id_type_doc']
        identification = request.POST['identification']
        print("----->",request.POST['identification'])
        try:
            print("UNO")
            person = Person.objects.get(
                id_type_doc = id_type_doc,
                identification=identification
            )
            print("DOS")
            print("person-->",person)
            # Agregar los datos iniciales como parámetros en la URL de redirección
            url_redirect = reverse('citation-create')  # Reemplaza 'nueva_vista' con el nombre de la vista del nuevo formulario
            url_redirect += '?' + urlparse.urlencode({'id':person.id})
            #form = CitationForm(initial={'id_type_doc': id_type_doc,'identification':identification})
            #return render(request, 'appointment/create.html', {'form': form, 'person':person})
            return redirect(url_redirect)
            #return redirect(reverse(CitationCreateView),id=person.id)
            #return HttpResponseRedirect(reverse('citation-create',args=({person,})))
        except Exception as e:
            data['error'] = str(e)
            print("data['error']--->",data['error'])
            #form = PersonForm(initial={'id_type_doc': id_type_doc,'identification':identification})
            #return render(request, 'person/create.html', {'form': form})
            #url_redirect = reverse('person-create',kwargs={'id_type_doc': id_type_doc,'identification':identification})  # Reemplaza 'nueva_vista' con el nombre de la vista del nuevo formulario
            url_redirect = reverse('person-create')
            url_redirect += '?' + urlparse.urlencode({'id_type_doc': id_type_doc,'identification':identification})
            return redirect(url_redirect)
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['form'] = PersonSearchForm
        return context
    
class PersonDetail(DetailView): 
    model = Person
    template_name = 'person/detail.html'

class PersonCreateView(CreateView):
    model = Person
    #form=PersonForm
    form_class = PersonForm
    template_name = 'person/create.html'
    
    def get_success_url(self):
        #print("ingresa a initial en get_success_url-->",self.request.GET.get('id_type_doc'))
        #print("AQUIIIII-------->:",self.object.id)
        #return reverse('citation-create', kwargs={'id': self.object.id})
        #return reverse('citation-create', args = [self.object.id] )
        #url_redirect = reverse('citation-create')  # Reemplaza 'nueva_vista' con el nombre de la vista del nuevo formulario
        #url_redirect += '?' + urlparse.urlencode({'id':self.object.id})
        if self.request.GET.get('id_type_doc')!= None: #si viene de creacion de cita
            url_redirect = reverse('citation-create')
            url_redirect += '?' + urlparse.urlencode({'id':self.object.id})
            #form = CitationForm(initial={'id_type_doc': id_type_doc,'identification':identification})
            #return render(request, 'appointment/create.html', {'form': form, 'person':person})
            return url_redirect
        else: #si viene de creacion de persona
            return reverse('person-list')

    def get_initial(self):
        # Obtiene los datos de inicialización de los argumentos de la URL
        initial = super().get_initial()
        #print("ingresa a initial-->",self.request.GET.get('id_type_doc'))
       # form = PersonForm(initial={'id_type_doc':  self.kwargs.get('id_type_doc'),'identification': self.kwargs.get('identification')})
        #id_type_doc = self.kwargs.get('id_type_doc')
        id_type_doc = self.request.GET.get('id_type_doc')
        identification = self.request.GET.get('identification')
        # Agrega otros campos según tus necesidades
        initial['id_type_doc'] = id_type_doc
        initial['identification'] = identification
        # Agrega otros campos al diccionario 'initial'
        return initial
    
    #def form_valid(self, form):
    #    response = super().form_valid(form)
    #    cleaned_data = form.cleaned_data

        # Imprime los datos en la consola del servidor
    #    print("Datos validados del formulario:", cleaned_data)
    
    #    data = {'message': 'Registro actualizado correctamente.'}
    #   return JsonResponse(data)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {'error': 'Error al actualizar el registro. Verifica los datos.'}
        return JsonResponse(data, status=400)

    # def get_context_data(self, **kwargs: Any):
    #     context = super().get_context_data(**kwargs)
    #     self.form_class = PersonForm(initial={'id_type_doc': self.request.GET.get('id_type_doc'),'identification':self.request.GET.get('identification')})
    #     #context['form'] = form
    #     return context

class PersonUpdateView(UpdateView):
    model = Person
    form_class = PersonUpdateForm
    template_name = 'person/update.html'
    success_url ="../list"

    def form_valid(self, form):
        response = super().form_valid(form)
        cleaned_data = form.cleaned_data

        # Imprime los datos en la consola del servidor
        print("Datos validados del formulario:", cleaned_data)
    
        data = {'message': 'Registro actualizado correctamente.'}
        return JsonResponse(data)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {'error': 'Error al actualizar el registro. Verifica los datos.'}
        return JsonResponse(data, status=400)

class PersonDeleteView(DeleteView):
    model = Person
    success_url = "../list"
    template_name = 'person/delete.html'
    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            return JsonResponse({'success': 'Registro eliminado exitosamente'})
        except Exception as e:
            return JsonResponse({'error': f'Error al eliminar el registro: {str(e)}'}, status=500)


#------- Functionary
class FunctionaryListView(ListView):
    model = Functionary
    template_name = 'appointment/functionary/list.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context

class FunctionaryCreateView(CreateView):
    model = Functionary
    form_class = FunctionaryForm
    template_name = 'appointment/functionary/create.html'
    def get_success_url(self):
        return reverse('functionary-list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        cleaned_data = form.cleaned_data

        # Imprime los datos en la consola del servidor
        print("Datos validados del formulario:", cleaned_data)
    
        data = {'message': 'Registro actualizado correctamente.'}
        return JsonResponse(data)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {'error': 'Error al actualizar el registro. Verifica los datos.'}
        return JsonResponse(data, status=400)

class FunctionaryDetail(DetailView): 
    model = Functionary
    template_name = 'appointment/functionary/detail.html'

class FunctionaryUpdateView(UpdateView):
    model = Functionary
    form_class = FunctionaryForm
    template_name = 'appointment/functionary/update.html'
    success_url ="../list"

    def form_valid(self, form):
        response = super().form_valid(form)
        cleaned_data = form.cleaned_data

        # Imprime los datos en la consola del servidor
        print("Datos validados del formulario:", cleaned_data)
    
        data = {'message': 'Registro actualizado correctamente.'}
        return JsonResponse(data)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {'error': 'Error al actualizar el registro. Verifica los datos.'}
        return JsonResponse(data, status=400)

class FunctionaryDeleteView(DeleteView):
    model = Functionary
    success_url = "../list"
    template_name = 'appointment/functionary/delete.html'

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            return JsonResponse({'success': 'Registro eliminado exitosamente'})
        except Exception as e:
            return JsonResponse({'error': f'Error al eliminar el registro: {str(e)}'}, status=500)

#------- City
class CityListView(ListView):
    model = City
    template_name = 'appointment/city/list.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context
    
class CityCreateView(CreateView):
    model = City
    form_class = CityForm
    template_name = 'appointment/city/create.html'
    def get_success_url(self):
        return reverse('city-list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        cleaned_data = form.cleaned_data

        # Imprime los datos en la consola del servidor
        print("Datos validados del formulario:", cleaned_data)
    
        data = {'message': 'Registro actualizado correctamente.'}
        return JsonResponse(data)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {'error': 'Error al actualizar el registro. Verifica los datos.'}
        return JsonResponse(data, status=400)

class CityUpdateView(UpdateView):
    model = City
    form_class = CityForm
    template_name = 'appointment/city/update.html'
    success_url ="../list"

    def form_valid(self, form):
        response = super().form_valid(form)
        cleaned_data = form.cleaned_data

        # Imprime los datos en la consola del servidor
        print("Datos validados del formulario:", cleaned_data)
    
        data = {'message': 'Registro actualizado correctamente.'}
        return JsonResponse(data)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {'error': 'Error al actualizar el registro. Verifica los datos.'}
        return JsonResponse(data, status=400)

class CityDeleteView(DeleteView):
    model = City
    success_url = "../list"
    template_name = 'appointment/city/delete.html'
    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            return JsonResponse({'success': 'Registro eliminado exitosamente'})
        except Exception as e:
            return JsonResponse({'error': f'Error al eliminar el registro: {str(e)}'}, status=500)


#------- Department
class DepartmentListView(ListView):
    model = Department
    template_name = 'appointment/department/list.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context

class DepartmentCreateView(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'appointment/department/create.html'
    def get_success_url(self):
        return reverse('department-list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        cleaned_data = form.cleaned_data

        # Imprime los datos en la consola del servidor
        print("Datos validados del formulario:", cleaned_data)
    
        data = {'message': 'Registro actualizado correctamente.'}
        return JsonResponse(data)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {'error': 'Error al actualizar el registro. Verifica los datos.'}
        return JsonResponse(data, status=400)

class DepartmentUpdateView(UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'appointment/department/update.html'
    success_url ="../list"

    def form_valid(self, form):
        response = super().form_valid(form)
        cleaned_data = form.cleaned_data

        # Imprime los datos en la consola del servidor
        print("Datos validados del formulario:", cleaned_data)
    
        data = {'message': 'Registro actualizado correctamente.'}
        return JsonResponse(data)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {'error': 'Error al actualizar el registro. Verifica los datos.'}
        return JsonResponse(data, status=400)
    
class DepartmentDeleteView(DeleteView):
    model = Department
    success_url = "../list"
    template_name = 'appointment/department/delete.html'

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            return JsonResponse({'success': 'Registro eliminado exitosamente'})
        except Exception as e:
            return JsonResponse({'error': f'Error al eliminar el registro: {str(e)}'}, status=500)

#------- DocumentType
class DocumentTypeListView(ListView):
    model = DocumentType
    template_name = 'appointment/document_type/list.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context

class DocumentTypeCreateView(CreateView):
    model = DocumentType
    form_class = DocumentTypeForm
    template_name = 'appointment/document_type/create.html'
    def get_success_url(self):
        return reverse('document-type-list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        cleaned_data = form.cleaned_data

        # Imprime los datos en la consola del servidor
        print("Datos validados del formulario:", cleaned_data)
    
        data = {'message': 'Registro actualizado correctamente.'}
        return JsonResponse(data)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {'error': 'Error al actualizar el registro. Verifica los datos.'}
        return JsonResponse(data, status=400)

class DocumentTypeUpdateView(UpdateView):
    model = DocumentType
    form_class = DocumentTypeForm
    template_name = 'appointment/document_type/update.html'
    success_url ="../list"   

    def form_valid(self, form):
        response = super().form_valid(form)
        cleaned_data = form.cleaned_data

        # Imprime los datos en la consola del servidor
        print("Datos validados del formulario:", cleaned_data)
    
        data = {'message': 'Registro actualizado correctamente.'}
        return JsonResponse(data)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {'error': 'Error al actualizar el registro. Verifica los datos.'}
        return JsonResponse(data, status=400)

class DocumentTypeDeleteView(DeleteView):
    model = DocumentType
    success_url = "../list"
    template_name = 'appointment/document_type/delete.html'
    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            return JsonResponse({'success': 'Registro eliminado exitosamente'})
        except Exception as e:
            return JsonResponse({'error': f'Error al eliminar el registro: {str(e)}'}, status=500)
        
#------- PersonType
class PersonTypeListView(ListView):
    model = PersonType
    template_name = 'appointment/person_type/list.html'
    paginate_by = 100  # if pagination is desired
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context

class PersonTypeCreateView(CreateView):
    model = PersonType
    form_class = PersonTypeForm
    template_name = 'appointment/person_type/create.html'
    def get_success_url(self):
        return reverse('person-type-list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        cleaned_data = form.cleaned_data

        # Imprime los datos en la consola del servidor
        print("Datos validados del formulario:", cleaned_data)
    
        data = {'message': 'Registro actualizado correctamente.'}
        return JsonResponse(data)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {'error': 'Error al actualizar el registro. Verifica los datos.'}
        return JsonResponse(data, status=400)
    
class PersonTypeUpdateView(UpdateView):
    model = PersonType
    form_class = PersonTypeForm
    template_name = 'appointment/person_type/update.html'
    success_url ="../list"    

    def form_valid(self, form):
        response = super().form_valid(form)
        cleaned_data = form.cleaned_data

        # Imprime los datos en la consola del servidor
        print("Datos validados del formulario:", cleaned_data)
    
        data = {'message': 'Registro actualizado correctamente.'}
        return JsonResponse(data)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {'error': 'Error al actualizar el registro. Verifica los datos.'}
        return JsonResponse(data, status=400)

class PersonTypeDeleteView(DeleteView):
    model = PersonType
    success_url = "../list"
    template_name = 'appointment/person_type/delete.html'
    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            return JsonResponse({'success': 'Registro eliminado exitosamente'})
        except Exception as e:
            return JsonResponse({'error': f'Error al eliminar el registro: {str(e)}'}, status=500)

#------ Place
class PlaceListView(ListView):
    model = Place
    template_name = 'appointment/place/list.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context

class PlaceCreateView(CreateView):
    model = Place
    form_class = PlaceForm
    template_name = 'appointment/place/create.html'
    def get_success_url(self):
        return reverse('place-list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        cleaned_data = form.cleaned_data

        # Imprime los datos en la consola del servidor
        print("Datos validados del formulario:", cleaned_data)
    
        data = {'message': 'Registro actualizado correctamente.'}
        return JsonResponse(data)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {'error': 'Error al actualizar el registro. Verifica los datos.'}
        return JsonResponse(data, status=400)

class PlaceUpdateView(UpdateView):
    model = Place
    form_class = PlaceForm
    template_name = 'appointment/place/update.html'
    success_url ="../list"

    def form_valid(self, form):
        response = super().form_valid(form)
        cleaned_data = form.cleaned_data

        # Imprime los datos en la consola del servidor
        print("Datos validados del formulario:", cleaned_data)
    
        data = {'message': 'Registro actualizado correctamente.'}
        return JsonResponse(data)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {'error': 'Error al actualizar el registro. Verifica los datos.'}
        return JsonResponse(data, status=400)

class PlaceDeleteView(DeleteView):
    model = Place
    success_url = "../list"
    template_name = 'appointment/place/delete.html'
    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            return JsonResponse({'success': 'Registro eliminado exitosamente'})
        except Exception as e:
            return JsonResponse({'error': f'Error al eliminar el registro: {str(e)}'}, status=500)
        


#------ Process
class ProcessListView(ListView):
    model = Process
    template_name = 'appointment/process/list.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context
    
class ProcessCreateView(CreateView):
    model = Process
    form_class = ProcessForm
    template_name = 'appointment/process/create.html'
    
    def get_success_url(self):
        return reverse('process-list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        cleaned_data = form.cleaned_data

        # Imprime los datos en la consola del servidor
        print("Datos validados del formulario:", cleaned_data)
    
        data = {'message': 'Registro actualizado correctamente.'}
        return JsonResponse(data)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {'error': 'Error al actualizar el registro. Verifica los datos.'}
        return JsonResponse(data, status=400)
    
class ProcessDetail(DetailView): 
    model = Process
    template_name = 'appointment/process/detail.html'
    
class ProcessUpdateView(UpdateView):
    model = Process
    form_class = ProcessForm
    template_name = 'appointment/process/update.html'
    success_url ="../list"

    def form_valid(self, form):
        response = super().form_valid(form)
        cleaned_data = form.cleaned_data

        # Imprime los datos en la consola del servidor
        print("Datos validados del formulario:", cleaned_data)
    
        data = {'message': 'Registro actualizado correctamente.'}
        return JsonResponse(data)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {'error': 'Error al actualizar el registro. Verifica los datos.'}
        return JsonResponse(data, status=400)

class ProcessDeleteView(DeleteView):
    model = Process
    success_url ="../list"
    template_name = 'appointment/process/delete.html'
    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            return JsonResponse({'success': 'Registro eliminado exitosamente'})
        except Exception as e:
            return JsonResponse({'error': f'Error al eliminar el registro: {str(e)}'}, status=500)
        

#------ Holiday
class HolidayListView(ListView):
    model = Holiday
    template_name = 'holiday/list.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context

class GetHolidayListView(View):
    def get(self, request, *args, **kwargs):
        holidays = list(Holiday.objects.values('id', 'date'))

        return JsonResponse({'holidays': holidays}, safe=False)
    
class HolidayCreateView(CreateView):
    model = Holiday
    form_class = HolidayForm
    template_name = 'holiday/create.html'
    def get_success_url(self):
        return reverse('holiday-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        cleaned_data = form.cleaned_data

        # Imprime los datos en la consola del servidor
        print("Datos validados del formulario:", cleaned_data)
    
        data = {'message': 'Registro actualizado correctamente.'}
        return JsonResponse(data)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {'error': 'Error al actualizar el registro. Verifica los datos.'}
        return JsonResponse(data, status=400)

class HolidayUpdateView(UpdateView):
    model = Holiday
    form_class = HolidayForm
    template_name = 'holiday/update.html'
    success_url ="../list"

    def form_valid(self, form):
        response = super().form_valid(form)
        cleaned_data = form.cleaned_data

        # Imprime los datos en la consola del servidor
        print("Datos validados del formulario:", cleaned_data)
    
        data = {'message': 'Registro actualizado correctamente.'}
        return JsonResponse(data)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        data = {'error': 'Error al actualizar el registro. Verifica los datos.'}
        return JsonResponse(data, status=400)
class HolidayDeleteView(DeleteView):
    model = Holiday
    success_url ="../list"
    template_name = 'holiday/delete.html'
    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            return JsonResponse({'success': 'Registro eliminado exitosamente'})
        except Exception as e:
            return JsonResponse({'error': f'Error al eliminar el registro: {str(e)}'}, status=500)

#--- Reportes 
class CitationSearchFormView(FormView):
    template_name = 'reports/citation_search_form.html'
    form_class = CitationSearchForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        # Renderiza la misma página con el formulario
        return render(request, self.template_name, {'form': form})

class CitationListViewPdf(View):
     def get(self, request, *args, **kwargs):
        name = request.GET.get('name')
        process = request.GET.get('process')
        date = request.GET.get('date')
        # Construir un Q object para la consulta
        filter_conditions = Q()
        if name:
            filter_conditions &= Q(id_process__id_functionary__name__icontains=name)
        if process:
            filter_conditions &= Q(id_process=process)
        if date:
            # Convertir a objeto datetime
            date_datetime = datetime.strptime(date, "%d/%m/%Y")
            # Formatear la fecha en el formato deseado (YYYY-MM-DD)
            date_format = date_datetime.strftime("%Y-%m-%d")
            filter_conditions &= Q(date=date_format)

        citations = Citation.objects.filter(filter_conditions)
        for citation in citations:
            citation.time = convert_to_12_hour_format(citation.time)
        quantity = Citation.objects.count()
        data = {
            'citations': citations,
            'quantity': quantity
        }
        pdf = render_to_pdf('reports/citation_pdf.html', data)
        return HttpResponse(pdf, content_type="application/pdf")

#--- Otras Funciones
def convert_to_12_hour_format(hour24):
    # Formatear el objeto datetime.time en un formato de 12 horas con am/pm
    hour12 = hour24.strftime('%I:%M %p')
    return hour12


def send_email(mail, name, lastname, date, time, process, place, functionary, uuid, identification, typedoc):
    context = {'mail': mail, 'name': name, 'lastname': lastname, 'date': date, 'time':time, 
               'process':process,'place':place, 'functionary': functionary, 'uuid': uuid, 
               'identification': identification, 'typedoc': typedoc }
    print("context")
    print(context)
    template = get_template('email.html')
    content = template.render(context)

    email = EmailMultiAlternatives(
        'Correo de prueba',
        ' Angi Gomez',
        settings.EMAIL_HOST_USER,
        [mail]
    )

    email.attach_alternative(content, 'text/html')
    email.send()

# Formatear el objeto datetime.time en un formato de 12 horas con am/pm
def convert_to_12_hour_format2(hour24):  
    time_object = datetime.strptime(hour24, "%H:%M")
    time_format_12_hours = time_object.strftime("%I:%M %p")

    return time_format_12_hours