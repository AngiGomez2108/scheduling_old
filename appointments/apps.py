from django.apps import AppConfig

class AppointmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointments'

    def ready(self):

        from apscheduler.schedulers.background import BackgroundScheduler
        from appointments.tasks import enviar_correo_programado

        # Configurar el planificador de tareas
        scheduler = BackgroundScheduler()
        # Configurar la tarea para que se ejecute cada día a las 8 AM
        print('hola mundo')
        scheduler.add_job(enviar_correo_programado, 'cron', hour=20, minute=17)
        scheduler.start()