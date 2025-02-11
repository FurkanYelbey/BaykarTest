from django.test import TestCase
from .models import Part, Assembly, UserCred, Department, PlaneType
from django.contrib.auth.models import User
from rest_framework import status

class PartTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.user_cred = UserCred.objects.create(department=Department.GOVDE_TAKIMI, user=self.user)
        Part.objects.create(part_name="Govde", plane_type="TB2", department="Govde Takimi", quantity=1)

        self.part = Part.objects.create(
            part_name="Govde",
            plane_type=PlaneType.TB2,
            department=Department.GOVDE_TAKIMI,
            quantity=10
        )

        self.client.login(username='testuser', password='password123')

    def test_part_list(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Govde")
        

    def test_part_create(self):
        data = {
            "part_name": "Govde",
            "plane_type": PlaneType.TB3,
            "department": Department.GOVDE_TAKIMI,
            "quantity": 2
        }

        response = self.client.post('/part_create/', data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Govde parçası başarıyla eklendi.")
        self.assertTrue(Part.objects.filter(part_name="Govde", plane_type=PlaneType.TB3).exists())

    def test_part_create_wrong_dep(self):

        data = {
            "part_name": "Govde",
            "plane_type": PlaneType.TB3,
            "department": Department.AVIYONIK_TAKIMI,
            "quantity": 2
        }

        response = self.client.post('/part_create/', data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gövde Takimi departmanına ait olmayan bir parça oluşturamazsınız.")
        self.assertFalse(Part.objects.filter(part_name="Govde", department=Department.AVIYONIK_TAKIMI).exists())

    def test_part_delete(self):

        delete_url = f'/delete_part/{self.part.pk}/'

        response = self.client.post(delete_url)  # POST isteği ile silme işlemi yap

        # 302 yönlendirme aldık mı?
        self.assertEqual(response.status_code, 302)

        # Yönlendirilen URL gerçekten 'part_list' mi?
        self.assertRedirects(response, '/')

        # Veritabanında parça gerçekten silindi mi?
        self.assertEqual(Part.objects.count(), 1)
