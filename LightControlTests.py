__author__ = 'galron'

import json
import time
import unittest

import LightControl


class LightControlTester(unittest.TestCase):
    def setUp(self):
        self.app = LightControl.app.test_client()

    def tearDown(self):
        pass

    def test_power(self):
        p = self.app.post('/api/power', data=json.dumps({'power_state': 1}), content_type='application/json')
        self.assertDictEqual(json.loads(p.data), {"power": 1, "state_did_change": True})
        time.sleep(10)
        p = self.app.post('/api/power', data=json.dumps({'power_state': 0}), content_type='application/json')
        self.assertDictEqual(json.loads(p.data), {"power": 0, "state_did_change": True})

if __name__ == '__main__':
    unittest.main()
