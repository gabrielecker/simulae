from rest.views import AnswerViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'answers', AnswerViewSet)
