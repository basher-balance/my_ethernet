from django.conf import settings
import django.apps

def model_paths(request):
    model_paths = []
    models = django.apps.apps.get_models()[:-7]

    for model in models:
        path = str(model._meta).split(".")
        model_paths.append("/".join(path))

    return {"model_paths": model_paths}
