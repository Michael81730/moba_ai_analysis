from django.apps import AppConfig


class MobaAiAnalysisConfig(AppConfig):
    # default_auto_field = 'django.db.models.BigAutoField'
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'
    name = 'moba_ai_analysis'
