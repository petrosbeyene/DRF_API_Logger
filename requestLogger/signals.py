from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from .models import ModelChangeLog
from datetime import datetime

@receiver(pre_save)
def logModelChanges(sender, **kwargs):
    try:
        instance = kwargs['instance']
        old_instance = sender.objects.get(pk=instance.pk)
        changes = {}
        if old_instance:
            for field in instance._meta.fields:
                if getattr(old_instance, field.name) != getattr(instance, field.name):
                    if isinstance(getattr(instance, field.name), datetime):
                        changes[field.name] = {
                            'old': getattr(old_instance, field.name).strftime('%Y-%m-%d %H:%M:%S'),
                            'new': getattr(instance, field.name).strftime('%Y-%m-%d %H:%M:%S')
                        }
                    else:
                        changes[field.name] = {'old': getattr(old_instance, field.name), 'new': getattr(instance, field.name)}
        # else:
        #     for field in instance._meta.fields:
        #         if isinstance(getattr(instance, field.name), datetime):
        #             changes[field.name] = {
        #                 'old': None,
        #                 'new': getattr(instance, field.name).strftime('%Y-%m-%d %H:%M:%S')
        #             }
        #         else:
        #             changes[field.name] = {'old': None, 'new': getattr(instance, field.name)}
        if changes:
            log_data = {
                # 'user_id': instance.user_id, # or any other user identifier you want to associate with the change
                'model_name': sender.__name__,
                'action_type': 'update' if old_instance else 'create',
                'instance_pk': instance.pk,
                'changes': changes
            }
            model_change_log = ModelChangeLog(**log_data)
            model_change_log.save()
    except ObjectDoesNotExist:
        pass