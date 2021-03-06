import json
from pprint import pprint

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.db.models import Q
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_headers
from django.views.decorators.http import condition

from .forms import *
from .forms import CreateTagForm, ExerciseForm
from .models import *
from .utils import *


alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}


def slugify_rus(s):
    """
    Overriding django slugify that allows to use russian words as well.
    """
    return slugify(''.join(alphabet.get(w, w) for w in s.lower()))


@ method_decorator(vary_on_headers('Cookie'), name='dispatch')
@ method_decorator(cache_page(60 * 15), name='dispatch')
# @ method_decorator(condition(etag_func=lambda _: 'v1'), name='dispatch')
class ShowExercises(DataMixin, ListView):
    model = Exercise
    template_name = 'python_exercise/index.html'
    context_object_name = 'exercises'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_category_slug = self.kwargs.get('category_slug')

        current_tag_slug = self.kwargs.get('tag_slug')

        if current_category_slug:
            context['current_category'] = Category.objects.get(
                slug=current_category_slug)
            context['title'] = context['current_category'].name
        else:
            context['title'] = 'Все категории'

        if current_tag_slug:
            context['current_tag'] = Tag.objects.get(
                slug=current_tag_slug)
            context['title'] += ' #' + context['current_tag'].name

        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()

        return context

    def get_queryset(self):
        current_category_slug = self.kwargs.get('category_slug')

        current_tag_slug = self.kwargs.get('tag_slug')

        exercises = []

        if current_category_slug and current_tag_slug:
            db_query = {
                'category__slug': current_category_slug,
                'tag__slug': current_tag_slug
            }
        elif current_category_slug:
            db_query = {
                'category__slug': current_category_slug,
            }
        elif current_tag_slug:
            db_query = {
                'tag__slug': current_tag_slug
            }
        else:
            db_query = {}

        exercises = (Exercise.objects
                     .filter(**db_query)
                     .select_related('category', 'author_create', 'author_update')
                     .prefetch_related('tag'))
        return exercises


class ShowUserExercises(LoginRequiredMixin, ShowExercises):
    slug_url_kwarg = 'username'
    template_name = 'python_exercise/user-exercises.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.user.username
        first_name = self.request.user.first_name
        last_name = self.request.user.last_name
        if first_name:
            context['title'] = f'Задачи от {first_name} {last_name} ({username})'
        else:
            context['title'] = f'Задачи от {username}'

        return context

    def get_queryset(self):
        query_author_create = Q(author_create=self.request.user)
        query_author_update = Q(author_update=self.request.user)

        exercises = (Exercise.objects
                     .filter(query_author_create | query_author_update)
                     .select_related('category', 'author_create', 'author_update')
                     .prefetch_related('tag'))
        return exercises


class ShowUserExercisesCreate(ShowUserExercises):
    def get_queryset(self):
        query_author_create = Q(author_create=self.request.user)

        exercises = (Exercise.objects
                     .filter(query_author_create)
                     .select_related('category', 'author_create', 'author_update')
                     .prefetch_related('tag'))
        return exercises


class ShowUserExercisesUpdate(ShowUserExercises):
    def get_queryset(self):
        query_author_update = Q(author_update=self.request.user)

        exercises = (Exercise.objects
                     .filter(query_author_update)
                     .select_related('category', 'author_create', 'author_update')
                     .prefetch_related('tag'))
        return exercises


class ShowTag(Index):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория'
        return context

    def get_queryset(self):
        return Tag.objects.get(slug=self.kwargs['tag_slug']).exercise_set.all()


class CreateExercise(LoginRequiredMixin, DataMixin, CreateView):
    form_class = ExerciseForm
    template_name = 'python_exercise/create-update-exercise.html'
    login_url = reverse_lazy('custom_auth:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление задачи'
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()

        context['submit_name'] = 'Создать'

        return context

    def form_valid(self, form):
        form.instance.author_create = self.request.user
        form.instance.author_update = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('python_exercise:exercise', args=(self.object.id,))


@require_POST
def create_tag(request):
    # if request.method != 'POST':
    #     return redirect('python_exercise:home', permanent=True)

    if not request.user.is_authenticated:
        return redirect('custom_auth:login', permanent=True)

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    data = body
    data['slug'] = slugify_rus(data['name'])
    form = CreateTagForm(data)
    if form.is_valid():
        try:
            Tag.objects.create(**form.cleaned_data)
            tags = Tag.objects.all()
            tags_json = serialize('json', tags)
            response = {
                'error': 'Null',
                'tags': tags_json
            }
        except:
            error = f"Тег с таким именем({form.cleaned_data['tag_name']}) уже существует"
            response = {
                'error': error,
                'tags': 'Null'
            }
    else:
        error = form.errors
        response = {
            'error': error,
            'tags': 'Null'
        }

    return JsonResponse(response)


class UpdateExercise(LoginRequiredMixin, DataMixin, UpdateView):
    model = Exercise
    form_class = ExerciseForm
    template_name = 'python_exercise/create-update-exercise.html'
    pk_url_kwarg = 'exercise_id'
    login_url = reverse_lazy('custom_auth:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование задачи'
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()

        context['cur_url_name'] = f"{context['cur_url_name']}/{self.kwargs['exercise_id']}"
        context['submit_name'] = 'Сохранить'
        return context

    def form_valid(self, form):
        form.instance.author_update = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('python_exercise:exercise', args=(self.object.id,))


class ShowComments(DataMixin, DetailView):
    model = Exercise
    template_name = 'python_exercise/exercise-discussion.html'
    pk_url_kwarg = 'exercise_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exercise'] = get_object_or_404(
            Exercise.objects.select_related('author_create', 'author_update'),
            id=self.kwargs['exercise_id'])

        context['title'] = context['exercise'].title
        return context


def page_not_found(request, exception):
    return HttpResponse('<h1> Страница не найдена </h1>')


def set_timezone(request):

    if request.method != 'POST':
        print('<' + request.POST['next'] + '>')
        return redirect(request.POST['next'], permanent=True)

    if request.method == 'POST':
        print(request.POST['timezone'])
        request.session['django_timezone'] = request.POST['timezone']
        return redirect(request.POST['next'], permanent=True)
