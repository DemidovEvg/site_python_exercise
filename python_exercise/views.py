import json
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .forms import ExerciseForm, CreateTagForm
from .models import *
from .utils import *
from .forms import *
from pprint import pprint
from django.template.defaultfilters import slugify
from django.core.serializers import serialize
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}


def slugify_rus(s):
    """
    Overriding django slugify that allows to use russian words as well.
    """
    return slugify(''.join(alphabet.get(w, w) for w in s.lower()))


class ShowExercises(DataMixin, ListView):
    model = Exercise
    template_name = 'index.html'
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

        exercises = Exercise.objects.filter(**db_query)

        return exercises


class ShowUserExercises(ShowExercises):
    slug_url_kwarg = 'user_slug'
    template_name = 'user-exercises.html'

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

        exercises = Exercise.objects.filter(
            query_author_create | query_author_update)
        return exercises


class ShowUserExercisesCreate(ShowUserExercises):
    def get_queryset(self):
        query_author_create = Q(author_create=self.request.user)

        exercises = Exercise.objects.filter(
            query_author_create)
        return exercises


class ShowUserExercisesUpdate(ShowUserExercises):
    def get_queryset(self):
        query_author_update = Q(author_update=self.request.user)

        exercises = Exercise.objects.filter(
            query_author_update)
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
    template_name = 'create-update-exercise.html'
    login_url = reverse_lazy('custom_auth:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление задачи'
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()

        context['submit_name'] = 'Создать'

        return context

    def form_valid(self, form):
        return super().form_valid(form)

    def form_valid(self, form):
        form.instance.author_create = self.request.user
        form.instance.author_update = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        print(self.request.POST)
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('python_exercise:exercise', args=(self.object.id,))


def create_tag(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if request.method == 'POST':
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
    template_name = 'create-update-exercise.html'
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
    template_name = 'exercise-discussion.html'
    pk_url_kwarg = 'exercise_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exercise'] = (Exercise.objects
                               .select_related('author_create', 'author_update')
                               .get(id=self.kwargs['exercise_id']))

        context['title'] = context['exercise'].title
        return context


def page_not_found(request, exception):
    return HttpResponse('<h1> Страница не найдена </h1>')
