def AnnotateReactionCoordinate(diagram, ax, times=False, temps=False, rates=False, time_ticks=False, temp_ticks=False):
    """
    Annotate reaction diagram
    Params
    ------
    diagram (reaction_coordinate_plot.ReactionDiagram())
    ax (plt.subplots())
    All other params are bools
    """
    if times:
        diagram.AnnotateTimes(ax)
    if temps:
        diagram.AnnotateTemperatures(ax)
    if rates:
        diagram.AnnotateRates(ax)
    if time_ticks:
        diagram.FunctionalTimeTickMarks(ax)
    if temp_ticks:
        diagram.FunctionalTempTickMarks(ax)
    return

def AnnotateIdentity(person, ax, name=False, jhed=False, email=False, notebook_number=False):
    """
    Annotate Identity
    Params
    ------
    person (experimenter_identity.Identity())
    ax (plt.subplots())
    All other params are bools
    """
    if name:
        person.AnnotateName(ax)
    if jhed:
        person.AnnotateJHED(ax)
    if email:
        person.AnnotateEmail(ax)
    if notebook_number:
        person.AnnotateNotebookNumber(ax)
    return

def AnnotateSpaceTime(space, ax, start=False, end=False):
    """
    Annotate space and time
    Params
    ------
    space (space_and_time.SpaceTime())
    ax (plt.subplots())
    All other params are bools
    """
    if start:
        space.AnnotateStart(ax)
    if end:
        space.AnnotateEnd(ax)
    return

def AnnotateChemistry(chemical, ax, compound=False, ta=False):
    """
    Annotate chemicals
    Params
    ------
    chemical (chemical_identity.Chemicals())
    ax (plt.subplots())
    All other params are bools
    """
    if compound:
        chemical.AnnotateCompound(ax)
    if ta:
        chemical.AnnotateTransportAgent(ax)
    return
