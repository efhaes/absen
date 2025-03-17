from django.apps import AppConfig

class BirruwattaqwaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'birruwattaqwa'
    
    def ready(self):
        import birruwattaqwa.signals  # Impor signals di dalam ready()

 
