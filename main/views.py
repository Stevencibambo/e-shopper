from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import (FormView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import (LoginRequiredMixin, UserPassesTestMixin)
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms as django_forms
from django.db import models as django_models
from django_filters.views import FilterView
from django.core.paginator import Paginator
import django_filters
from main import forms
from main import models
import logging


def home(request):
    template_name = "home.html"
    tags = models.ProductTag.objects.all()
    products = models.Product.objects.all().order_by('-date_updated')[:6]
    for product in products:
        image = product.productimage_set.all()[:1]
        if image:
            product.image = image[0].thumbnail.url
    return render(request, template_name, {'tags': tags, 'items': products})


class ContactUsView(FormView):
    template_name = "contact_form.html"
    form_class = forms.ContactForm
    success_url = "/"

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)


class ProductTagsListView(ListView):
    template_name = "main/product_tags.html"
    paginate_by = 5

    def get_queryset(self):
        tags = models.ProductTag.objects.active()

        return tags.order_by()


class ProductListView(ListView):
    template_name = "main/product_list.html"
    paginate_by = 4

    def get_queryset(self):
        tag = self.kwargs['subtag']
        self.tag = None
        if tag != 'all':
            self.tag = get_object_or_404(
                models.ProductSubTag, slug=tag
            )
        if self.tag:
            products = models.Product.objects.active().filter(
                tags=self.tag
            )
        else:
            products = models.Product.objects.active()

        return products.order_by()


logger = logging.getLogger(__name__)


class SignupView(FormView):
    template_name = "signup.html"
    form_class = forms.UserCreationForm

    def get_success_url(self):
        redirect_to = self.request.GET.get("next", "/")
        return redirect_to

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()
        email = form.cleaned_data.get("email")
        raw_password = form.cleaned_data.get("password1")
        logger.info("New signup for email=%s through SignupView", email)
        user = authenticate(email=email, password=raw_password)
        login(self.request, user)
        form.send_mail()
        messages.info(self.request, "You signed up successfully")

        return response


class AddressListView(LoginRequiredMixin, ListView):
    model = models.Address

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = models.Address
    fields = [
        "name",
        "address1",
        "address2",
        "zip_code",
        "city",
        "country"
    ]
    success_url = reverse_lazy("address_list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Address
    fields = ["name", "address1", "address2", "zip_code", "city", "country"]
    success_url = reverse_lazy("address_list")

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    models = models.Address
    success_url = reverse_lazy("address_list")

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class AddressSelectionView(LoginRequiredMixin, FormView):
    template_name = "address_select.html"
    form_class = forms.AddressSelectionForm
    success_url = reverse_lazy('checkout_done')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        del self.request.session['basket_id']
        basket = self.request.basket
        basket.create_order(
            form.cleaned_data['billing_address'],
            form.cleaned_data['shipping_address']
        )
        return super().form_valid(form)


class DateInput(django_forms.DateInput):
    input_type = 'date'


class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = models.Order
        fields = {
            'user__email': ['icontains'],
            'status': ['exact'],
            'date_updated': ['gt', 'lt'],
            'date_added': ['gt', 'lt'],
        }
        filter_overrides = {
            django_models.DateTimeField: {
                'filter_class': django_filters.DateFilter,
                'extra': lambda f: {'widget': DateInput}
            }
        }


class OrderView(UserPassesTestMixin, FilterView):
    filterset_class = OrderFilter
    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.is_staff is True


def all_products(request):
    template_name = "main/product_tags.html"
    tags = models.ProductTag.objects.all()
    products = models.Product.objects.all()
    for product in products:
        image = product.productimage_set.all()[:1]
        if image:
            product.image = image[0].thumbnail.url

    products = Paginator(products, 10)
    page_number = request.GET.get('page')
    products = products.get_page(page_number)

    return render(request, template_name, {'tags': tags, 'products': products})


def tag_products(request, tag, subtag):
    template_name = "main/tag_products.html"
    tags = models.ProductTag.objects.active()
    p_tag = None
    if tag is not None and subtag is not None:
        p_tag = get_object_or_404(models.ProductSubTag, slug=subtag)
    else:
        return HttpResponseRedirect(reverse("products"))

    products = models.Product.objects.active().filter(tags=p_tag)
    for product in products:
        image = product.productimage_set.all()[:1]
        if image:
            product.image = image[0].thumbnail.url

    products = Paginator(products, 10)
    page_number = request.GET.get('page')
    products = products.get_page(page_number)

    return render(request, template_name, {'tags': tags, 'products': products})


def product_detail(request, slug):
    template_name = "main/product_detail.html"
    tags = models.ProductTag.objects.all()
    product = models.Product.objects.get(slug=slug)
    image = product.productimage_set.all()[:1]
    if image:
        product.image = image[0].thumbnail.url

    return render(request, template_name, {'product': product, 'tags': tags})


def add_to_basket(request):
    product = get_object_or_404(models.Product, pk=request.GET.get("product_id"))
    basket = request.basket
    if not request.basket:
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None
        basket = models.Basket.objects.create(user=user)
        request.session["basket_id"] = basket.id

    basketline, created = models.BasketLine.objects.get_or_create(basket=basket, product=product)
    if not created:
        basketline.quantity += 1
        basketline.save()

    return HttpResponseRedirect(reverse("product", args=(product.slug,)))


def manage_basket(request):
    if not request.basket:
        return render(request, "basket.html", {"formset": None})

    if request.method == "POST":
        formset = forms.BasketLineFormSet(request.POST, instance=request.basket)
        if formset.is_valid():
            formset.save()

    else:
        formset = forms.BasketLineFormSet(instance=request.basket)

    if request.basket.is_empty():
        return render(request, "basket.html", {"formset": None})

    return render(request, "basket.html", {"formset": formset})


def room(request, order_id):
    return render(
        request,
        "chat_room.html",
        {"room_name_json": str(order_id)}
    )
