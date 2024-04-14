from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

"""
    Student: Firstname Lastname authentication Level Course_status
    Tutor: Firstname Lastname Level Subject
    Courses: Course_name Course_description Course_level Course_subject Course_tutor
    Course_status: Course_name Course_description Course_completion Course_type
"""

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
        return user

    def create_user(self, email, password, **extra_fields):
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


class User(AbstractUser):
    username = None
    USERNAME_FIELD = 'email'
    email = models.EmailField(_('email address'), unique=True)
    REQUIRED_FIELDS = []      # No additional required fields

    objects = UserManager()

# Enumerations for level and country choices
class Level(models.TextChoices):
    f5 = "Form 5"
    l6 = "Lowersixth"
    u6 = "Uppersixth"
    uni = "University"
    no_ed = "No formal education"

class Country(models.TextChoices):
    cameroon = "Cameroon"
    nigeria = "Nigeria"
    rwanda = "Rwanda"
    kenya = "Kenya"
    zambia = "Zambia"
    other = "other"

class Student(models.Model):
    """
    Model representing a student.

    Attributes:
        user (OneToOneField): The user associated with the student.
        level (CharField): The education level of the student.
        country (CharField): The country of residence of the student.
        created_at (DateField): The date when the student record was created.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="profile_pics", default="profile_pics/Default_pfp.svg") # Should also change this to imagefield
    level = models.CharField(max_length=100, choices=Level.choices)
    country = models.CharField(max_length=100, choices=Country.choices)
    bio = models.TextField(blank=True, null=True)
    preferred_name = models.CharField(max_length=20, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    enrolled_courses = models.ManyToManyField('Course', related_name='enrolled_students')
    saved_courses = models.ManyToManyField('Course', related_name='saved_students')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name
    
class Socials(models.Model):
    github = models.URLField(max_length=200,blank=True, null=True)
    instagram = models.URLField(max_length=200, blank=True, null=True)
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    facebook = models.URLField(max_length=200, blank=True, null=True)
    twitter = models.URLField(max_length=200, blank=True, null=True) 
    number = models.IntegerField(blank=True, null=True)


class Tutor(models.Model):
    """
    Model representing a tutor.

    Attributes:
        user (OneToOneField): The user associated with the tutor.
        level (CharField): The education level of the tutor.
        subject (CharField): The subject taught by the tutor.
        verified (BooleanField): Indicates whether the tutor is verified.
        created_at (DateField): The date when the tutor record was created.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="profile_pics", default="https://upload.wikimedia.org/wikipedia/commons/2/2c/Default_pfp.svg") # Should also change this to imagefield
    level = models.CharField(max_length=100, choices=Level.choices)
    subject = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        if self.user.is_superuser:
            return "Admin"
        return self.user.first_name + " " + self.user.last_name


class Course(models.Model):
    """
    Model representing a course.

    Attributes:
        course_name (CharField): The name of the course.
        course_description (TextField): The description of the course.
        time_to_complete (CharField): The estimated time to complete the course.
        price (DecimalField): The price of the course.
        created_at (DateField): The date when the course record was created.
    """
    course_name = models.CharField(max_length=100)
    course_image = models.TextField()
    course_description = models.TextField()
    course_category = models.TextField() # Should change to textchoices
    course_tutor = models.ForeignKey(Tutor, on_delete=models.SET_DEFAULT, default=1)
    time_to_complete = models.CharField(max_length=100)
    price = models.DecimalField(blank=True, validators=[MinValueValidator(0)], decimal_places=2, max_digits=10, default=0.0)
    created_at = models.DateField(auto_now_add=True)

class CourseWeek(models.Model):
    """
    Model representing a course week.

    Attributes:
        course (ForeignKey): The course associated with the week.
        week_number (IntegerField): The number of the week.
        week_text (TextField): The text content of the week.
        week_videos (TextField): The video content of the week.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    week_number = models.IntegerField()
    week_text = models.TextField(blank=True, null=True)
    week_videos = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("course", "week_number")

class WeekStatus(models.Model):
    """
    Model representing the status of a week for a student.

    Attributes:
        week (ForeignKey): The week associated with the status.
        student (ForeignKey): The student associated with the status.
        completed (BooleanField): Indicates whether the week is completed by the student.
        grade (IntegerField): The grade received by the student for the week.
    """
    week = models.ForeignKey(CourseWeek, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    modified_at = models.DateField(auto_now=True)
    
    class Meta:
        unique_together = ("week", "student")

class Grade(models.Model):
    """
    Represents a grade for a specific week status.

    Attributes:
        week_status (WeekStatus): The week status associated with this grade.
        grade (Decimal): The grade value, ranging from 0 to 100.
        created_at (Date): The date and time when the grade was created.
    """
    week_status = models.ForeignKey(WeekStatus, on_delete=models.CASCADE)
    grade = models.DecimalField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)], decimal_places=2, max_digits=10)
    created_at = models.DateField(auto_now_add=True)

class Achievement(models.Model):
    """
    Represents an achievement that can be earned by users.

    Attributes:
        course (Course): The course associated with this achievement.
        achievement_icon (str): The path to the icon representing the achievement.
        name (str): The name of the achievement.
        description (str): The description of the achievement.
    """
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    achievement_icon = models.ImageField(upload_to='achievement_icons') # Should prolly change it to ImageField after
    name = models.CharField(max_length=100)
    description = models.TextField()

class UserAchievement(models.Model):
    """
    Represents a user's achievement.

    Attributes:
        student (Student): The student who achieved this achievement.
        achievement (Achievement): The achievement earned by the student.
        achieved_at (DateTime): The date and time when the achievement was earned.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    achieved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "achievement")

class Quiz(models.Model):
    """
    Represents a quiz.

    Attributes:
        title (str): The title of the quiz.
        description (str): The description of the quiz.
        created_at (DateTime): The date and time when the quiz was created.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    """
    Represents a question in a quiz.

    Attributes:
        quiz (Quiz): The quiz to which this question belongs.
        question_text (str): The text of the question.
        question_type (str): The type of the question (MCQ, SA, TF).
        possible_answers (str): The possible answers for the question.
        marks (int): The marks assigned to the question.
    """
    QUIZ_QUESTION_TYPE_CHOICES = [
        ('MCQ', 'Multiple Choice'),
        ('SA', 'Short Answer'),
        ('TF', 'True/False'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(max_length=3, choices=QUIZ_QUESTION_TYPE_CHOICES)
    possible_answers = models.TextField()
    marks = models.IntegerField()

    def __str__(self):
        return self.question_text

class Answer(models.Model):
    """
    Represents an answer to a question.

    Attributes:
        question (Question): The question to which this answer belongs.
        answer_text (str): The text of the answer.
        is_correct (bool): Indicates whether the answer is correct or not.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text

class CourseComment(models.Model):
    """
    Represents a comment on a course.

    Attributes:
        course (Course): The course on which the comment is made.
        user (User): The user who made the comment.
        comment (str): The text of the comment.
        added_at (DateTime): The date and time when the comment was added.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    comment = models.TextField()
    added_at = models.DateTimeField(auto_now=True)
