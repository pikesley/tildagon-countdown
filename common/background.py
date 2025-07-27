from ..common.asset_path import asset_path


class Background:
    """Background."""

    def __init__(
        self,
        colour=(0, 0, 0),
        image="emf.png",
        opacity=1.0,
    ):
        """Construct."""
        self.colour = list(colour) + [opacity]
        # self.image = image

    def draw(self, ctx):
        """Draw ourself."""
        # ctx.image(asset_path("countdown") + self.image, -120, -120, 240, 240)

        ctx.rgba(*self.colour)
        ctx.rectangle(-120, -120, 240, 240)
        ctx.fill()
