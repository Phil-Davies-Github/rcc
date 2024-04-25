from typing import Any
from django.forms.forms import BaseForm
from django.shortcuts import render
from django.views.generic import FormView, ListView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from intermediate.models import Intermediate, Object1, ItemModel
from .forms import IntermediateModelForm, IntermediateFormSet, ItemModelForm
from django.forms import modelformset_factory, formset_factory
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.shortcuts import redirect

# Test Object View
class DeleteItem(FormView):
    pass

class ItemUpdateView(FormView):
    # specify what needs to be used
    template_name = 'formset_view.html'
    # Each form is associate with an instance of the ItemModel
    # Only modelformsets have a save method so create a modelformset
    form_class = modelformset_factory(
        ItemModel,
        form = ItemModelForm,
        extra = 2
    )
    success_url = 'success'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        queryset = ItemModel.objects.all() 
        context['item_formset'] = self.form_class(queryset=queryset)
        return context
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        formset = self.form_class(request.POST, request.FILES)
        print(formset)
        if formset.is_valid():
            # add the additional fields to the database by adding to the corresponding model instance
            for form in formset:
                # get the instance to update from the model
                instance = form.instance
                if instance.pk: # if instance has a primary key
                    instance.elapsed_time_seconds = form.cleaned_data['elapsed_time_seconds'] 
                    instance.elapsed_time_minutes = form.cleaned_data['elapsed_time_minutes'] 
                    instance.save()
                
            messages.success(request, "Item Saved to database")
            # This creates a new formset instance with only the saved instances
            # formset = self.form_class(queryset=ItemModel.objects.filter(id__in=[instance.id for instance in instances]))
            # To obtain all instances of the item object, fetch the data from the database        
            all_instances = ItemModel.objects.all()
            formset_data = []
            formset = self.form_class(queryset=all_instances)
            
            # Reconstruct the formset with the elapsed time input data
            formset = self.form_class(initial=[{'elapsed_time': instance.elapsed_time} for instance in all_instances])
            
            # Redirect user to url after save
            return render(request, self.template_name, {'item_formset': formset})
        else: 
            return self.render_to_response({'item_formset': formset})


    def form_valid(self, form):
        
        return super().form_valid(form)
    
    # Rerender the form with error
    def form_invalid(self, form) -> HttpResponse:
        return self.render_to_response(self.get_context_data(form=form))  

# Create your views here.
class Index(TemplateView):
    template_name='index.html'

class IntermediateListView(ListView):
    model=Intermediate
    template_name='intermediate_list.html'

    # Override the get_context_data so that relevant data can be retrieved from then database

    def get_context_data(self, **kwargs):
        related_object2_instances = []
        seen_ids = set()

        context = super().get_context_data(**kwargs)
       
        # Retrieve only unique items in queryset and pass to the context
        unique_object2 = Intermediate.objects.values('object2_id').distinct()
        context['distinct_object2_instances'] = unique_object2
        
        # Only append the distinct instance of related_object2
        # by iterating through the Intermediate Object looking for the first instance of each distinct object2 
        for intermediate_obj in Intermediate.objects.all():
            object2_id = intermediate_obj.object2_id
            if object2_id not in seen_ids:
                seen_ids.add(object2_id)
                # Add to query
                related_object2_instances.append(intermediate_obj.object2)
        # Pass related Object2 instances to context
        context['related_object2_instances'] = related_object2_instances
        return context

class IntermediateUpdateView(FormView):
    model = Intermediate
    form_class = IntermediateModelForm
    template_name='update_intermediate_form.html'
    success_url='/success/'

    # The view needs to render the intermediate field together with the related object1 name
    # The following get_context override retrieves the querysets for both the intermediate instances 
    # and the object1
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Extract the value of object2_id from the URL parameters
        object2_id = self.kwargs.get('object2_id')  
        # Extract multiple instances filtered by the value of object 2 
        intermediate_queryset = Intermediate.objects.filter(object2_id=object2_id)
        # Get related object1 data
        related_object1_instances = Object1.objects.filter(id__in=intermediate_queryset.values('object1_id'))
        formset = IntermediateFormSet(queryset=intermediate_queryset)
        # populate related object1 data in each form instance
        # define the form
        '''
        form = formset.empty_form
        # iterates over pairs of elements from two iterables (formset and related_object1_instances) simultaneously
        
        for form, related_object1_instance in zip(formset, related_object1_instances):
            form.fields['object1_name'].initial = related_object1_instance.name if related_object1_instance else ""
        '''
        context['formset'] = formset
        #context['related_object1_instances'] = related_object1_instances
        return context
        
    # Called when form is submitted and passes validation
    def form_valid(self, form):
        form.save()
        # Redirect or show success message
        return super().form_valid(form)
    '''
    def post(self, request, *args, **kwargs):
        # get object we want to work with
        self.object = self.get_object(queryset=Intermediate.objects.all)
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return IntermediateFormSet(**self.get_form_kwargs(), instance=self.object)
    '''
   
    
    # Get keyword arguments that will be passed to the form class



    '''
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['object2_id'] = self.kwargs['object2_id']
        return kwargs

    # Called when form is submitted and passes validation
    def form_valid(self, form):
        form.save()
        # Redirect or show success message
        return super().form_valid(form)
    '''

# Function Based Views
def submit_view(request):
    initial_form_data = {
        'name': 'Rock',
        'estimated_price': 0,
    }
    if request.method=="GET":
        item_form = ItemModelForm(initial=initial_form_data)
    elif request.method=="POST":
        item_form = ItemModelForm(data=request.POST,
                                     initial=initial_form_data)
        if item_form.is_valid() and item_form.has_changed():
            name = item_form.cleaned_data['name']
            estimated_price = item_form.cleaned_data['estimated_price']
            message = f'Thanks for your submission of {name}, \
                        with an estimated price of {estimated_price}!'
            return HttpResponse(message)

    context = {
        'item_form': item_form
    }
    return render(request, 'submit.html', context)

def formset_submit_view(request):
    ItemFormSet = formset_factory(ItemModelForm, extra=2)
    item_formset = ItemFormSet()
    context = {
        'item_formset': item_formset
    }
    return render(request, 'formset_view.html', context)