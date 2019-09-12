from django.contrib import admin
from company.models import JobOffer, InternshipOffer, JobAdvertisement, InternshipAdvertisement
from accounts.models import StudentProfile, CompanyPerson, CompanyProfile, Resume
from .resources import CompanyProfileResource, StudentProfileResource
from import_export.admin import ImportExportActionModelAdmin


class JobAdvertisementInline(admin.StackedInline):
    model = JobAdvertisement


class InternshipAdvertisementInline(admin.StackedInline):
    model = InternshipAdvertisement


class JobOfferInline(admin.StackedInline):
    model = JobOffer


class InternshipOfferInline(admin.StackedInline):
    model = InternshipOffer


class CompanyPersonInline(admin.StackedInline):
    model = CompanyPerson


class ResumeInline(admin.StackedInline):
    model = Resume


def approve_resumes(modeladmin, request, queryset):
    queryset.update(is_verified=True)


def unapprove_resumes(modeladmin, request, queryset):
    queryset.update(is_verified=False)


def ban(modeladmin, request, queryset):
    queryset.update(banned=True)


def mark_placed(modeladmin, request, queryset):
    queryset.update(placed=True)


@admin.register(StudentProfile)
class StudentProfileAdmin(ImportExportActionModelAdmin):
    readonly_fields = ['registration_timestamp', ]
    resource_class = StudentProfileResource
    inlines = (ResumeInline,)
    list_display = ['__str__', 'roll_no', 'program_branch', 'year', 'registration_timestamp']
    list_filter = ['program_branch', 'year', 'registration_timestamp']
    ordering = ['roll_no', ]
    search_fields = ['roll_no', 'user__first_name', 'user__last_name']
    actions = [ban, mark_placed]

    class Meta:
        model = StudentProfile
        fields = '__all__'


@admin.register(CompanyProfile)
class CompanyProfileAdmin(ImportExportActionModelAdmin):
    readonly_fields = ['registration_timestamp', ]
    resource_class = CompanyProfileResource
    inlines = (CompanyPersonInline, JobOfferInline, InternshipOfferInline,)
    list_display = ['name', 'domain', 'url', 'registration_timestamp']
    list_filter = ['domain', 'registration_timestamp']
    search_fields = ['name', 'user__username']

    class Meta:
        model = CompanyProfile
        fields = '__all__'


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    readonly_fields = ['timestamp', ]
    ordering = ['student', ]
    list_display = ['get_roll_no', 'student', 'get_gpa', 'reference', 'file', 'is_verified', 'timestamp', ]
    search_fields = ['student__user__first_name', 'student__user__last_name', 'student__user__username']
    list_filter = ['is_verified', 'timestamp']
    actions = [approve_resumes, unapprove_resumes]

    def get_roll_no(self, instance):
        return instance.student.roll_no

    def get_gpa(self, instance):
        return instance.student.gpa

    class Meta:
        model = Resume
        fields = '__all__'
