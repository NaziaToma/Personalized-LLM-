from openai import OpenAI
from django.db import models
from core.tasks import handle_ai_request_job


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
    
    def _queue_job(self):
        """add job to queue, asynchronous task"""
        handle_ai_request_job.delay(self.id)
    
    
    def handle(self):
        """Handle request"""
        
        self.status = self.RUNNING
        self.save()
        client = OpenAI()
        try:
            completion = client.chat.completions.create(
                model= "gpt-4o-mini",
                messages=self.message
            )
            self.response = completion.to_dict()
            self.status = self.COMPLETE
        except:
            self.status=self.FAILED
        self.save()
    
    
    def save(self, **kwargs):
        is_new =self._state.adding
        super().save(**kwargs)
        if is_new:
            self._queue_job()