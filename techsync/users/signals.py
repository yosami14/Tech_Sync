def deleteUser(sender, instance, **kwargs):
    if instance.user_id is not None:
        instance.user.delete()#single signal for both User and Profile
        
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import User, Profile, EventOrganizer
from django.core.mail import send_mail
from django.conf import settings

#Single signal for both User and Profile
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_event_organizer:
            EventOrganizer.objects.create(
                user=instance,
                username=instance.username,
                name=instance.first_name,
            )
        else:
            Profile.objects.create(
                user=instance,
                username=instance.username,
                name=instance.first_name,
            )

        subject = f'Welcome to TechSync, {instance.first_name}!'
        message = (
            f'Dear {instance.first_name},\n\n'
            'Welcome to TechSync!\n\n'
            'We are thrilled to have you join our community. TechSync is a platform designed to help you share your experiences, '
            'collaborate on projects, and grow your career. We believe that with your unique skills and insights, our community '
            'will be even stronger.\n\n'
            'If you have any questions or need assistance, please don’t hesitate to reach out to us at support@techsync.com. '
            'We are here to help.\n\n'
            'Best regards,\n'
            'The TechSync Team'
        )

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [instance.email],
            fail_silently=False,
        )

@receiver(post_save, sender=Profile)
def update_user(sender, instance, created, **kwargs):
    user = instance.user
    if not created:
        user.username = instance.username
        user.first_name = instance.name
        user.save(update_fields=['username', 'first_name'])

@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    try:
        instance.user.delete()
    except User.DoesNotExist:
        pass

@receiver(post_save, sender=EventOrganizer)
def update_user_event_organizer(sender, instance, created, **kwargs):
    user = instance.user
    if not created:
        user.username = instance.username
        user.first_name = instance.name
        user.save(update_fields=['username', 'first_name'])

@receiver(post_delete, sender=EventOrganizer)
def delete_user_event_organizer(sender, instance, **kwargs):
    try:
        instance.user.delete()
    except User.DoesNotExist:
        pass

