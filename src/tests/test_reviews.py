# import unittest
# from main import create_app, db


# class TestBlogs(unittest.TestCase):
#     @classmethod
#     def setUp(cls):
#         cls.app = create_app()
#         cls.app_context = cls.app.app_context()
#         cls.app_context.push()
#         cls.client = cls.app.test_client()
#         db.create_all()

#         runner = cls.app.test_cli_runner()
#         result = runner.invoke(args=["db-custom", "seed"])
#         if result.exit_code != 0:
#             raise ValueError(result.stdout)

#     @classmethod
#     def tearDown(cls):
#         db.session.remove()
#         db.drop_all()
#         cls.app_context.pop()

#     def test_all_reviews(self):
#         response = self.client.get("/reviews/")
#         data = response.get_json()

#         self.assertEqual(response.status_code, 200)
#         self.assertIsInstance(data, list)
#         self.assertTrue(len(data) == 10)

#     def test_review_show(self):
#         response = self.client.get("/reviews/1")
#         data = response.get_json()

#         self.assertEqual(response.status_code, 200)
#         self.assertIsInstance(data, dict)
#         self.assertTrue(len(data) == 9)

#     def test_new_review(self):
#         response = self.client.post("/reviews/new_review", data={
#             "title": "Review 11",
#             "location": "Sydney, Australia",
#             "date": "2020-11-25",
#             "category": "Adventure",
#             "activity_type": "Bridge Climb",
#             "rating": "4",
#             "description": "Curabitur viverra cursus convallis..."
#         })
#         data = response.get_json()

#         self.assertEqual(response.status_code, 200)
#         self.assertIsInstance(data, dict)
#         self.assertTrue(data["location"] == "Sydney, Australia")
#         self.assertTrue(len(data) == 9)

#     def test_review_update(self):
#         response = self.client.put("/reviews/2", data={
#             "activity_type": "hiking",
#             "date": "2020-11-15"
#         })
#         data = response.get_json()

#         self.assertEqual(response.status_code, 200)
#         self.assertIsInstance(data, dict)
#         self.assertTrue(data["activity_type"] == "hiking")
#         self.assertTrue(data["date"] == "2020-11-15")

#     def test_delete_review(self):
#         self.client.delete("/reviews/3")
#         self.client.delete("/reviews/4")
#         response = self.client.get("/reviews/")
#         data = response.get_json()

#         reviewids = []
#         for entry in data:
#             reviewids.append(entry["reviewid"])

#         self.assertIsInstance(data, list)
#         self.assertTrue(len(data) == 8)
#         self.assertNotIn([3, 4], reviewids)
