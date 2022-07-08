import matplotlib.pyplot as plt
from experimenter_identity import Identity
from chemical_identity import Chemicals
from space_and_time import SpaceTime
from reaction_coordinate_plot import ReactionDiagram
import annotate_label

def HideSomeSpines(ax):
    """ This is just a function to hide the top and right spines on a plt diagram because I do it so often """
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    return

def HideAllSpines(ax):
    """ This is just a function to hide all spines on a plt diagram because I do it so often """
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    return

def LabelBeautification(ax):
    """
    Beautify label
    Assumes ax = [ax0, ax1] and that ax0 --> details // ax1 --> reaction diagram
    """
    # Clean top label
    HideAllSpines(ax[0])
    ax[0].set_xticks([])
    ax[0].set_yticks([])

    # Clean bottom label
    HideSomeSpines(ax[1])
    ax[1].set_xticks([])
    ax[1].set_yticks([])

    return

def main(times,  temps, rates=[]):
    """ Main function in N dimensions """
    # Figure instance
    fig, ax = plt.subplots(nrows=2, ncols=1, gridspec_kw={"height_ratios": [1, 4]})
    # Beautification, i.e., remove spines + tick marks
    LabelBeautification(ax)

    #### Reaction Diagram ####
    dwell = ReactionDiagram(times=times, temps=temps, rates=rates)
    dwell.PlotVectors(ax[1])
    annotate_label.AnnotateReactionCoordinate(
        dwell, ax[1],
        times=True,
        temps=True,
        rates=True,
        time_ticks=True,
        temp_ticks=True
    )

    #### Experimenter Identity ####
    sam = Identity("Name", "JHED")
    sam.NotebookNumber("Page Number")
    annotate_label.AnnotateIdentity(
        sam, ax[0],
        name=True,
        jhed=True,
        email=True,
        notebook_number=True
    )

    #### Date, Location, Time, etc. ####
    spacetime = SpaceTime(20221218, 245, 20221219, 1355)
    annotate_label.AnnotateSpaceTime(
        spacetime, ax[0],
        start=True,
        end=True
    )

    #### Chemicals and Such ####
    chemical = Chemicals("Superconductor", "I2")
    annotate_label.AnnotateChemistry(
        chemical, ax[0],
        compound=False, # LOOK TO chemical_identity.AnnotateTransportAgent() FOR ISSUE
        ta=True
    )

    # Funsies
    plt.suptitle("I am a God")
    return

if __name__ == "__main__":
    rate_test = True # change this bool for rates vs. no rates
    temp_array = [25, 650, 1200, 1000, 250, 25]

    # Rates exist
    if rate_test:
        time_array = [48, 12, 12, 36]
        rate_array = [104.167, 22.917, 16.667, 31.25, 37.5] # C/hr # IF YOU"RE MAKING THIS DATA UP, MAKE SURE MATH IS CORRECT
        main(times=time_array, temps=temp_array, rates=rate_array)
        plt.savefig("images/Rates.pdf")
    # Rates don't exist
    else:
        time_array = [6, 48, 24, 12, 12, 12, 24, 36, 6] # hr
        main(times=time_array, temps=temp_array, rates=[])
        plt.savefig("images/No_rates.pdf")
