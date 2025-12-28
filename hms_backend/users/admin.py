from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, PatientProfile, DoctorProfile, NurseProfile, PharmacistProfile, LabTechProfile, RadiologistProfile, ReceptionistProfile
from  .forms import CustomUserCreationForm


class PatientProfileInline(admin.StackedInline):
    model = PatientProfile
    can_delete = False
    verbose_name_plural = 'Patient Profile'

class DoctorProfileInline(admin.StackedInline):
    model = DoctorProfile
    can_delete = False
    verbose_name_plural = 'Doctor Profile'

class NurseProfileInline(admin.StackedInline):
    model = NurseProfile
    can_delete = False
    verbose_name_plural = 'Nurse Profile'

class PharmacistProfileInline(admin.StackedInline):
    model = PharmacistProfile
    can_delete = False
    verbose_name_plural = 'Pharmacist Profile'

class LabTechProfileInline(admin.StackedInline):
    model = LabTechProfile
    can_delete = False
    verbose_name_plural = 'Lab Technician Profile'

class RadiologistProfileInline(admin.StackedInline):
    model = RadiologistProfile
    can_delete = False
    verbose_name_plural = 'Radiologist Profile'

class ReceptionistProfileInline(admin.StackedInline):
    model = ReceptionistProfile
    can_delete = False
    verbose_name_plural = 'Receptionist Profile'

class UserAdmin(BaseUserAdmin):
    add_form=CustomUserCreationForm
    list_display=('email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter=('role', 'is_staff','is_active')
    fieldsets=(
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2')}
        ),
    )

    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        
        inlines = []
        if obj.role == 'PATIENT':
            inlines.append(PatientProfileInline(self.model, self.admin_site))
        elif obj.role == 'DOCTOR':
            inlines.append(DoctorProfileInline(self.model, self.admin_site))
        elif obj.role == 'NURSE':
            inlines.append(NurseProfileInline(self.model, self.admin_site))
        elif obj.role == 'PHARMACIST':
            inlines.append(PharmacistProfileInline(self.model, self.admin_site))
        elif obj.role == 'LAB_TECH':
            inlines.append(LabTechProfileInline(self.model, self.admin_site))
        elif obj.role == 'RADIOLOGIST':
            inlines.append(RadiologistProfileInline(self.model, self.admin_site))
        elif obj.role == 'RECEPTIONIST':
            inlines.append(ReceptionistProfileInline(self.model, self.admin_site))

        return inlines
    
admin.site.register(User, UserAdmin)
admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)
admin.site.register(NurseProfile)
admin.site.register(PharmacistProfile)
admin.site.register(LabTechProfile)
admin.site.register(RadiologistProfile)
admin.site.register(ReceptionistProfile)



# Register your models here.
