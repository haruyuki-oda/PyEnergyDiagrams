# -*- coding: utf-8 -*-
r"""
Created on Mon Jan 23 13:09:19 2017

--- Energy profile diagram---
This is a simple script to plot energy profile diagram using matplotlib.
E|          4__
n|   2__    /  \
e|1__/  \__/5   \
r|  3\__/       6\__
g|
y|
@author: Giacomo Marchioro giacomomarchioro@outlook.com

"""

from typing import Optional, Union, Tuple, Any, List
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from .box_notation import plot_orbital_boxes


class ED:
    # Class constants
    GOLDEN_RATIO: float = 1.6181
    DEFAULT_OFFSET_RATIO: float = 0.02
    DEFAULT_ARROW_WIDTH: float = 20.0
    DIMENSION_RATIO: float = 0.5
    SPACE_RATIO: float = 0.5
    XLIM_DIMENSION_RATIO: float = 0.6
    XLIM_SPACE_RATIO: float = 0.4

    def __init__(self, aspect: Union[str, float] = "auto", xlim: Optional[Tuple[float, float]] = (0, 10)) -> None:
        # plot parameters
        self.ratio = self.GOLDEN_RATIO
        self.dimension = "auto"
        self.space = "auto"
        self.offset = "auto"
        self.offset_ratio = self.DEFAULT_OFFSET_RATIO
        self.color_bottom_text = "blue"
        self.color_top_text = "k"
        self.aspect = aspect
        self.xlim = xlim
        self.round_energies_at_digit = "keep all digits"
        self.top_text_fontsize = "medium"
        self.bottom_text_fontsize = "medium"
        self.right_text_fontsize = "medium"
        self.left_text_fontsize = "medium"
        # data
        self.pos_number = 0
        self.energies = []
        self.positions = []
        self.top_texts = []
        self.bottom_texts = []
        self.left_texts = []
        self.right_texts = []
        self.links = []
        self.arrows = []
        self.electrons_boxes = []
        self.level_kwargs = []
        # matplotlib figure handlers
        self.fig = None
        self.ax = None

    def add_level(
        self,
        energy: float,
        bottom_text: str = "",
        position: Optional[Union[int, float, str]] = None,
        top_text: Optional[Union[str, float]] = None,
        right_text: str = "",
        left_text: str = "",
        color: str = "k",
        linewidth: float = 2,
        **kwargs: Any,
    ) -> None:
        """
        Method of ED class
        This method add a new energy level to the plot.

        Parameters
        ----------
        energy : int
                 The energy of the level in Kcal mol-1
        bottom_text  : str
                The text on the bottom of the level (label of the level)
                (default '')
        position  : str
                The position of the level in the plot. Keep it empty to add
                the level on the right of the previous level use 'last' as
                argument for adding the level to the last position used
                for the level before.
                An integer can be used for adding the level to an arbitrary
                position.
                (default  None)
        color  : str
                Color of the level  (default  'k')
        top_text  : str
                Text on the top of the level. By default it will print the
                energy of the level. (default  'Energy')
        right_text  : str
                Text at the right of the level. (default  '')
        left_text  : str
                Text at the left of the level. (default  '')
        linestyle  : str
                The linestyle of the level, one of the following values:
                'solid', 'dashed', 'dashdot', 'dotted' (default  'solid')




        Returns
        -------
        Append to the class data all the information regarding the level added
        """

        if position is None:
            position = self.pos_number + 1 - 0.75
            self.pos_number += 1
        elif isinstance(position, (int, float)):
            pass
        elif position == "last" or position == "l":
            position = self.pos_number - 0.75
        else:
            raise ValueError(
                "Position must be None or 'last' (abrv. 'l') or in case an integer or float specifing the position. It was: %s"
                % position
            )
        if top_text is None:
            if self.round_energies_at_digit == "keep all digits":
                top_text = energy
            else:
                top_text = round(energy, self.round_energies_at_digit)

        self.energies.append(energy)
        self.positions.append(position)
        self.top_texts.append(top_text)
        self.bottom_texts.append(bottom_text)
        self.left_texts.append(left_text)
        self.right_texts.append(right_text)
        kwargs["color"] = color
        kwargs["linewidth"] = linewidth
        self.level_kwargs.append(kwargs)

        self.links.append([])
        self.arrows.append([])

    def add_arrow(
        self, start_level_id: int, end_level_id: int, position: str = "center",
        text: Optional[Union[str, float]] = None, **kwargs: Any
    ) -> None:
        """
        Method of ED class
        Add a arrow between two energy levels using IDs of the level. Use
        self.plot(show_index=True) to show the IDs of the levels.

        Parameters
        ----------
        start_level_id : int
                 Starting level ID
        end_level_id : int
                 Ending level ID

        Returns
        -------
        Append arrow to self.arrows

        """
        if start_level_id < 0 or start_level_id >= len(self.energies):
            raise IndexError(f"start_level_id {start_level_id} is out of range. Valid range: 0-{len(self.energies)-1}")
        if end_level_id < 0 or end_level_id >= len(self.energies):
            raise IndexError(f"end_level_id {end_level_id} is out of range. Valid range: 0-{len(self.energies)-1}")
        self.arrows[start_level_id].append((end_level_id, position, text, kwargs))

    def add_link(
        self,
        start_level_id: int,
        end_level_id: int,
        line_order: int = 1,
        color: str = "k",
        ls: str = "dashed",
        lw: float = 1.0,
        **kwargs: Any,
    ) -> None:
        """
        Method of ED class
        Add a link between two energy levels using IDs of the level. Use
        self.plot(show_index=True) to show the IDs of the levels.

        Parameters
        ----------
        start_level_id : int
                 Starting level ID
        end_level_id : int
                 Ending level ID
        color : str
                color of the line
        ls : str
                line styple e.g. -- , ..
        linewidth : int
                line width

        Returns
        -------
        Append link to self.links

        """
        if start_level_id < 0 or start_level_id >= len(self.energies):
            raise IndexError(f"start_level_id {start_level_id} is out of range. Valid range: 0-{len(self.energies)-1}")
        if end_level_id < 0 or end_level_id >= len(self.energies):
            raise IndexError(f"end_level_id {end_level_id} is out of range. Valid range: 0-{len(self.energies)-1}")
        kwargs["line_order"] = line_order
        kwargs["color"] = color
        kwargs["ls"] = ls
        kwargs["lw"] = lw
        self.links[start_level_id].append((end_level_id, kwargs))

    def _calculate_x_position(self, position: float) -> float:
        """
        Helper method to calculate x position based on xlim settings.

        Parameters
        ----------
        position : float
            The position index

        Returns
        -------
        float
            The calculated x coordinate
        """
        if self.xlim is not None:
            xmin, _ = self.xlim
            return xmin + position * (self.dimension + self.space)
        else:
            return position * (self.dimension + self.space)

    def add_electronbox(self, level_id: int, boxes: int, electrons: int,
                        side: float = 0.5, spacing_f: int = 5) -> None:
        """
        Method of ED class
        Add electron orbital box notation to an energy level. Use
        self.plot(show_IDs=True) to show the IDs of the levels.

        Parameters
        ----------
        level_id : int
                 The ID of the level to add electron boxes to
        boxes : int
                 Number of orbital boxes to display
        electrons : int
                 Number of electrons to fill in the boxes
        side : float
                 Size of each box (default 0.5)
        spacing_f : int
                 Spacing factor between electron spins (default 5)

        Returns
        -------
        Appends electron box configuration to self.electrons_boxes

        """
        if level_id < 0 or level_id >= len(self.energies):
            raise IndexError(f"level_id {level_id} is out of range. Valid range: 0-{len(self.energies)-1}")
        self.__auto_adjust()
        x = self._calculate_x_position(self.positions[level_id]) + self.dimension * 0.5
        y = self.energies[level_id]
        self.electrons_boxes.append((x, y, boxes, electrons, side, spacing_f))

    def plot_level(self, energy: float, pos: float, btext: str, ttext: Union[str, float],
                   rtext: str, ltext: str, **kwargs: Any) -> None:
        """
        Internal method to plot a single energy level with text labels.

        Parameters
        ----------
        energy : float
            Energy value of the level
        pos : float
            Position index for the level
        btext : str
            Bottom text label
        ttext : Union[str, float]
            Top text label (usually energy value)
        rtext : str
            Right text label
        ltext : str
            Left text label
        **kwargs : Any
            Additional plotting parameters for hlines
        """
        start = self._calculate_x_position(pos)
        self.ax.hlines(energy, start, start + self.dimension, **kwargs)
        # top text
        self.ax.text(
            start + 0.5 * self.dimension,  # X
            energy + self.offset,  # Y
            ttext,  # self.top_texts
            horizontalalignment="center",
            verticalalignment="bottom",
            color=self.color_top_text,
            fontsize=self.top_text_fontsize,
        )
        # bottom text
        self.ax.text(
            start + self.dimension,  # X
            energy,  # Y
            rtext,  # self.right_text
            horizontalalignment="left",
            verticalalignment="center",
            color=self.color_bottom_text,
            fontsize=self.left_text_fontsize,
        )
        # right text
        self.ax.text(
            start,  # X
            energy,  # Y
            ltext,  # self.left_text
            horizontalalignment="right",
            verticalalignment="center",
            color=self.color_bottom_text,
            fontsize=self.right_text_fontsize,
        )
        # left text
        self.ax.text(
            start + 0.5 * self.dimension,  # X
            energy - 2 * self.offset,  # Y
            btext,  # self.bottom_text
            horizontalalignment="center",
            verticalalignment="top",
            color=self.color_bottom_text,
            fontsize=self.bottom_text_fontsize,
        )

    def plot_link(self, idx: int, idy: int, **kwargs: Any) -> None:
        """
        Internal method to plot a link between two energy levels.

        Parameters
        ----------
        idx : int
            Starting level index
        idy : int
            Ending level index
        **kwargs : Any
            Line drawing parameters including line_order, color, ls, lw
        """
        # Calculate positions
        start = self._calculate_x_position(self.positions[idx])
        x1 = start + self.dimension
        x2 = self._calculate_x_position(self.positions[idy])
        y1 = self.energies[idx]
        y2 = self.energies[idy]
        # draw line
        line_order = kwargs.pop("line_order")
        if line_order == 1:
            # straight line
            line = Line2D([x1, x2], [y1, y2], **kwargs)
            self.ax.add_line(line)
        elif line_order == 2:
            # tapered at the top
            curve = PathPatch(
                Path(
                    [(x1, y1), ((x1 + x2) / 2, max(y1, y2)), (x2, y2)],
                    [Path.MOVETO, Path.CURVE3, Path.CURVE3],
                ),
                fc="none",
                **kwargs,
            )
            self.ax.add_patch(curve)
        elif line_order == 3:
            # tapered at bottom and top
            curve = PathPatch(
                Path(
                    [(x1, y1), ((x1 + x2) / 2, y1), ((x1 + x2) / 2, y2), (x2, y2)],
                    [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4],
                ),
                fc="none",
                **kwargs,
            )
            self.ax.add_patch(curve)
        else:
            raise NotImplementedError

    def plot_arrow(self, idx: int, idy: int, position: str,
                   text: Optional[Union[str, float]], **kwargs: Any) -> None:
        """
        Internal method to plot an arrow between two energy levels.

        Parameters
        ----------
        idx : int
            Starting level index
        idy : int
            Ending level index
        position : str
            Arrow position ('center', 'left', or 'right')
        text : Optional[Union[str, float]]
            Text to display on the arrow (default: energy gap)
        **kwargs : Any
            Arrow styling parameters
        """
        start = self._calculate_x_position(self.positions[idx])
        x_arrow = start + 0.5 * self.dimension
        x_text = x_arrow
        y1 = self.energies[idx]
        y2 = self.energies[idy]
        gap = y1 - y2

        if text is None:
            if self.round_energies_at_digit == "keep all digits":
                text = gap
            else:
                text = round(gap, self.round_energies_at_digit)

        middle = y1 - 0.5 * gap
        arrow_width = self.DEFAULT_ARROW_WIDTH
        arrowprops = {
            "arrowstyle": "<->",
            "shrinkA": 0,
            "shrinkB": 0,
            "linestyle": "--",
            "mutation_scale": arrow_width,
            "color": "green",
        }
        bbox = {
            "boxstyle": "round",
            "fc": "white",
            "color": "green",
        }
        arrowprops.update({key: kwargs[key] for key in kwargs if key in arrowprops})
        bbox.update({key: kwargs[key] for key in kwargs if key in bbox})

        # determine arrow position
        if position == "center":
            ha = "center"
        elif position == "right":
            arrowprops["arrowstyle"] = "|-|"
            arrowprops["mutation_scale"] *= 0.2
            x_arrow += 0.5 * self.dimension + 0.2 * self.space
            x_text += 0.5 * self.dimension + 0.5 * self.space
            ha = "left"
        elif position == "left":
            arrowprops["arrowstyle"] = "|-|"
            arrowprops["mutation_scale"] *= 0.2
            x_arrow -= 0.5 * self.dimension + 0.2 * self.space
            x_text -= 0.5 * self.dimension + 0.5 * self.space
            ha = "right"
        else:
            raise ValueError

        # double arrow
        self.ax.annotate(
            "", xy=(x_arrow, y1), xytext=(x_arrow, y2), arrowprops=arrowprops
        )
        # text
        self.ax.text(x_text, middle, text, bbox=bbox, va="center", ha=ha)

        # draw supporting line if levels are offset
        line_kwargs = {"color": "green", "linestyle": "--"}
        line_kwargs.update({key: kwargs[key] for key in kwargs if key in line_kwargs})
        p1 = self.positions[idx]
        p2 = self.positions[idy]
        if p1 > p2:
            x2 = self._calculate_x_position(p2) + self.dimension
            x1 = self._calculate_x_position(p1) + self.dimension
            line = Line2D([x1, x2], [y2, y2], **line_kwargs)
            self.ax.add_line(line)
        elif p2 > p1:
            x2 = self._calculate_x_position(p2)
            x1 = self._calculate_x_position(p1)
            line = Line2D([x1, x2], [y2, y2], **line_kwargs)
            self.ax.add_line(line)

    def plot(
        self, show_IDs: bool = False, ylabel: str = "Energy / $kcal$ $mol^{-1}$",
        ax: Optional[plt.Axes] = None
    ) -> None:
        r"""
        Method of ED class
        Plot the energy diagram. Use show_IDs=True for showing the IDs of the
        energy levels and allowing an easy linking.
        E|          4__
        n|   2__    /  \
        e|1__/  \__/5   \
        r|  3\__/       6\__
        g|
        y|

        Parameters
        ----------
        show_IDs : bool
            show the IDs of the energy levels
        ylabel : str
            The label to use on the left-side axis. "Energy / $kcal$
            $mol^{-1}$" by default.
        ax : plt.Axes
            The axes to plot onto. If not specified, a Figure and Axes will be
            created for you.

        Returns
        -------
        fig (plt.figure) and ax (fig.add_subplot())

        """

        # Create a figure and axis if the user didn't specify them.
        if not ax:
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(111, aspect=self.aspect)
        # Otherwise register the axes and figure the user passed.
        # This is useful if you want to add the diagram to an existing ax.di
        else:
            self.ax = ax
            self.fig = ax.figure

            # Constrain the target axis to have the proper aspect ratio
            # self.ax.set_aspect(self.aspect)

        self.ax.set_ylabel(ylabel)
        self.ax.set_xlabel("Reaction Coordinate")
        self.ax.axes.get_xaxis().set_visible(False)
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["bottom"].set_visible(False)

        self.__auto_adjust()

        data = list(
            zip(
                self.energies,  # 0
                self.positions,  # 1
                self.bottom_texts,  # 2
                self.top_texts,  # 3
                self.right_texts,  # 5
                self.left_texts,  # 6
                self.level_kwargs,
            )
        )  # 7

        for energy, pos, btext, ttext, rtext, ltext, kwargs in data:
            self.plot_level(energy, pos, btext, ttext, rtext, ltext, **kwargs)

        if show_IDs:
            # for showing the ID allowing the user to identify the level
            for ind, level in enumerate(data):
                start = self._calculate_x_position(level[1])
                self.ax.text(
                    start,
                    level[0] + self.offset,
                    str(ind),
                    horizontalalignment="right",
                    color="red",
                )

        for idx, arrow in enumerate(self.arrows):
            # x1, x2   y1, y2
            for idy, position, text, kwargs in arrow:
                self.plot_arrow(idx, idy, position, text, **kwargs)

        for idx, link in enumerate(self.links):
            # here we connect the levels with the links
            # x1, x2   y1, y2
            for idy, kwargs in link:
                self.plot_link(idx, idy, **kwargs)

        for box in self.electrons_boxes:
            # here we add the boxes
            # x,y,boxes,electrons,side,spacing_f
            x, y, boxes, electrons, side, spacing_f = box
            plot_orbital_boxes(self.ax, x, y, boxes, electrons, side, spacing_f)

        # Set xlim to fix x-axis range if specified
        if self.xlim is not None:
            self.ax.set_xlim(self.xlim)

    def __auto_adjust(self) -> None:
        """
        Method of ED class
        This method use the ratio to set the best dimension and space between
        the levels.

        Affects
        -------
        self.dimension
        self.space
        self.offset

        """
        # Max range between the energy
        Energy_variation = abs(max(self.energies) - min(self.energies))
        if self.dimension == "auto" or self.space == "auto":
            if self.xlim is not None:
                # Calculate dimension and space based on xlim range
                xmin, xmax = self.xlim
                total_width = xmax - xmin
                max_position = max(self.positions) if self.positions else 0
                
                # Calculate space for each level position to fit within xlim
                if max_position > 0:
                    space_for_level = total_width / (max_position + 1)
                else:
                    space_for_level = total_width

                self.dimension = space_for_level * self.XLIM_DIMENSION_RATIO
                self.space = space_for_level * self.XLIM_SPACE_RATIO
            else:
                # Original behavior: calculate based on energy variation
                unique_positions = float(len(set(self.positions)))
                space_for_level = Energy_variation * self.ratio / unique_positions
                self.dimension = space_for_level * self.DIMENSION_RATIO
                self.space = space_for_level * self.SPACE_RATIO

        if self.offset == "auto":
            self.offset = Energy_variation * self.offset_ratio
