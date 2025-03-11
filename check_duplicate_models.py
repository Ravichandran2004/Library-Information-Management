import os
import django
import inspect
from django.db import models  # ✅ Import Django's base model class

# ✅ Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Library-Information-Management.settings")
django.setup()  # Initialize Django apps

# ✅ Now, import models safely
import lims_app.models as lims_models
import api.models as api_models

def get_model_fields(model):
    """Returns a set of field names for a given model class"""
    return {field.name for field in model._meta.fields}

# ✅ Get only Django model classes from lims_app
lims_model_names = {name for name, obj in inspect.getmembers(lims_models, inspect.isclass) if issubclass(obj, models.Model)}

# ✅ Get only Django model classes from api
api_model_names = {name for name, obj in inspect.getmembers(api_models, inspect.isclass) if issubclass(obj, models.Model)}

# ✅ Find duplicate model names
duplicate_model_names = lims_model_names.intersection(api_model_names)

if duplicate_model_names:
    print(f"🚨 Duplicate Models Found: {duplicate_model_names}")

    # ✅ Check if the fields of the duplicate models are also the same
    for model_name in duplicate_model_names:
        lims_model = getattr(lims_models, model_name)
        api_model = getattr(api_models, model_name)

        lims_fields = get_model_fields(lims_model)
        api_fields = get_model_fields(api_model)

        if lims_fields == api_fields:
            print(f"✅ {model_name} is fully duplicated in both apps.")
        else:
            print(f"⚠️ {model_name} exists in both apps but has different fields!")
else:
    print("✅ No Duplicate Models Found!")
