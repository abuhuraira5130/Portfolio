from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ProductViewSet, CollectionViewSet, CustomerViewSet, OrderViewSet, CartViewSet, RegisterViewSet, CustomObtainAuthToken

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('collections', CollectionViewSet, basename='collection')
router.register('customers', CustomerViewSet, basename='customer')
router.register('orders', OrderViewSet, basename='order')
router.register('carts', CartViewSet, basename='cart')
router.register('auth/register', RegisterViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', CustomObtainAuthToken.as_view(), name='token-auth'),
    path('auth/jwt/create/', TokenObtainPairView.as_view(), name='jwt-create'),
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
]