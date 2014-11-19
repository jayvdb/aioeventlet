import datetime
import eventlet
import tests

class TimerTests(tests.TestCase):
    def test_display_date(self):
        result = []
        delay = 0.050
        count = 3

        def display_date(end_time, loop):
            result.append(datetime.datetime.now())
            if (loop.time() + delay) < end_time:
                loop.call_later(delay, display_date, end_time, loop)
            else:
                loop.stop()

        end_time = self.loop.time() + delay * count
        self.loop.call_soon(display_date, end_time, self.loop)
        self.loop.run_forever()

        self.assertEqual(len(result), count, result)

    def test_later_stop_later(self):
        result = []

        def hello():
            result.append("Hello")

        def world(loop):
            result.append("World")
            loop.stop()

        self.loop.call_later(0.010, hello)
        self.loop.call_later(0.020, self.loop.stop)
        self.loop.call_later(0.030, world, self.loop)
        self.loop.run_forever()

        eventlet.sleep(0.050)
        self.assertEqual(result, ["Hello"])

        self.loop.run_forever()
        self.assertEqual(result, ["Hello", "World"])
