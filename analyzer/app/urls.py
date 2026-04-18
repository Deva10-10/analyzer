# analyzer/app/urls.py 

from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path("",            views.login_view,    name="login"),
    path("register/",   views.register_view, name="register"),
    path("logout/",     views.logout_view,   name="logout"),

    # Dashboard
    path("dashboard/",  views.dashboard,     name="dashboard"),

    # Feature 1: Requirement Analyzer
    path("analyze/",                    views.risk_analysis, name="risk_analysis"),
    path("analyze/<int:analysis_id>/",  views.risk_detail,   name="risk_detail"),

    # Feature 2: Idea Clarity Score
    path("clarity/",        views.idea_clarity,   name="idea_clarity"),

    # Feature 3: Business Model Analyzer
    path("business-model/", views.business_model, name="business_model"),

    # Feature 4: Cost Estimator
    path("cost/",           views.cost_estimator, name="cost_estimator"),

    # Feature 5: Roadmap Generator
    path("roadmap/",        views.roadmap,        name="roadmap"),

    # AI Chatbot
    path("chatbot/",        views.chatbot,        name="chatbot"),

    # Utilities
    path("delete/<int:chat_id>/",   views.delete_chat,   name="delete_chat"),
    path("download/<int:chat_id>/", views.download_chat, name="download_chat"),
]
