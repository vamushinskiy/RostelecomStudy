from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import main.views as main_views
handler404 = main_views.custom_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('news/', include('news.urls')),
    path('users/', include('users.urls')),
    path('home/', include('home.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# добавляем строку для работы медиафайлов
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# для работы debug_toolbars
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug/__', include(debug_toolbar.urls)),
        ] + urlpatterns

admin.site.site_header = "Новости погоды"
admin.site.index_title = "Панель администрирования сайта Новости погоды"