import importlib.util
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "render-check.py"
SPEC = importlib.util.spec_from_file_location("wireframe_render_check", MODULE)
render = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(render)


class GeometryTest(unittest.TestCase):
    def test_intersection_requires_positive_area(self):
        a = {"left": 0, "right": 10, "top": 0, "bottom": 10}
        touching = {"left": 10, "right": 20, "top": 0, "bottom": 10}
        overlap = {"left": 9, "right": 20, "top": 0, "bottom": 10}
        self.assertFalse(render.intersects(a, touching))
        self.assertTrue(render.intersects(a, overlap))

    def test_inside_allows_one_pixel_tolerance(self):
        outer = {"left": 0, "right": 100, "top": 0, "bottom": 100}
        self.assertTrue(render.inside({"left": -0.5, "right": 100.5, "top": 0, "bottom": 100}, outer))
        self.assertFalse(render.inside({"left": -2, "right": 100, "top": 0, "bottom": 100}, outer))


if __name__ == "__main__":
    unittest.main()
