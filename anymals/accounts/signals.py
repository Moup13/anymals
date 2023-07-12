from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def send_verify_email(instance, created, **kwargs):
    if not created or instance.is_active:
        return
    domain = settings.ALLOWED_HOSTS[0] or 'http://localhost:8000'
    token = generate_token(instance.id)
    message = render_to_string(
        "verify_email.html",
        context={"token": token, "base_url": domain},
    )
    send_mail(
        "Verify Email Subject",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[instance.email],
    )