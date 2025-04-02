from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import *
from .serializers import *
from .permissions import *



class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MyAccountView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsInstructor]


class CourseListView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsInstructor()]
        return super().get_permissions()


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsOwnerOrInstructor]


class LessonListCreateView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Lesson.objects.filter(course_id=course_id)

    def perform_create(self, serializer):
        course = Course.objects.get(id=self.kwargs['course_id'])
        serializer.save(course=course)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsInstructor()]
        return super().get_permissions()


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrInstructor]


class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Review.objects.filter(course_id=course_id)


class PaymentCreateView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        payment.status = "completed"  # Toʻlov statusini avtomatik "completed" qilish
        payment.save()


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)


class EnrollInCourseView(generics.CreateAPIView):
    serializer_class = CourseEnrollSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        course = Course.objects.get(id=serializer.validated_data['course_id'])

        # Toʻlovni tekshirish
        if not Payment.objects.filter(user=user, course=course, status="completed").exists():
            return Response({"error": "You must purchase the course first."}, status=400)

        # Talabani qo‘shish (ManyToManyField uchun)
        student, created = Student.objects.get_or_create(user=user)
        student.course.add(course)

        # ✅ Foydalanuvchi ma'lumotlarini qaytarish
        return Response({
            "course_id": course.id,
            "course_title": course.title,
            "user": {
                "id": user.id,
                "username": user.username,
                "full_name": f"{user.first_name} {user.last_name}",
                "email": user.email,
                "is_instructor": user.is_instructor
            }
        }, status=201)


class CourseStudentsListView(generics.ListAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsInstructor]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Student.objects.filter(course__id=course_id)
