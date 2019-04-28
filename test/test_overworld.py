import os
import sys
import unittest

from HonestQuest.overworld import overworld

sys.stdout = open(os.devnull, "w")


WORLD = overworld.OverWorld(4, 5)


class TestWorld(unittest.TestCase):
    def test_rendered_world(self):
        f = "{} . . . .\n. . . . .\n. . {} . .\n. . . . ."
        expected = f.format(u"\U0001F6B6", u"\u2302")
        render = WORLD.field.render_field()
        self.assertTrue(expected, render)

    def test_move_down(self):
        x = WORLD.field.x
        WORLD.key_press.direction = "s"
        WORLD.move_hero()
        self.assertEqual(WORLD.field.x, x + 1)

    def test_move_up(self):
        WORLD.field.x = 2
        x = WORLD.field.x
        WORLD.key_press.direction = "w"
        WORLD.move_hero()
        self.assertEqual(WORLD.field.x, x - 1)

    def test_move_right(self):
        y = WORLD.field.y
        WORLD.key_press.direction = "d"
        WORLD.move_hero()
        self.assertEqual(WORLD.field.y, y + 1)

    def test_move_left(self):
        WORLD.field.y = 2
        y = WORLD.field.y
        WORLD.key_press.direction = "a"
        WORLD.move_hero()
        self.assertEqual(WORLD.field.y, y - 1)


if __name__ == "__main__":
    unittest.main()
