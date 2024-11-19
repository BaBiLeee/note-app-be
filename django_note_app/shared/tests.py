from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from user.models import User
from note.models import Note
from shared.models import Shared

class SharedViewSetTest(TestCase):
    def setUp(self):
        # Tạo người dùng
        self.owner = User.objects.create_user(fullname="owner", email="a@gmail.com", password="owner123")
        self.shared_user = User.objects.create_user(fullname="shared_user", email="b@gmail.com", password="shared123")
        self.other_user = User.objects.create_user(fullname="other_user", email="c@gmail.com", password="other123")

        # Tạo ghi chú
        self.note = Note.objects.create(
            user=self.owner,
            type="Personal",
            title="Test Note",
            content="This is a test note.",
            color="bg-blue-200"
        )

        # Tạo bản ghi Shared
        self.shared_note = Shared.objects.create(
            note=self.note,
            owner=self.owner,
            shared_by=self.owner,
            shared_user=self.shared_user,
            permission=Shared.VIEW | Shared.EDIT
        )

        # API Client để test
        self.client = APIClient()

    def authenticate_user(self, user):
        """Xác thực người dùng."""
        self.client.force_authenticate(user=user)

    def test_list_shared_notes(self):
        """Kiểm tra danh sách các ghi chú được chia sẻ."""
        self.authenticate_user(self.shared_user)
        response = self.client.get("/shared/")  # Endpoint list shared notes
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["note"], self.note.id)

    # def test_retrieve_shared_note_success(self):
    #     """Kiểm tra lấy chi tiết ghi chú được chia sẻ thành công."""
    #     self.authenticate_user(self.shared_user)
    #     response = self.client.get(f"/shared/{self.note.id}/")  # Endpoint retrieve
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data["note"], self.note.id)

    # def test_retrieve_shared_note_no_permission(self):
    #     """Kiểm tra lấy chi tiết ghi chú mà không có quyền truy cập."""
    #     self.authenticate_user(self.other_user)
    #     response = self.client.get(f"/shared/{self.note.id}/")
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_create_shared_note_success(self):
    #     """Kiểm tra tạo bản ghi chia sẻ thành công."""
    #     self.authenticate_user(self.owner)
    #     data = {
    #         "note": self.note.id,
    #         "owner": self.owner.id,
    #         "shared_by": self.owner.id,
    #         "shared_user": self.other_user.id,
    #         "permission": Shared.VIEW,
    #     }
    #     response = self.client.post("/shared/", data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.data["note"], self.note.id)
    #     self.assertEqual(response.data["shared_user"], self.other_user.id)

    # def test_update_shared_note_success(self):
    #     """Kiểm tra cập nhật quyền chia sẻ của ghi chú thành công."""
    #     self.authenticate_user(self.owner)
    #     data = {
    #         "permission": Shared.VIEW | Shared.DELETE,
    #     }
    #     response = self.client.patch(f"/shared/{self.note.id}/", data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.shared_note.refresh_from_db()
    #     self.assertEqual(self.shared_note.permission, Shared.VIEW | Shared.DELETE)

    # def test_update_shared_note_no_permission(self):
    #     """Kiểm tra cập nhật ghi chú chia sẻ mà không có quyền."""
    #     self.authenticate_user(self.shared_user)
    #     data = {
    #         "permission": Shared.VIEW | Shared.DELETE,
    #     }
    #     response = self.client.patch(f"/shared/{self.note.id}/", data)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
