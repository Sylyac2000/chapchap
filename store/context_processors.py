""" Send some datas in sidebar, and directly on templates(layout...)"""


from frontend.models import Utilisateur
from store.models import Store


def add_datas_to_context(request):

    if request.user.is_authenticated and not request.user.is_admin:
        utilisateur = Utilisateur.objects.get(email=request.user.email)
        thestores = Store.objects.filter(proprietary=utilisateur)
        nbre = len(thestores)

    else:
        nbre = -1

    return {
        'has_stores': True if nbre > 0 else False
        #'objparametre': "Salam"
    }