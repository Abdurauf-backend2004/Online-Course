from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg import openapi
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh
from rest_framework import permissions
from drf_yasg.views import get_schema_view

from main.views import *

schema_view = get_schema_view(
    openapi.Info(
        title="Online Course API",
        default_version='v1',
        description="",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns += [
    path('token/', token_obtain_pair),
    path('token/refresh/', token_refresh),
]

urlpatterns += [
    path('api/register/',UserRegisterView.as_view(), name='register'),
    path('api/users/my-account/', MyAccountView.as_view(), name='my-account'),
    path('api/users/', UserListView.as_view(), name='user-list'),

    path('api/courses/', CourseListView.as_view(), name='course-list'),
    path('api/courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),

    path('api/courses/<int:course_id>/lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('api/lessons/<int:pk>/',LessonDetailView.as_view(), name='lesson-detail'),

    path('api/courses/<int:course_id>/reviews/', ReviewListView.as_view(), name='review-list'),
    path('api/courses/<int:course_id>/reviews/create/', ReviewCreateView.as_view(), name='review-create'),

    path('api/courses/<int:course_id>/pay/', PaymentCreateView.as_view(), name='payment-create'),
    path('api/payments/', PaymentListView.as_view(), name='payment-list'),

    path('api/courses/<int:course_id>/enroll/', EnrollInCourseView.as_view(), name='enroll-course'),

    path('api/courses/<int:course_id>/students/', CourseStudentsListView.as_view(), name='course-students'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)