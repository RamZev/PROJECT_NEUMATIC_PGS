# neumatic\apps\menu\views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import MenuHeading, MenuItem
from .forms import MenuHeadingForm, MenuItemForm

class MenuHeadingListView(LoginRequiredMixin, ListView):
    model = MenuHeading
    template_name = 'menu/menuheading_list.html'
    context_object_name = 'headings'
    paginate_by = 20

class MenuHeadingCreateView(LoginRequiredMixin, CreateView):
    model = MenuHeading
    form_class = MenuHeadingForm
    template_name = 'menu/menuheading_form.html'
    success_url = reverse_lazy('menu:heading_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Encabezado de Menú'
        return context

class MenuHeadingUpdateView(LoginRequiredMixin, UpdateView):
    model = MenuHeading
    form_class = MenuHeadingForm
    template_name = 'menu/menuheading_form.html'
    success_url = reverse_lazy('menu:heading_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Encabezado de Menú'
        return context

class MenuHeadingDeleteView(LoginRequiredMixin, DeleteView):
    model = MenuHeading
    template_name = 'menu/menuheading_confirm_delete.html'
    success_url = reverse_lazy('menu:heading_list')

class MenuItemListView(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = 'menu/menuitem_list.html'
    context_object_name = 'items'
    paginate_by = None  # Show all items without pagination
    
    def get_queryset(self):
        return MenuItem.objects.select_related('heading', 'parent').prefetch_related('groups')

class MenuItemCreateView(LoginRequiredMixin, CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'menu/menuitem_form.html'
    success_url = reverse_lazy('menu:item_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Item de Menú'
        return context

class MenuItemUpdateView(LoginRequiredMixin, UpdateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'menu/menuitem_form.html'
    success_url = reverse_lazy('menu:item_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Item de Menú'
        return context

class MenuItemDeleteView(LoginRequiredMixin, DeleteView):
    model = MenuItem
    template_name = 'menu/menuitem_confirm_delete.html'
    success_url = reverse_lazy('menu:item_list')

class MenuTreeView(LoginRequiredMixin, TemplateView):
    template_name = 'menu/menu_tree.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        headings = MenuHeading.objects.prefetch_related(
            'menuitem_set__children__children'
        ).all()
        context['headings'] = headings
        return context