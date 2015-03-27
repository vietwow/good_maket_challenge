from tests import ClientTest, expect
from model import *
import json

class UserApiTest(ClientTest):

    def setUp(self):
        self.user = User.create(email='test@gmail.com', password='123456', token='tokentoken')
        pass

    def tearDown(self):
        # Category.objects.delete()
        User.delete().where(User.id == self.user.id).execute()
        pass

    def test_user_list_should_return_status_200(self):
        resp = self.get('/api/v1/users/')
        expect(resp.status_int).to_equal(200)

    def test_after_create_user_api_should_return_status_200(self):
        resp = self.get('/api/v1/users/' + str(self.user.id))
        expect(resp.status_int).to_equal(200)

    def test_after_create_user_api_should_return_correct_data(self):
        resp = self.get('/api/v1/users/' + str(self.user.id))
        expect(resp.body).to_include(self.user.email)

