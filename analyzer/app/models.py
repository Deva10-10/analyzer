

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"


class RequirementAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    startup_idea = models.TextField()
    risk_analysis = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    problem_statement = models.TextField()
    features = models.TextField()
    user_stories = models.TextField()
    tech_stack = models.TextField()
    risks = models.TextField()
    mvp_scope = models.TextField()
    future_scope = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Requirement by {self.user.username} on {self.created_at}"