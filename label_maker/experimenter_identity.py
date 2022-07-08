class Identity:
    def __init__(self, name, jhed, page=""):  # sam.page returns FALSE when page=""
        # Only one of these?
        self.name = name
        self.jhed = jhed
        self.page = page

    # Shenanigans
    def NotebookNumber(self, page):
        """ Assign page number to experiment """
        self.page = page
        return

    # Plotting shenanigans
    # Assumes the subplot is a 1x1 square
    def AnnotateName(self, ax):
        """ Define positions of each element relative to the name of experimenter. Annotate name of experimenter """
        pos = (0, 1)
        ax.annotate(f"{self.name}", pos, ha="left", c="k")
        return pos

    def AnnotateJHED(self, ax):
        """ Annotate name of experimenter """
        pos = self.AnnotateName(ax)
        ax.annotate(f"{self.jhed}", (0, pos[1] - 0.25), c="k")
        return

    def AnnotateEmail(self, ax):
        """ Annotate name of experimenter """
        pos = self.AnnotateName(ax)
        ax.annotate(f"{self.jhed}@jhu.edu", (0, pos[1] - 0.5), c="k")
        return

    def AnnotateNotebookNumber(self, ax):
        """ Annotate name of experimenter """
        pos = self.AnnotateName(ax)
        ax.annotate(f"{self.page}", (0, pos[1] - 0.75), c="k")
        return

if __name__ == "__main__":
    ...
