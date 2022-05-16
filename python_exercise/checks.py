from django.core.checks import Error, register


@register()
def example_check(app_configs, **kwargs):
    errors = []
    # ... your check logic here
    # if True:
    # errors.append(
    #     Error(
    #         'an error',
    #         hint='A hint.',
    #         obj=[1,2,3],
    #         id='myapp.E001',
    #     )
    # )
    return errors
