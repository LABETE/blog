from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import Http404
from django.utils import timezone
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from braces.views import LoginRequiredMixin

from .forms import PostForm
from .models import Post


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = PostForm
    template_name = "posts/post_form.html"
    success_message = "Your post was created successfully."

    def get_context_data(self, *args, **kwargs):
        context = super(PostCreateView, self).get_context_data(*args, **kwargs)
        if self.request.user.is_staff:
            return context
        raise Http404

    def post(self, *args, **kwargs):

        form = self.get_form()
        if form.is_valid():
            form.user = self.request.user
            return self.form_valid(form)


class PostUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"
    success_message = "Your post was updated successfully."

    def get_context_data(self, *args, **kwargs):
        context = super(PostCreateView, self).get_context_data(*args, **kwargs)
        if self.request.user.is_staff:
            return context
        raise Http404


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        if context["object"].draft or context["object"].publish > timezone.now().date():
            if self.request.user.is_staff:
                return context
        raise Http404


class PostListView(ListView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super(PostListView, self).get_context_data(*args, **kwargs)
        q = self.request.GET.get("q")
        qs = (
                    Q(title__icontains=q) |
                    Q(content__icontains=q) |
                    Q(user__first_name__icontains=q) |
                    Q(user__last_name__icontains=q)
                )
        if self.request.user.is_staff:
            if q:
                object_list = Post.objects.filter(qs).distinct()
            else:
                object_list = Post.objects.all()
        else:
            if q:
                object_list = Post.objects.active().filter(qs)
            else:
                object_list = Post.objects.active()

        paginator = Paginator(object_list, 2)  # Show 5 results per page

        page = self.request.GET.get('page')
        try:
            object_list = paginator.page(page)
            page_range = paginator.page_range
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            object_list = paginator.page(1)
            page_range = paginator.page_range
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of
            # results.
            object_list = paginator.page(paginator.num_pages)
            page_range = paginator.page_range

        context["object_list"] = object_list
        context["page_range"] = page_range
        return context


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("posts:list")
    success_message = "Your post was deleted successfully."

    def get_context_data(self, *args, **kwargs):
        context = super(PostCreateView, self).get_context_data(*args, **kwargs)
        if self.request.user.is_staff:
            return context
        raise Http404

    def delete(self, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PostDeleteView, self).delete(*args, **kwargs)
