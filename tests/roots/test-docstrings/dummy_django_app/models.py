from django.db import models

try:
    from phonenumber_field.modelfields import PhoneNumberField

    PHONENUMBER = True
except ModuleNotFoundError:
    # In case phonenumber is not used, pass
    PHONENUMBER = False


class SimpleModelManager(models.Manager):
    pass


class FileModel(models.Model):
    file = models.FileField()


class SimpleModel(models.Model):
    # Foreign Keys
    foreignkey = models.ForeignKey(
        "FileModel",
        related_name="reverse_foreignkey",
        on_delete=models.CASCADE,
    )

    # One to one field
    onetoonefield = models.OneToOneField(
        "ChildModel",
        related_name="reverse_onetoonefield",
        on_delete=models.CASCADE,
    )

    # Dummy field
    dummy_field = models.CharField(
        max_length=3,
        help_text="This should help you",
        verbose_name="Very verbose name of dummy field",
    )

    #: Custom model manager
    custom_objects = SimpleModelManager()

    # Mock get_..._display method of Django models
    def get_dummy_field_display(self):
        pass

    # Mock common get_next_by_ method
    def get_next_by_dummy_field(self):
        pass

    # Mock common get_previous_by_ method
    def get_previous_by_dummy_field(self):
        pass


class AbstractModel(models.Model):
    foreignkey_string = models.ForeignKey(
        "SimpleModel",
        related_name="rev_f_str",
        on_delete=models.CASCADE,
    )
    foreignkey_string_containing_dot = models.ForeignKey(
        "auth.User", related_name="+", on_delete=models.CASCADE
    )
    foreignkey_string_self = models.ForeignKey("self", on_delete=models.CASCADE)

    class Meta:
        abstract = True


class ChildModel(AbstractModel):
    pass


if PHONENUMBER:

    class PhoneNumberModel(models.Model):
        phone_number = PhoneNumberField()
