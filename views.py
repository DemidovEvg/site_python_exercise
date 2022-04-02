from django.http import HttpResponse


def test_view(request):
    return HttpResponse('<h1>test_app2</h1>')
