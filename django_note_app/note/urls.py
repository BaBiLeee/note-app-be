# note/urls.py
from django.urls import path
from .views import change_permission, delete_note, get_note_by_id, get_share_note, get_shared_note, manage_share, share_note, update_note, view_note

# router = DefaultRouter()
# router.register(r'notes', NoteViewSet)

# router.register(r'types', TypeViewSet)
# router.register(r'groups', GroupViewSet)
# router.register(r'users', UserViewSet)


urlpatterns = [
    # path('', include(router.urls)), 
    # path('notes/', view_note, name='note')
    path('note/', view_note, name='note'),
    path('note/<int:note_id>/', get_note_by_id, name='note'),
    path('share-note/<int:note_id>/', share_note, name='note'),
    path('get-shared-note/', get_shared_note, name='note'),
    path('get-share-note/', get_share_note, name='note'),
    path('manage-share/<int:user_id>/', manage_share, name='note'),
    path('update-note/<int:note_id>/', update_note, name='note'),
    path('delete-note/<int:note_id>/', delete_note, name='note'),
    path('change-permission/', change_permission, name='note'),
]
