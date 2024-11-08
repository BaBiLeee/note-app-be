# note/urls.py
from django.urls import path
from .views import view_note

# router = DefaultRouter()
# router.register(r'notes', NoteViewSet)

# router.register(r'types', TypeViewSet)
# router.register(r'groups', GroupViewSet)
# router.register(r'users', UserViewSet)


urlpatterns = [
    # path('', include(router.urls)), 
    # path('notes/', view_note, name='note')
    path('note/', view_note, name='note'),
]
