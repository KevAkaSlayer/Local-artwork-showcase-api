from django.contrib.auth.base_user import BaseUserManager



class CustomUserManager(BaseUserManager):   
    def create_user(self, email, username, password=None,**extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        user = self.create_user(email, username, password, **extra_fields)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user 