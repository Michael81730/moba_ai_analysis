from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import auth_handlers
from . import match_handlers

app_name = "moba_ai_analysis"
urlpatterns = [
    path("signup", auth_handlers.user_signup, name="signup"),
    path("csrf-token", auth_handlers.csrf_token, name="csrf_token"),
    
    path("login", auth_handlers.user_login, name="login"),
    path("logout", auth_handlers.user_logout, name="logout"),
    path("token-refresh", TokenRefreshView.as_view(), name="token_refresh"),

    path("password-reset", auth_handlers.password_reset, name="password_reset"),
    # path("test-protected-api", auth_handlers.test_protected_api, name="test_protected_api"),

    path("match_events", match_handlers.match_events, name="match_events"),
    path("match_vision_graph", match_handlers.match_vision_graph, name="match_vision_graph"),
]