import unittest
import requests
import time, uuid

BASE = "http://localhost:8003"
HEADERS = {"Content-Type": "application/json"}

USER = f"Ruth_{int(time.time())}_{uuid.uuid4().hex[:6]}"
PASS = "Secret123"

class TestAuthAPI(unittest.TestCase):
    token = None  # class var

    @classmethod
    def setUpClass(cls):
        r = requests.post(f"{BASE}/auth/signup", json={"userId": USER, "password": PASS}, headers=HEADERS)
        if r.status_code == 200:
            cls.token = r.json()["access_token"]
        elif r.status_code == 409:
            r = requests.post(f"{BASE}/auth/login", json={"userId": USER, "password": PASS}, headers=HEADERS)
            r.raise_for_status()
            cls.token = r.json()["access_token"]
        else:
            raise AssertionError(f"Cannot obtain token: {r.status_code} {r.text}")

    def setUp(self):
        # ודא שתמיד יש token גם באובייקט וגם במחלקה
        if not getattr(type(self), "token", None):
            r = requests.post(f"{BASE}/auth/login", json={"userId": USER, "password": PASS}, headers=HEADERS)
            r.raise_for_status()
            type(self).token = r.json()["access_token"]
        self.token = type(self).token

    def test_1_signup_success(self):
        r = requests.post(f"{BASE}/auth/signup", json={"userId": USER, "password": PASS}, headers=HEADERS)
        self.assertEqual(r.status_code, 409, r.text)

    def test_2_login_success(self):
        r = requests.post(f"{BASE}/auth/login", json={"userId": USER, "password": PASS}, headers=HEADERS)
        self.assertEqual(r.status_code, 200, r.text)
        type(self).token = r.json()["access_token"]
        self.token = type(self).token

    def test_3_login_wrong_password(self):
        r = requests.post(f"{BASE}/auth/login", json={"userId": USER, "password": "Wrong"}, headers=HEADERS)
        self.assertEqual(r.status_code, 401, r.text)

    def test_4_get_indexes_requires_token(self):
        r = requests.get(f"{BASE}/auth/indexes")
        self.assertEqual(r.status_code, 401, r.text)

    def test_5_get_indexes_success(self):
        r = requests.get(f"{BASE}/auth/indexes", headers={"Authorization": f"Bearer {self.token}"})
        self.assertEqual(r.status_code, 200, r.text)
        self.assertIn("indexs", r.json())

    def test_6_add_index(self):
        r = requests.post(
            f"{BASE}/auth/indexes/add",
            headers={"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"},
            json={"index": "my-notes"},
        )
        self.assertEqual(r.status_code, 200, r.text)
        self.assertIn("my-notes", r.json()["user"]["indexs"])

    def test_7_remove_index(self):
        r = requests.post(
            f"{BASE}/auth/indexes/remove",
            headers={"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"},
            json={"index": "my-notes"},
        )
        self.assertEqual(r.status_code, 200, r.text)
        self.assertNotIn("my-notes", r.json()["user"]["indexs"])

    def test_8_invalid_token(self):
        r = requests.get(f"{BASE}/auth/indexes", headers={"Authorization": "Bearer BADTOKEN"})
        self.assertEqual(r.status_code, 401, r.text)

    def test_9_add_index_blank(self):
        r = requests.post(
            f"{BASE}/auth/indexes/add",
            headers={"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"},
            json={"index": "   "},
        )
        self.assertIn(r.status_code, [400, 422], r.text)

    def test_10_add_index_blank(self):
        r = requests.post(
            f"{BASE}/auth/indexes/add",
            headers={"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"},
            json={"index": ""},
        )
        self.assertIn(r.status_code, [400, 422], r.text)

if __name__ == "__main__":
    unittest.main()
