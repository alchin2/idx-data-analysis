from matplotlib.ticker import ScalarFormatter


class FixedOrderFormatter(ScalarFormatter):
    """ScalarFormatter that forces the axis offset to a fixed power of 10,

    Example:
        ax.set_xticks(np.linspace(0, 1e8, 11))
        ax.xaxis.set_major_formatter(FixedOrderFormatter(7))
        # -> ticks read 0..10 with a "1e7" axis offset
    """

    def __init__(self, order):
        super().__init__(useOffset=True, useMathText=False)
        self._fixed_order = order

    def _set_order_of_magnitude(self):
        self.orderOfMagnitude = self._fixed_order
