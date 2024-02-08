from django.urls import path

from . import views

urlpatterns = [
    #path("", views.index, name="index"),
    #---- functionary
    path("functionary/list/", views.FunctionaryListView.as_view(), name="functionary-list"),
    path("functionary/add/", views.FunctionaryCreateView.as_view(), name="functionary-create"),
    path('functionary/detail/<int:pk>', views.FunctionaryDetail.as_view(), name='functionary-detail'),
    path("functionary/update/<int:pk>", views.FunctionaryUpdateView.as_view(), name="functionary-update"),
    path("functionary/delete/<str:pk>", views.FunctionaryDeleteView.as_view(), name="functionary-delete"),
    #---- person
    path("person/add/", views.PersonCreateView.as_view(), name="person-create"),
    path("person/search/", views.PersonSearchView.as_view(), name="person-search"),
    path('person/detail/<int:pk>', views.PersonDetail.as_view(), name='person-detail'),
    path("person/list/", views.PersonListView.as_view(), name="person-list"),
    path("person/update/<int:pk>", views.PersonUpdateView.as_view(), name="person-update"),
    path("person/delete/<str:pk>", views.PersonDeleteView.as_view(), name="person-delete"),
    #---- citation
    path("add/", views.CitationCreateView.as_view(), name="citation-create"),
    path("cancel-form/", views.CitationCancelFormView.as_view(), name="citation-cancel-form"),
    path("cancel/", views.CitationCancelView.as_view(), name="citation-cancel"),
    path("person-consult-form/", views.CitationPersonConsultFormView.as_view(), name="citation-person-consult-form"),
    path("person-consult/", views.CitationPersonConsult.as_view(), name="citation-person-consult"),
    path("close-process/", views.CloseProcess.as_view(), name="citation-close-process"),
    #---- department
    path("department/list/", views.DepartmentListView.as_view(), name="department-list"),
    path("department/add/", views.DepartmentCreateView.as_view(), name="department-create"),
    path("department/update/<int:pk>", views.DepartmentUpdateView.as_view(), name="department-update"),
    path("department/delete/<str:pk>", views.DepartmentDeleteView.as_view(), name="department-delete"),
    #---- city
    path("city/list/", views.CityListView.as_view(), name="city-list"),
    path("city/add/", views.CityCreateView.as_view(), name="city-create"),
    path("city/update/<int:pk>", views.CityUpdateView.as_view(), name="city-update"),
    path("city/delete/<str:pk>", views.CityDeleteView.as_view(), name="city-delete"),
    #---- document
    path("document_type/list/", views.DocumentTypeListView.as_view(), name="document-type-list"),
    path("document_type/add/", views.DocumentTypeCreateView.as_view(), name="document-type_create"),
    path("document_type/update/<str:pk>", views.DocumentTypeUpdateView.as_view(), name="document-type-update"),
    path("document_type/delete/<str:pk>", views.DocumentTypeDeleteView.as_view(), name="document-type-delete"),
    #---- person_type
    path("person_type/list/", views.PersonTypeListView.as_view(), name="person-type-list"),
    path("person_type/add/", views.PersonTypeCreateView.as_view(), name="person-type-create"),
    path("person_type/update/<str:pk>", views.PersonTypeUpdateView.as_view(), name="person-type-update"),
    path("person_type/delete/<str:pk>", views.PersonTypeDeleteView.as_view(), name="person-type-delete"),
    #---- place
    path("place/list/", views.PlaceListView.as_view(), name="place-list"),
    path("place/add/", views.PlaceCreateView.as_view(), name="place-create"),
    path("place/update/<str:pk>", views.PlaceUpdateView.as_view(), name="place-update"),
    path("place/delete/<str:pk>", views.PlaceDeleteView.as_view(), name="place-delete"),
    #---- process
    path("process/list/", views.ProcessListView.as_view(), name="process-list"),
    path("process/add/", views.ProcessCreateView.as_view(), name="process-create"),
    path('process/detail/<int:pk>', views.ProcessDetail.as_view(), name='process-detail'),
    path("process/update/<str:pk>", views.ProcessUpdateView.as_view(), name="process-update"),
    path("process/delete/<str:pk>", views.ProcessDeleteView.as_view(), name="process-delete"),
    #---- citation
    path("citation/list/", views.CitationListView.as_view(), name="citation-list"),
    path("citation/update/<int:pk>", views.CitationUpdateView.as_view(), name="citation-update"),
    path('citation/detail/<int:pk>', views.CitationDetail.as_view(), name='citation-detail'),
    path("citation/delete/<str:pk>", views.CitationDeleteView.as_view(), name="citation-delete"),
    #---- holiday
    path("holiday/list/", views.HolidayListView.as_view(), name="holiday-list"),
    path("holiday/add/", views.HolidayCreateView.as_view(), name="holiday-create"),
    path("holiday/update/<str:pk>", views.HolidayUpdateView.as_view(), name="holiday-update"),
    path("holiday/delete/<str:pk>", views.HolidayDeleteView.as_view(), name="holiday-delete"),
    path("holiday/get", views.GetHolidayListView.as_view(), name="holiday-get"),
    #----- constraint
    path("constraint/add/", views.ConstraintCreateView.as_view(), name="constraint-create"), 
    #----- Reports
    path("citation/search-form", views.CitationSearchFormView.as_view(), name="citation-search-form"),
    path("citation/list/pdf", views.CitationListViewPdf.as_view(), name="citation-list-pdf"),
]