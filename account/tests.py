from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse_lazy


class TestRgisterView(APITestCase):
    register_view_url = reverse_lazy("register-view")
    
    valid_register_user_data = {
        "name": "some",
        "email": "some@gmail.com",
        "phone_number": "09123456789",
        "password": "Example@12345",
        "password2": "Example@12345"
    }

    invalid_register_user_data = {
        "name": "some",
        "email": "somegmail.com",
        "phone_number": "123g56789",
        "password": "Example@12345",
        "password2": "Example@12345"
    }

    def test_valid_register(self):
        response = self.client.post(
            self.register_view_url,
            self.valid_register_user_data, format="json") 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_register(self):
        response = self.client.post(
            self.register_view_url,
            self.invalid_register_user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
  

class TestChangePasswordView(APITestCase):
    register_view_url = reverse_lazy("register-view")
    change_password_url = reverse_lazy("change-password")

    register_user_data = {
        "name": "some",
        "email": "some@gmail.com",
        "phone_number": "09123456789",
        "password": "Example@12345",
        "password2": "Example@12345"
    }

    valid_change_password_data = {
        "current_password": "Example@12345",
        "new_password": "Example$12345",
        "new_password2": "Example$12345"
    }

    invalid_change_password_data = {
        "current_password": "Example@12345",
        "new_password": "Example@12345",
        "new_password2": "Example@1234"
    }

    def setUp(self):
        response = self.client.post(
            self.register_view_url,
            self.register_user_data, format="json")
        self.access_token = response.data["access"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_valid_change_password(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = client.post(self.change_password_url, self.valid_change_password_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_change_password(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = client.post(self.change_password_url, self.invalid_change_password_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestProfileView(APITestCase):
    register_view_url = reverse_lazy("register-view")
    profile_view_url = reverse_lazy("profile-view")
    login_view_url = reverse_lazy("token_obtain_pair")
    refresh_view_url = reverse_lazy("token_refresh")

    register_user_data = {
        "name": "some",
        "email": "some@gmail.com",
        "phone_number": "09123456789",
        "password": "Example@12345",
        "password2": "Example@12345"
    }

    valid_update_user_data = {
        "name": "some-updated",
        "email": "some-updated@gmail.com",
        "phone_number": "09123456789",
    }

    invalid_update_user_data = {
        "username": "some-updated",
        "phone_number": "0912345789"
    }

    def setUp(self):
        response = self.client.post(
            self.register_view_url,
            self.register_user_data, format="json")
        self.access_token = response.data["access"]
        self.refresh_token = response.data["refresh"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_valid_profile_get(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = client.get(self.profile_view_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_profile_get(self):
        response = self.client.get(self.profile_view_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_invalid_profile_put(self):
        response = self.client.put(self.profile_view_url, data=self.valid_update_user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_valid_profile_patch(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = client.patch(self.profile_view_url, data=self.valid_update_user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_profile_patch(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = client.patch(self.profile_view_url, data=self.invalid_update_user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_invalid_profile_patch(self):
        response = self.client.patch(self.profile_view_url, data=self.valid_update_user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)    
      
    def test_login(self):
        data = {"email": "some@gmail.com", "password": "Example@12345"}  
        response = self.client.post(self.login_view_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)  

    def test_refresh(self):
        data = {"refresh": self.refresh_token}
        response = self.client.post(self.refresh_view_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)  
