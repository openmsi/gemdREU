class Chemicals:
    def __init__(self, compound, transport_agent=""):
        self.compound = compound
        self.ta = transport_agent

    # Plotting shenanigans
    # Assumes the subplot is a 1x1 square
    def AnnotateCompound(self, ax):
        """Define positions of each element relative to the name of experimenter. Annotate name of experimenter"""
        pos = (1,1)
        ax.annotate(f"{self.compound} Synthesis", pos, ha="right", c="k")
        return pos
    def AnnotateTransportAgent(self, ax):
        """Annotate name of experimenter"""
        pos = self.AnnotateCompound(ax)
        if self.ta:
            ax.annotate(f"Transport Agent: {self.ta}", (1, pos[1]-0.25), ha="right", c="k")
        return

if __name__ == "__main__":
    # Test
    oxide = Chemicals("Ba2O3", "I2")
    oxide.ta