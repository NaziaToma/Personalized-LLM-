from django.db import models


class Recipe(models.Model):
    """Represents a recipe in the system."""
    name = models.CharField(max_length=255)
    steps = models.TextField()

    def __str__(self):
        return self.name

#AI chat session model

class AiChatSession(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
#AI request model
class AiRequest(models.Model):
    
    #adding status
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETE = 'complete'
    FAILED = 'failed'
    #user will see this
    STATUS_OPTIONS = (
        (PENDING, 'Pending'),
        (RUNNING, 'Running'),
        (COMPLETE, 'Complete'),
        (FAILED, 'Failed')
    )

    status = models.CharField(choices=STATUS_OPTIONS, default=PENDING)
    
    #this stores each chat session's id  
    session = models.ForeignKey(
        AiChatSession,
        on_delete=models.CASCADE,
        null = True,
        blank= True
    )
    #This stores user input
    message = models.JSONField()
    
    #This stores AI's response 
    response = models.JSONField(null = True, blank = True)
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    