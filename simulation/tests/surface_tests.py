from unittest import TestCase
from simulation.network import Surface, Frame, Empty


class TestSurface(TestCase):
    def setUp(self):
        self.surface = [
            [2, 2, 2, 1, 0, 1],
            [2, 0, 0, 0, 0, 2],
            [2, 1, 2, 2, 2, 2]
        ]
        self.mapped_surface = Surface(self.surface)

    def test_if_all_slots_created(self):
        slots_number = len(self.mapped_surface.entry_points)
        self.assertEqual(slots_number, 3)

    def test_if_frame_visits_all_empty_cells(self):
        test_frame = Frame(1, 1)
        for row in self.mapped_surface.surface:
            for tile in row:
                if isinstance(tile, Empty):
                    tile.last_received_frame_id = -10
        self.mapped_surface.entry_points[0].content = test_frame
        self.mapped_surface.entry_points[0].propagate()
        for row in self.mapped_surface.surface:
            for tile in row:
                if isinstance(tile, Empty):
                    with self.subTest(tile):
                        self.assertNotEqual(tile.last_received_frame_id, -10)
