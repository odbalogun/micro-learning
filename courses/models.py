from django.db import models
from django.conf import settings
from safedelete.models import SafeDeleteModel
from django.template.defaultfilters import slugify
from smart_selects.db_fields import ChainedForeignKey
from tinymce.models import HTMLField
from django.urls import reverse
import datetime


PAYMENT_STATUS_CHOICES = (
    ('unpaid', 'Unpaid'),
    ('partly', 'Part Payment'),
    ('paid', 'Fully Paid')
)

ENROLLED_STATUS_CHOICES = (
    ('ongoing', 'Ongoing'),
    ('completed', 'Completed')
)


def course_image_path(instance, filename):
    # for file uploads
    return 'images/events/events/{0}/{1}/{2}/{3}'.format(datetime.datetime.now().year, datetime.datetime.now().month,
                                                         datetime.datetime.now().day, filename)


class Courses(SafeDeleteModel):
    name = models.CharField('name', null=False, max_length=100)
    slug = models.CharField('slug', null=False, max_length=100)
    course_code = models.CharField('course code', null=True, blank=True, max_length=50)
    short_description = models.TextField('short description', max_length=300)
    learning_and_outcome = HTMLField('learning and outcome', blank=True, null=True)
    outline = HTMLField('outline', blank=True, null=True)
    overview = models.TextField('overview', blank=False, null=False)
    pre_requisites = models.TextField('pre-requisites', blank=False, null=False)
    strategy = models.TextField('course strategy', blank=True, null=True)
    tools_and_technology = models.TextField('tools and Technologies', blank=True, null=True)
    course_fee = models.DecimalField('course fee', decimal_places=2, max_digits=10)
    image = models.ImageField('image', upload_to=course_image_path)
    is_active = models.BooleanField('is active', default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_courses', on_delete=models.SET_NULL,
                                   null=True)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrolled', through_fields=('course', 'user'))

    def students_count(self):
        return self.students.count()

    def modules_count(self):
        return self.modules.count()

    @property
    def get_max_module_position(self):
        if self.modules_count() == 0:
            return 0
        return self.modules.aggregate(models.Max('order'))['order__max']

    def __str__(self):
        return self.name

    def display_fee(self):
        return "${:0,.2f}".format(self.course_fee)

    def save(self, *args, **kwargs):
        # Overwrite save to allow for slug creation
        self.slug = slugify(self.name)
        super(Courses, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('courses:detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'course'
        verbose_name_plural = 'courses'

    # labels
    display_fee.short_description = 'Course Fee'
    students_count.short_description = 'Students'
    modules_count.short_description = 'Modules'


class Modules(SafeDeleteModel):
    course = models.ForeignKey(Courses, related_name='modules', on_delete=models.CASCADE)
    name = models.CharField('name', blank=False, max_length=100)
    description = models.TextField('description')
    access_code = models.CharField('media code', max_length=100, null=True, blank=True)
    order = models.IntegerField('position')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_modules', on_delete=models.CASCADE)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='modules', through="EnrolledModules")

    def __str__(self):
        return "{}: {}".format(self.order, self.name)

    class Meta:
        unique_together = ('course', 'order')
        # order_by = 'order'
        verbose_name = 'module'
        verbose_name_plural = 'modules'


class Enrolled(SafeDeleteModel):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrolled_courses')
    status = models.CharField(max_length=50, choices=ENROLLED_STATUS_CHOICES, default='ongoing')
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES)
    current_module = ChainedForeignKey(Modules, chained_field='course', chained_model_field='course', show_all=False,
                                       auto_choose=True, on_delete=models.SET_NULL, null=True)
    date_enrolled = models.DateTimeField('date enrolled', auto_now_add=True)

    class Meta:
        unique_together = ('course', 'user')
        verbose_name_plural = 'Enrollments'
        verbose_name = 'Enrollment'

    def __str__(self):
        return "{}: {}".format(self.course, self.user)


class EnrolledModules(SafeDeleteModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    module = models.ForeignKey(Modules, on_delete=models.CASCADE)
    enrolled = models.ForeignKey(Enrolled, related_name='modules', on_delete=models.CASCADE)
    date_activated = models.DateTimeField('date activated', auto_now_add=True)
    days = models.IntegerField('open for', default=7)
    expires = models.DateTimeField('date expires')

    class Meta:
        unique_together = ('user', 'module')

    def set_expires(self):
        if getattr(self, 'days'):
            self.expires = datetime.datetime.now() + datetime.timedelta(days=self.days)