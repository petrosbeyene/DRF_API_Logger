from functools import wraps
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from requestLogger.models import ModelChangeLog
from datetime import datetime
import json


## Python Decorator to Prevent infinite recursion of post_save signal
def prevent_recursion(func):
    # @wraps(func)
    def no_recursion(sender, **kwargs):
        instance = kwargs['instance']
        if not instance:
            return
        if hasattr(instance, '_dirty'):
            return
        try:
            instance._dirty = True
            func(sender, **kwargs)
            instance.save()
        finally:
            del instance._dirty
    return no_recursion



@receiver(pre_save)
def logModelChanges(sender, **kwargs):
    try:
        instance = kwargs['instance']
        if instance.pk:
            old_instance = sender.objects.get(pk=instance.pk)
            changes = {}
            for field in instance._meta.fields:
                if getattr(old_instance, field.name) != getattr(instance, field.name):
                    if isinstance(getattr(instance, field.name), datetime):
                        changes[field.name] = {
                            'old': getattr(old_instance, field.name).strftime('%Y-%m-%d %H:%M:%S'),
                            'new': getattr(instance, field.name).strftime('%Y-%m-%d %H:%M:%S')
                        }
                    else:
                        changes[field.name] = {'old': getattr(old_instance, field.name), 'new': getattr(instance, field.name)}

            if changes:
                log_data = {
                    'model_name': sender.__name__,
                    'action_type': 'update' if old_instance else 'create',
                    'instance_pk': instance.pk,
                    'changes': json.dumps(changes)
                }
                model_change_log = ModelChangeLog(**log_data)
                model_change_log.save()
        
    except ObjectDoesNotExist:
        pass


# @receiver(post_save)
# @prevent_recursion
# def logModelCreation(sender, **kwargs):
#     try:
#         instance = kwargs['instance']
#         if kwargs['created']:
#         # This means that a new instance of the model was created
#             changes = {}
#             for field in instance._meta.fields:
#                 if isinstance(getattr(instance, field.name), datetime):
#                     changes[field.name] = {
#                         'old': None,
#                         'new': getattr(instance, field.name).strftime('%Y-%m-%d %H:%M:%S')
#                     }
#                 else:
#                     changes[field.name] = {'old': None, 'new': getattr(instance, field.name)}
#             log_data = {
#                 'model_name': sender.__name__,
#                 'action_type': 'create',
#                 'instance_pk': instance.pk,
#                 'changes': changes
#             }
#             model_change_log = ModelChangeLog(**log_data)
#             model_change_log.save()
#     except ObjectDoesNotExist:
#         pass

@receiver(pre_delete)
def logModelDeletion(sender, **kwargs):
    try:
        instance = kwargs['instance']
        log_data = {
            'model_name': sender.__name__,
            'action_type': 'delete',
            'instance_pk': instance.pk,
            'changes': '{}'
        }
        model_change_log = ModelChangeLog(**log_data)
        model_change_log.save()
        
    except ObjectDoesNotExist:
        pass