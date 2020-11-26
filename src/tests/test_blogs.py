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

    # def test_blog_post(self):
    #     response = self.client.get("/blogs/1")
    #     data = response.get_json()

    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(data, dict)
    #     self.assertTrue(len(data) == 5)

    # def test_blog_create(self):
    #     response = self.client.post("/blogs/", data={
    #         "title": "TestBlog123",
    #         "date": "2020-11-11",
    #         "location": "Melbourne, Australia",
    #         "blog": "Lorem ipsum dolor sit amet..."
    #     })
    #     data = response.get_json()

    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(data, dict)
    #     self.assertTrue(data["title"] == "TestBlog123")
    #     self.assertTrue(len(data) == 5)

    # def test_blog_update(self):
    #     response = self.client.put("/blogs/1", data={
    #         "title": "UpdatedBlog123",
    #         "location": "Sydney, Australia"
    #     })
    #     data = response.get_json()

    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(data, dict)
    #     self.assertTrue(data["title"] == "UpdatedBlog123")
    #     self.assertTrue(data["location"] == "Sydney, Australia")

    # def test_blog_delete(self):
    #     self.client.delete("/blogs/1")
    #     self.client.delete("/blogs/2")
    #     response = self.client.get("/blogs/")

    #     data = response.get_json()
    #     blogids = []
    #     for entry in data:
    #         blogids.append(entry["blogid"])

    #     self.assertIsInstance(data, list)
    #     self.assertTrue(len(data) == 8)
    #     self.assertNotIn([1, 2], blogids)
