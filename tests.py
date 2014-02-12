import os
import meetup_slides
import unittest
import tempfile
from mockredis import mock_redis_client
from mock import patch

@patch('redis.Redis', mock_redis_client)
class MeetupSlidesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = meetup_slides.app.test_client()

    def tearDown(self):
        pass
        
    def test_add_meetup(self):
        rv = self.app.post('/meetup/add', data=dict(
        meetup_name='python',
        meetup_city='San Francisco',
        desc='description',
        website='http://www.meetupslides.com',
        ajax=1,
    ), follow_redirects=True)
        assert 'python' in rv.data
        assert 'San Francisco' in rv.data

if __name__ == '__main__':
    unittest.main()