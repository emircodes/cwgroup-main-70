from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import date
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager

# Create your models here.
    
class UserManager(BaseUserManager):
    def create_user(self, email: str, password: Optional[str] =None, **extra_fields: dict) -> "User":
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user: User = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: Optional[str] =None, **extra_fields: dict) -> "User":
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email: str) -> "User":
        return self.get(email=email)

#Custom User Model
class User(AbstractUser):
    name: str = models.CharField(max_length=100)
    email: str = models.EmailField(unique=True)
    date_of_birth: Optional[date] = models.DateField(null=True, blank=True)
    hobbies: "RelatedManager[Hobby]" = models.ManyToManyField('Hobby', blank=True)
    friends: "RelatedManager[User]" = models.ManyToManyField('self', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    objects = UserManager()

    def __str__(self) -> str:
        return self.email
    
    @property
    def age(self) -> Optional[int]:
        if self.date_of_birth:
            today: date = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
    
    def add_friend(self, user: "User") -> None:
        self.friends.add(user)
        user.friends.add(self)
    
    def remove_friend(self, user: "User") -> None:
        self.friends.remove(user)
        user.friends.remove(self)
        
    def add_hobby(self, hobby: "Hobby") -> None: 
        self.hobbies.add(hobby)
        
    def remove_hobby(self, hobby: "Hobby") -> None:
        self.hobbies.remove(hobby)

#Hobby Model
class Hobby(models.Model):
    name = models.CharField(max_length=100, unique=True)
    popularity = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name
    
#Friend Request Model
class FriendRequest(models.Model):
    sender: "User" = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver: "User" = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status: str = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='pending'
    )
    created_at: date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self) -> str:
        return f"{self.sender.email} -> {self.receiver.email} ({self.status})"

    def accept(self) -> None:
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


    def reject(self) -> None:
        if self.status != 'pending':
            raise ValueError("Only pending requests can be rejected.")
        self.status = 'rejected'
        self.save()

        Notification.objects.create(
            user=self.sender,
            message=f"{self.receiver.name} rejected your friend request.",
        )

    def cancel(self) -> None:
        if self.status != 'pending':
            raise ValueError("Only pending requests can be canceled.")
        self.delete()


#Notification Model
class Notification(models.Model):
    user: "User" = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message: str = models.TextField()
    is_read: bool = models.BooleanField(default=False)
    created_at: date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Notification for {self.user.username}: {self.message[:20]}"
    
    def mark_as_read(self) -> None:
        self.is_read = True
        self.save()

    @staticmethod
    def mark_all_as_read(user: "User") -> None:
        user.notifications.filter(is_read=False).update(is_read=True)
