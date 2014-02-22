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
        self.app.post('/api/dimmer/warm_white', data=json.dumps({'value': 120}), content_type='application/json')
        time.sleep(5)
        p = self.app.post('/api/power', data=json.dumps({'power_state': 0}), content_type='application/json')
        self.assertDictEqual(json.loads(p.data), {u'blue': 0,
                                                  u'color_pattern': u'0000000000000000000000000000000000000000000000000000000000000000',
                                                  u'cool': 0,
                                                  u'green': 0,
                                                  u'red': 0,
                                                  u'warm': 120})
        time.sleep(5)
        p = self.app.post('/api/power', data=json.dumps({'power_state': 1}), content_type='application/json')
        time.sleep(5)
        self.assertDictEqual(json.loads(p.data), {u'blue': 0,
                                                  u'color_pattern': u'0000000000000000000000000000000000000000000000000000000000000000',
                                                  u'cool': 0,
                                                  u'green': 0,
                                                  u'red': 0,
                                                  u'warm': 120})

    def test_integration(self):
        self.app.post('/api/dimmer/warm_white', data=json.dumps({'value': -256}), content_type='application/json')
        self.app.post('/api/dimmer/cool_white', data=json.dumps({'value': 256}), content_type='application/json')
        for _ in xrange(256):
            self.app.post('/api/dimmer/warm_white', data=json.dumps({'value': 8}), content_type='application/json')
            self.app.post('/api/dimmer/cool_white', data=json.dumps({'value': -8}), content_type='application/json')
            time.sleep(0.5)



    def test_warm(self):
        time.sleep(10)
        p = self.app.post('/api/dimmer/warm_white', data=json.dumps({'value': 500}), content_type='application/json')
        print p
        time.sleep(3)
        self.assertDictEqual(json.loads(p.data), {u'blue': 0,
                                                  u'color_pattern': u'0000000000000000000000000000000000000000000000000000000000000000',
                                                  u'cool': 0,
                                                  u'green': 0,
                                                  u'red': 0,
                                                  u'warm': 255})
        p = self.app.post('/api/dimmer/warm_white', data=json.dumps({'value': -64}), content_type='application/json')
        time.sleep(3)
        self.assertDictEqual(json.loads(p.data), {u'blue': 0,
                                                  u'color_pattern': u'0000000000000000000000000000000000000000000000000000000000000000',
                                                  u'cool': 0,
                                                  u'green': 0,
                                                  u'red': 0,
                                                  u'warm': 191})
        p = self.app.post('/api/dimmer/warm_white', data=json.dumps({'value': -64}), content_type='application/json')
        time.sleep(3)
        self.assertDictEqual(json.loads(p.data), {u'blue': 0,
                                                  u'color_pattern': u'0000000000000000000000000000000000000000000000000000000000000000',
                                                  u'cool': 0,
                                                  u'green': 0,
                                                  u'red': 0,
                                                  u'warm': 127})
        p = self.app.post('/api/dimmer/warm_white', data=json.dumps({'value': -64}), content_type='application/json')
        time.sleep(3)
        self.assertDictEqual(json.loads(p.data), {u'blue': 0,
                                                  u'color_pattern': u'0000000000000000000000000000000000000000000000000000000000000000',
                                                  u'cool': 0,
                                                  u'green': 0,
                                                  u'red': 0,
                                                  u'warm': 63})
        p = self.app.post('/api/dimmer/warm_white', data=json.dumps({'value': -64}), content_type='application/json')
        time.sleep(3)
        self.assertDictEqual(json.loads(p.data), {u'blue': 0,
                                                  u'color_pattern': u'0000000000000000000000000000000000000000000000000000000000000000',
                                                  u'cool': 0,
                                                  u'green': 0,
                                                  u'red': 0,
                                                  u'warm': 0})

    def test_cool(self):
        time.sleep(10)
        p = self.app.post('/api/dimmer/cool_white', data=json.dumps({'value': 500}), content_type='application/json')
        print p
        time.sleep(3)
        self.assertDictEqual(json.loads(p.data), {u'blue': 0,
                                                  u'color_pattern': u'0000000000000000000000000000000000000000000000000000000000000000',
                                                  u'cool': 255,
                                                  u'green': 0,
                                                  u'red': 0,
                                                  u'warm': 0})
        p = self.app.post('/api/dimmer/cool_white', data=json.dumps({'value': -64}), content_type='application/json')
        time.sleep(3)
        self.assertDictEqual(json.loads(p.data), {u'blue': 0,
                                                  u'color_pattern': u'0000000000000000000000000000000000000000000000000000000000000000',
                                                  u'cool': 191,
                                                  u'green': 0,
                                                  u'red': 0,
                                                  u'warm': 0})
        p = self.app.post('/api/dimmer/cool_white', data=json.dumps({'value': -64}), content_type='application/json')
        time.sleep(3)
        self.assertDictEqual(json.loads(p.data), {u'blue': 0,
                                                  u'color_pattern': u'0000000000000000000000000000000000000000000000000000000000000000',
                                                  u'cool': 127,
                                                  u'green': 0,
                                                  u'red': 0,
                                                  u'warm': 0})
        p = self.app.post('/api/dimmer/cool_white', data=json.dumps({'value': -64}), content_type='application/json')
        time.sleep(3)
        self.assertDictEqual(json.loads(p.data), {u'blue': 0,
                                                  u'color_pattern': u'0000000000000000000000000000000000000000000000000000000000000000',
                                                  u'cool': 63,
                                                  u'green': 0,
                                                  u'red': 0,
                                                  u'warm': 0})
        p = self.app.post('/api/dimmer/cool_white', data=json.dumps({'value': -64}), content_type='application/json')
        time.sleep(3)
        self.assertDictEqual(json.loads(p.data), {u'blue': 0,
                                                  u'color_pattern': u'0000000000000000000000000000000000000000000000000000000000000000',
                                                  u'cool': 0,
                                                  u'green': 0,
                                                  u'red': 0,
                                                  u'warm': 0})


if __name__ == '__main__':
    unittest.main()
