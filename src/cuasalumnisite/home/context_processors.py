from cuasalumnisite.home.models import Setting
from django.utils.safestring import mark_safe

def settings(request):
    settings = {}
    for setting in Setting.objects.all():
        settings['gSetting_%s' % setting.name] = mark_safe(setting.value)
        
    return settings