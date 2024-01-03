from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser
from twilio.rest import Client

class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)


class Session(models.Model):
    start_year = models.DateField()
    end_year = models.DateField()

    def __str__(self):
        return "From " + str(self.start_year) + " to " + str(self.end_year)


class CustomUser(AbstractUser):
    USER_TYPE = ((1, "HOD"), (2, "Staff"), (3, "Student"))
    GENDER = [("M", "Male"), ("F", "Female")]


    username = None  # Removed username, using email instead
    email = models.EmailField(unique=True)
    user_type = models.CharField(default=1, choices=USER_TYPE, max_length=1)
    gender = models.CharField(max_length=1, choices=GENDER)
    profile_pic = models.ImageField()

    address = models.TextField()
    fcm_token = models.TextField(default="")  # For firebase notifications
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    phone_num = models.IntegerField(max_length=12 ,null=True,blank=False)
    aadhar_num = models.IntegerField(max_length=16,null=True,blank=False)
    date_of_birth = models.DateField(null=True,blank=False)

    def __str__(self):
        return self.first_name + "  " + self.last_name


class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

class Department(models.Model):
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=120)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Student(models.Model):

    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True, blank=False)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=False)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)
    phone_num = models.IntegerField(max_length=12 ,null=True,blank=False)
    aadhar_num = models.IntegerField(max_length=12,null=True,blank=False)
    date_of_birth = models.DateField(null=True,blank=False)
    religion = models.CharField(max_length=12,null=True,blank=False)
    register_num = models.CharField(max_length=12,null=True,blank=False)
    admission_num = models.CharField(max_length=16,null=True,blank=False)


    def __str__(self):
        return self.admin.first_name + ", " + self.admin.last_name


class Staff(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=False)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_num = models.IntegerField(max_length=12 ,null=True,blank=False)
    qualification = models.CharField(max_length=20,null=True,blank=False)
    aadhar_num = models.IntegerField(max_length=12,null=True,blank=False)
    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name


class Subject(models.Model):
    name = models.CharField(max_length=120)
    staff = models.ForeignKey(Staff,on_delete=models.CASCADE,)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True, blank=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AttendanceReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.message

    def save(self,*args,**kwargs):
        account_sid = "ACaa9720195b1101f4f741a8336d53886a"
        auth_token = "053c69ac82834960211afb5867bc4fc8"
        client = Client(account_sid, auth_token)
        message = client.messages.create(
          body=f"HI ,{self.message}",
          from_="+16515656402",
          to=f"+91{self.staff.phone_num}"

        )

        print(message.sid)
        return super().save(*args,**kwargs)

    # def save(self,*args,**kwargs):
    #     account_sid = "ACaa9720195b1101f4f741a8336d53886a"
    #     auth_token = "053c69ac82834960211afb5867bc4fc8"
    #     client = Client(account_sid, auth_token)
    #     message = client.messages.create(
    #       body=f"HI ,{self.message}",
    #       from_='whatsapp:+14155238886',
    #       to=f'whatsapp:+91{self.staff.phone_num}'

    #     )

    #     print(message.sid)
    #     return super().save(*args,**kwargs)



class NotificationStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

    # def save(self,*args,**kwargs):
    #     account_sid = "ACaa9720195b1101f4f741a8336d53886a"
    #     auth_token = "053c69ac82834960211afb5867bc4fc8"
    #     client = Client(account_sid, auth_token)
    #     message = client.messages.create(
    #       body=f"HI ,{self.message}",
    #       from_="+16515656402",
    #       to=f"+91{self.student.phone_num}"

    #     )
    #     print(message.sid)
    #     return super().save(*args,**kwargs)

    def save(self,*args,**kwargs):
        account_sid = "ACaa9720195b1101f4f741a8336d53886a"
        auth_token = "053c69ac82834960211afb5867bc4fc8"
        client = Client(account_sid, auth_token)
        message = client.messages.create(
          body=f"HI ,{self.message}",
          from_='whatsapp:+14155238886',
          to=f'whatsapp:+91{self.student.phone_num}'

        )

        print(message.sid)
        return super().save(*args,**kwargs)

class StudentResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test = models.FloatField(default=0)
    exam = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Staff.objects.create(admin=instance)
        if instance.user_type == 3:
            Student.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.student.save()
