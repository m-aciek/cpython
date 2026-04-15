import turtle
import unittest


class TestRecordingBackend(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.turtle = turtle

    def _new_turtle(self):
        backend = self.turtle._RecordingTurtleBackend(width=200, height=200)
        screen = self.turtle.TurtleScreen._from_backend(backend)
        t = self.turtle.RawTurtle(screen)
        backend.operations.clear()
        return t, backend

    def test_forward_turn_records_polyline_updates(self):
        t, backend = self._new_turtle()
        t.pencolor("red")
        t.pensize(3)
        t.forward(10)
        t.left(90)
        t.forward(5)

        line = backend.items[t.currentLineItem]
        self.assertEqual(line["type"], "line")
        self.assertEqual(line["points"], [(0.0, -0.0), (10.0, -0.0), (10.0, -5.0)])
        self.assertEqual(line["style"]["fill"], "red")
        self.assertEqual(line["style"]["width"], 3)

    def test_penup_pendown_starts_new_segment(self):
        t, backend = self._new_turtle()
        t.penup()
        t.forward(20)
        t.pendown()
        t.forward(10)

        line = backend.items[t.currentLineItem]
        self.assertEqual(line["points"], [(20.0, -0.0), (30.0, -0.0)])

    def test_begin_fill_end_fill_records_polygon(self):
        t, backend = self._new_turtle()
        t.fillcolor("blue")
        t.begin_fill()
        for _ in range(4):
            t.forward(10)
            t.left(90)
        t.end_fill()

        polygon_items = [item for item in backend.items.values() if item["type"] == "polygon"]
        self.assertTrue(polygon_items)
        fill_polygon = polygon_items[-1]
        self.assertEqual(fill_polygon["style"]["fill"], "blue")
        self.assertIn("outline", fill_polygon["style"])
        self.assertEqual(len(fill_polygon["points"]), 5)


if __name__ == "__main__":
    unittest.main()
