#single signal for both User and Profile
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import User, Profile
#Single signal for both User and Profile
def createProfile(sender, instance, created, **kwargs):
    print('Signal Triggered')
    if created:
        Profile.objects.create(
            user=instance,
            username=instance.username,
            name=instance.first_name,
        )

#update user and profile signal
def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    
    if created == False:
        user.username = profile.username
        user.first_name = profile.name
        user.save(update_fields=['username', 'first_name'])
        # profile.save()  # remove this line

def deleteUser(sender, instance, **kwargs):
    instance.user.delete()

post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)