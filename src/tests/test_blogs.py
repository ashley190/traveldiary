import unittest
from main import create_app, db


class TestBlogs(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()
        db.create_all()

        runner = cls.app.test_cli_runner()
        result = runner.invoke(args=["db-custom", "seed"])
        if result.exit_code != 0:
            raise ValueError(result.stdout)

        cls.headers = {}
        for i in range(1, 6):
            cls.login = cls.client.post(
                "user/login",
                json={
                    "email": f"test{i}@test.com",
                    "password": "123456"
                }
            )
            cls.token = cls.login.get_json()["token"]
            cls.header = {"Authorization": f"Bearer {cls.token}"}
            cls.headers[f"test{i}"] = cls.header

    @classmethod
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_blog_index(self):
        response = self.client.get("/blogs/", headers=self.headers["test1"])
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_blog_post(self):
        import random
        test_1_blogs = self.client.get(
            "/blogs/", headers=self.headers["test1"]).get_json()
        test_2_blogs = self.client.get(
            "/blogs/", headers=self.headers["test2"]).get_json()
        test_1_blog = random.choice(test_1_blogs)["blogid"]
        test_2_blog = random.choice(test_2_blogs)["blogid"]

        response_1 = self.client.get(
            f"/blogs/{test_1_blog}", headers=self.headers["test1"])
        data_1 = response_1.get_json()

        self.assertEqual(response_1.status_code, 200)
        self.assertIsInstance(data_1, dict)
        self.assertTrue(len(data_1) == 6)
        self.assertTrue(data_1["user"]["userid"] == 1)

        response_2 = self.client.get(
            f"/blogs/{test_2_blog}", headers=self.headers["test2"])
        data_2 = response_2.get_json()

        self.assertEqual(response_2.status_code, 200)
        self.assertIsInstance(data_2, dict)
        self.assertTrue(len(data_2) == 6)
        self.assertTrue(data_2["user"]["userid"] == 2)

    def test_blog_create(self):
        response = self.client.post(
            "/blogs/", headers=self.headers["test3"], data={
                "title": "TestBlog123",
                "date": "2020-11-11",
                "location": "Melbourne, Australia",
                "blog": "Lorem ipsum dolor sit amet..."
            })
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertTrue(data["title"] == "TestBlog123")
        self.assertTrue(data["location"] == "Melbourne, Australia")
        self.assertTrue(len(data) == 6)
        self.assertTrue(data["user"]["userid"] == 3)

    def test_blog_update(self):
        import random
        test_4_blogs = self.client.get(
            "/blogs/", headers=self.headers["test4"]).get_json()
        test_4_blog = random.choice(test_4_blogs)["blogid"]

        response = self.client.put(
            f"/blogs/{test_4_blog}", headers=self.headers["test4"], data={
                "title": "UpdatedBlog123",
                "location": "Sydney, Australia"
            })
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertTrue(data["title"] == "UpdatedBlog123")
        self.assertTrue(data["location"] == "Sydney, Australia")

    def test_blog_delete(self):
        import random
        test_5_blogs = self.client.get(
            "/blogs/", headers=self.headers["test5"]).get_json()
        test_5_blogids = [blog["blogid"] for blog in test_5_blogs]
        non_test_5_blogids = [
            i for i in range(1, 31) if i not in test_5_blogids]
        test_5_blogid = random.choice(test_5_blogids)

        response_1 = self.client.delete(
            f"/blogs/{test_5_blogid}", headers=self.headers["test5"])
        data_1 = response_1.get_json()

        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(data_1["blogid"], test_5_blogid)

        response_2 = self.client.delete(
            f"/blogs/{test_5_blogid}", headers=self.headers["test4"])
        data_2 = response_2.get_json()

        self.assertEqual(response_2.status_code, 400)
        self.assertFalse(data_2)

        response_3 = self.client.get("/blogs/", headers=self.headers["test5"])
        data_3 = response_3.get_json()
        remaining_blogids = [blog["blogid"] for blog in data_3]

        self.assertTrue(test_5_blogid not in remaining_blogids)
        self.assertTrue(test_5_blogid not in non_test_5_blogids)
