from django.db import models
from django.contrib.auth.models import User

class PlaneType(models.TextChoices):
    TB2 = "TB2", "TB2"
    TB3 = "TB3", "TB3"
    AKINCI = "Akinci", "Akinci"
    KIZILELMA = "Kizilelma", "Kizilelma"

class Department(models.TextChoices):
    KANAT_TAKIMI = "Kanat Takimi", "Kanat Takimi"
    GOVDE_TAKIMI = "Gövde Takimi", "Gövde Takimi"
    KUYRUK_TAKIMI = "Kuyruk Takimi", "Kuyruk Takimi"
    AVIYONIK_TAKIMI = "Aviyonik Takimi", "Aviyonik Takimi"
    MONTAJ_TAKIMI = "Montaj Takimi", "Montaj Takimi"

class PartModel(models.TextChoices):
    KANAT = "Kanat", "Kanat"
    GOVDE = "Govde", "Govde"
    KUYRUK = "Kuyruk", "Kuyruk"
    AVIYONIK = "Aviyonik", "Aviyonik"

# Parça Modeli
class Part(models.Model):
    part_name = models.CharField(max_length=20, choices=PartModel.choices)
    plane_type = models.CharField(max_length=20, choices=PlaneType.choices)
    department = models.CharField(max_length=20, choices=Department.choices)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.part_name} ({self.department})"

# Montaj Modeli
class Assembly(models.Model):
    plane_type = models.CharField(max_length=20, choices=PlaneType.choices)
    assembly_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.plane_type} - {self.assembly_date.strftime('%Y-%m-%d %H:%M:%S')}"

# Kullanılan Parçalar Modeli
class UsedPart(models.Model):
    assembly = models.ForeignKey(Assembly, on_delete=models.CASCADE, related_name="used_parts")
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity_used = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity_used} x {self.part.part_name} in {self.assembly}"
    
class UserCred(models.Model):
    department = models.CharField(max_length=20, choices=Department.choices)
    user=models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.department}"