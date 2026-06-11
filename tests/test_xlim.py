import unittest

import matplotlib

matplotlib.use("Agg")  # Non-interactive backend for headless testing

import matplotlib.pyplot as plt

from energydiagram import ED


class TestXlim(unittest.TestCase):
    def test_xlim_is_stored(self):
        ed = ED(xlim=(0, 10))
        self.assertEqual(ed.xlim, (0, 10))

    def test_plot_with_xlim(self):
        ed = ED(xlim=(0, 10))
        ed.add_level(0, "Reactant")
        ed.add_level(5, "TS")
        ed.add_level(2, "Product")
        ed.add_link(0, 1)
        ed.add_link(1, 2)
        fig, ax = plt.subplots()
        try:
            ed.plot(ax=ax)
        except Exception as e:
            self.fail(f"plot() raised {e}")
        self.assertEqual(ax.get_xlim(), (0.0, 10.0))
        plt.close(fig)

    def test_plot_without_xlim(self):
        ed = ED()
        ed.add_level(0, "Reactant")
        ed.add_level(5, "TS")
        ed.add_level(2, "Product")
        ed.add_link(0, 1)
        ed.add_link(1, 2)
        try:
            ed.plot()
        except Exception as e:
            self.fail(f"plot() raised {e}")

    def test_position_last_with_xlim(self):
        ed = ED(xlim=(0, 12))
        ed.add_level(0, "A")
        ed.add_level(3, "B", position="last")
        ed.add_level(5, "C")
        ed.add_level(2, "D", position="last")
        ed.add_level(-1, "E")
        fig, ax = plt.subplots()
        try:
            ed.plot(ax=ax)
        except Exception as e:
            self.fail(f"plot() raised {e}")
        plt.close(fig)


if __name__ == "__main__":
    unittest.main()
