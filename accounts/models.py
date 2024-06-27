from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from .managers import UserManager
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
) 
from services.generator import CodeGenerator


def upload_to(instance, filename):
    return f"users/{instance.email}/{filename}"


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=120)
    mobile = PhoneNumberField(blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    surname = models.CharField(max_length=250, blank=True, null=True)
    logo = models.ImageField(upload_to=upload_to, blank=True, null=True)

    slug = models.SlugField(unique=True)
    activation_code = models.CharField(max_length=6, blank=True, null=True)



    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname", "mobile"]
    
    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "User"
        verbose_name_plural = "User"
    

    def __str__(self):
        return self.email
    
    def full_name(self):
        return f"{self.name} {self.surname}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = CodeGenerator.create_slug_shortcode(size=20, model_=self.__class__)
        if not self.logo:
            default_logo_path = "staticfiles/user/user.jpg"
            self.logo.save("default_user_logo.jpg", open(default_logo_path, "rb"), save=False)
        return super(User, self).save(*args, **kwargs)
    


