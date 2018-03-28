from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.urls import reverse

from domain.models import Domain

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # Create user profile
        AgentProfile(user = user).save()

        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
           
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Agent(AbstractUser):
    """User model"""

    username = None
    email = models.EmailField('email address', unique=True)
    is_owner = models.BooleanField(default=False)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='agents', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class AgentProfile(models.Model):

    phone = models.CharField(max_length=60, blank=True, null=True)
    first_name = models.CharField(max_length=60, blank=True, null=True)
    last_name = models.CharField(max_length=60, blank=True, null=True)
    avatar = models.ImageField(upload_to = 'avatars/', default = 'avatars/no-img.png')
    title = models.CharField(max_length=120, blank=True, null=True)

    user = models.OneToOneField(Agent, related_name='profile', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('agent:detail', kwargs={'email': self.user.email})

# Activation signal
def check_domain(sender, user, request, **kwargs):
    domain, created = Domain.objects.get_or_create(name=user.email.split('@')[1])
    if created: user.is_owner = True
    user.domain = domain
    user.save()

from registration.signals import user_activated
user_activated.connect(check_domain, dispatch_uid='registration.signals.user_activated')

