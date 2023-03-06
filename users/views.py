# users/views.py
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from dicoms.models import DicomFile, Comment, DicomFile_User
from django.views.generic import DetailView , ListView
from django.db.models import Q

from users.filters import UserListFilter
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


@login_required
def dashboard_view(request):

    latest_dicoms = DicomFile_User.objects.filter(user=request.user.pk).order_by('-added_time')[:5]
    latest_comments = Comment.objects.filter(Q(dicom_file__access=request.user.pk) | Q(dicom_file__owner=request.user.pk)).order_by('-comment_time').distinct()[:5]

    context = {
        'latest_dicoms':latest_dicoms,
        'latest_comments':latest_comments,
    }

    return render(request,'users/dashboard.html', context=context)
    

def home_page_view(request):
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    else:
        return redirect('login')


def about_us_page_view(request):
    return render(request,'users/about_us.html')



def contact_us_page_view(request):
    return render(request,'users/contact_us.html')



class UserDetailView(LoginRequiredMixin, DetailView):
    model = User


class UserListView(LoginRequiredMixin, ListView):
    model = User 
    context_object_name = 'users_list'
    paginate_by = 25
    filterset_class = UserListFilter
    
    def get_queryset(self):
        order = self.request.GET.get('order')
        if order is None:
            order = 'first_name'
        queryset = User.objects.order_by(order)
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context



