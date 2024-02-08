from appointments.models import Citation, Person
from django.core.mail import send_mail
from datetime import datetime, timedelta

def enviar_correo_programado():
            # Lógica para enviar recordatorios de citas
            fecha_manana = datetime.now() + timedelta(days=1)
            fecha_anterior = fecha_manana - timedelta(days=1)
            citas_manana = Citation.objects.filter(date=fecha_manana)
            for cita in citas_manana:
               destinatario = cita.id_person.email
               asunto = 'Recordatorio Cita'
               cuerpo = f'Hola {cita.id_person.name}, recuerda tu cita mañana {cita.date.strftime("%d-%m-%Y")} a las {cita.time.strftime("%H:%M")}. ¡No la pierdas!'
               if(cita.date_creation != fecha_anterior.date()):
                  send_mail(asunto, cuerpo, 'pruebadjango023@gmail.com', [destinatario])
                  print('PAsa por aquí', timedelta(days=1), 'tomorrow', cita.date )