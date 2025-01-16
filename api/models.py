from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import date

# Create your models here.
    
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)

class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    #hobbies = models.TextField(blank=True)
    hobbies = models.ManyToManyField('Hobby', blank=True)
    friends = models.ManyToManyField('self', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
    
    def add_friend(self, user):
        self.friends.add(user)
    
    def remove_friend(self, user):
        self.friends.remove(user)
        
    def add_hobby(self, hobby: "Hobby") -> None: 
        self.hobbies.add(hobby)
        
    def remove_hobby(self, hobby: "Hobby") -> None:
        self.hobbies.remove(hobby)


class Hobby(models.Model):
    name = models.CharField(max_length=100, unique=True)
    popularity = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    

class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender.email} -> {self.receiver.email} ({self.status})"

    def accept(self):
        if self.status != 'pending':
            raise ValueError("Only pending requests can be accepted.")
        self.sender.add_friend(self.receiver)
        self.receiver.add_friend(self.sender)
        self.status = 'accepted'
        self.save()

        Notification.objects.create(
            user=self.sender,
            message=f"{self.receiver.name} accepted your friend request.",
        )


    def reject(self):
        if self.status != 'pending':
            raise ValueError("Only pending requests can be rejected.")
        self.status = 'rejected'
        self.save()

        Notification.objects.create(
            user=self.sender,
            message=f"{self.receiver.name} rejected your friend request.",
        )

    def cancel(self):
        if self.status != 'pending':
            raise ValueError("Only pending requests can be canceled.")
        self.delete()

    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:20]}"