"""User model"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



class UtilisateurAccountManager(BaseUserManager):

    def create_user(self, nom, prenom, email, telephone, password=None):
        if not nom:
            raise ValueError("Nom requis")
        if not prenom:
            raise ValueError("prénom requis")
        if not email:
            raise ValueError("Email requis")
        if not telephone:
            raise ValueError("téléphone requis")
        email = self.normalize_email(email)

        user = self.model(nom=nom, prenom=prenom, email=email,telephone=telephone)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nom, prenom, email, telephone, password):

        email = self.normalize_email(email)

        user = self.create_user(nom=nom, prenom=prenom, email=email, telephone=telephone, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user

    def getProfileImageFilepath(self, filename):
        return  f'profile_images/{self.pk}/{"profile_image.png"}'


    def getDefaultProfileImage(self, filename):
        return  "public/images/logo.png"

#TODO:Permissions mixin https://stackoverflow.com/questions/31370333/custom-django-user-object-has-no-attribute-has-module-perms
#https://stackoverflow.com/questions/1190697/django-filefield-with-upload-to-determined-at-runtime?rq=1
#https://stackoverflow.com/questions/25767787/django-cannot-create-migrations-for-imagefield-with-dynamic-upload-to-value
class Utilisateur(AbstractBaseUser, PermissionsMixin):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email                = models.EmailField(verbose_name="email", max_length=100, unique=True)
    telephone                = models.CharField( max_length=50, unique=True)
    date_joined                = models.DateTimeField( verbose_name="date joined", auto_now_add=True)
    last_login                = models.DateTimeField( verbose_name="last login", auto_now=True)
    is_admin                = models.BooleanField( default=False)
    is_active                = models.BooleanField( default=True)
    is_staff                = models.BooleanField( default=False)
    is_superuser                = models.BooleanField( default=False)
    profil_image                = models.ImageField(max_length=255, upload_to="uploads/%Y/%m/%d/", null=True, blank=True, default="")


    objects = UtilisateurAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'telephone']

    def __str__(self):
        return self.nom + " " + self.prenom + " " +self.telephone


    # has admin permission?
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # has admin permission?
    def has_module_perms(self, app_label):
        return True

    def getProfileImageFilename(self):
        return str(self.profil_image)[str(self.profil_image).index(f'profile_image/{self.pk}/'):]



