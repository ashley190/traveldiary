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

    def test_all_reviews(self):
        response = self.client.get("/reviews/")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) == 30)

    def test_review_show(self):
        response = self.client.get("/reviews/1")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertTrue(len(data) == 10)

    def test_new_review(self):
        response = self.client.post(
            "/reviews/new_review",
            headers=self.headers["test1"],
            data={
                "title": "Review 11",
                "location": "Sydney, Australia",
                "date": "2020-11-25",
                "category": "Adventure",
                "activity_type": "Bridge Climb",
                "rating": "4",
                "description": "Curabitur viverra cursus convallis..."
            })
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
        self.assertTrue(data["location"] == "Sydney, Australia")
        self.assertTrue(len(data) == 10)

    def test_review_update(self):
        import random
        all_reviews = self.client.get("/reviews/").get_json()
        test_1_reviewids = []
        for review in all_reviews:
            if review["user"]["userid"] == 1:
                test_1_reviewids.append(review["reviewid"])
        non_test_1_reviewids = [
            i for i in range(1, 31) if i not in test_1_reviewids]
        test_1_reviewid = random.choice(test_1_reviewids)
        non_test_1_reviewid = random.choice(non_test_1_reviewids)

        response_1 = self.client.put(
            f"/reviews/{test_1_reviewid}",
            headers=self.headers["test1"],
            data={
                "activity_type": "hiking",
                "date": "2020-11-15",
                "title": "Updated review v2"
            }
        )
        data_1 = response_1.get_json()

        self.assertEqual(response_1.status_code, 200)
        self.assertIsInstance(data_1, dict)
        self.assertTrue(data_1["activity_type"] == "hiking")
        self.assertTrue(data_1["date"] == "2020-11-15")
        self.assertTrue(data_1["title"] == "Updated review v2")
        self.assertTrue(data_1["user"]["userid"] == 1)

        response_2 = self.client.put(
            f"/reviews/{non_test_1_reviewid}",
            headers=self.headers["test1"],
            data={
                "activity_type": "sightseeing",
                "category": "museums",
                "title": "Review v3"
            }
        )
        data_2 = response_2.get_json()

        self.assertEqual(response_2.status_code, 401)
        self.assertFalse(data_2)

    def test_delete_review(self):
        import random
        all_reviews = self.client.get("/reviews/").get_json()
        test_4_reviewids = []
        for review in all_reviews:
            if review["user"]["userid"] == 4:
                test_4_reviewids.append(review["reviewid"])
        non_test_4_reviewids = [
            i for i in range(1, 31) if i not in test_4_reviewids]
        test_4_reviewid = random.choice(test_4_reviewids)
        non_test_4_reviewid = random.choice(non_test_4_reviewids)

        response_1 = self.client.delete(
            f"/reviews/{test_4_reviewid}",
            headers=self.headers["test4"]
        )
        data_1 = response_1.get_json()

        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(data_1["reviewid"], test_4_reviewid)

        response_2 = self.client.delete(
            f"/reviews/{non_test_4_reviewid}",
            headers=self.headers["test4"]
        )
        data_2 = response_2.get_json()

        self.assertEqual(response_2.status_code, 400)
        self.assertFalse(data_2)

        remaining_reviews = self.client.get("/reviews/").get_json()
        remaining_reviewids = [
            review["reviewid"] for review in remaining_reviews]

        self.assertTrue(test_4_reviewid not in remaining_reviewids)
