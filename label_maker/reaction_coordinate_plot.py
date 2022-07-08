import numpy as np
import more_itertools


def BufferList(array):
    """"
    Function to add 0 to beginning and end of a list
    Useful for graphing start and end vectors in reaction diagram
    """
    array.insert(0, 0)
    array.append(0)
    return

def CombineListsAlternatively(a1, a2):
    """
    Combine two lists in alternating fashion
    Used for combining ramp and dwell time arrays when rates are provided
    """
    res = [None] * (len(a1) + len(a2))
    res[::2] = a1
    res[1::2] = a2
    return res

def TemperatureRate(initial_temp, final_temp, initial_time, final_time):
    """
    Get rate of temperature change
    Returns
    -------
    Rate of temperature change over specified time and temp interval
    """
    return (final_temp - initial_temp) / (final_time - initial_time)

def TemperatureFromTime(time, initial_time, final_time, initial_temp, final_temp):
    """
    Get temperature as a function of time
    Returns
    -------
    # Equation for line of temperature as a function of time
    Temperature at time `time`
    """
    slope = TemperatureRate(initial_temp, final_temp, initial_time, final_time)
    return slope * (time - initial_time) + initial_temp


class ReactionDiagram:
    def __init__(self, times=[], temps=[], rates=[]):
        """
        times (array) = array of times FOR ALL RAMPING AND DWELL STEPS
        temps (array) = array of temps FOR ALL DWELLING STEPS
        rates (array) = array of rates FOR RAMPING STEPS
        """
        # Temperature shenanigans
        self.temperatures = temps  # celsius
        self.function_temps = CombineListsAlternatively(self.temperatures, self.temperatures)

        # Rate shenanigans
        self.rates = rates  # celsius/hr # inherently listed only for ramp steps

        # Time shenanigans
        self.times = times  # hr

        if not rates:  # rates don't exist
            # Time lengths
            self.all_times = self.times.copy()
            self.ramp_times = [i for i in self.times if self.times.index(i) % 2 != 0]  # get ramp times
            self.dwell_times = [i for i in self.times if self.times.index(i) % 2 == 0]  # get dwell times
            # Buffer list of all_times
            BufferList(self.all_times)  # add 0 to start and end of all times
        else:  # rates exist
            # Time lengths
            self.ramp_times = self.GetRampTimes()  # get ramp times
            self.dwell_times = self.times
            self.all_times = CombineListsAlternatively(self.ramp_times, self.dwell_times)
            # Buffer list of all_times
            BufferList(self.all_times)
        # Functional times represent the points on the time axis where a vector changes direction
        self.function_times = np.cumsum(self.all_times)
        # Time intervals correspond to how long the ramping/dwelling domains are
        self.time_intervals = [j - i for i, j in zip(self.function_times[:-1], self.function_times[1:])]
        self.time_intervals.insert(0, 0)  # Buffer time intervals with zero in front
        self.total_time = sum(self.all_times)  # get total time

        # (Time, Temp) shenanigans
        self.function_times = np.insert(self.function_times, 0, 0)  # insert zero at front of list

        # Take function_times and function_temps and generate list of tuples representing
        # ((initial_time, final_time), (initial_temp, final_temp)) for plotting
        self.time_temp_pairs = self.GenerateTimeTempList()
        return

    #### Actual shenanigans ####
    def GetTemperatures(self):
        """ Get temperatures of each step """
        return self.temperatures

    def GetTimeIntervals(self):
        """ Get time intervals """
        return tuple(self.times.values())

    def GetFunctionalTimes(self):
        """ Get functional times """
        return self.function_times

    def GenerateTimeTempList(self):
        """
        Returns
        -------
        List of [((initial_time, final_time), (initial_temp, final_temp)), ...]
        """
        pairwise_times = more_itertools.pairwise(self.function_times)
        pairwise_temps = more_itertools.pairwise(self.function_temps)
        return [(t, T) for t, T in zip(pairwise_times, pairwise_temps)]

    #### Rate shenanigans ####
    def GetRampTimes(self):
        """
        Get list of times for Reaction Diagram given input of rates
        Return array of times for ramping steps
        """
        temp_diffs = [j - i for i, j in zip(self.temperatures[:-1], self.temperatures[1:])]
        return [np.absolute(T / rate) for T, rate in zip(temp_diffs, self.rates)]

    #### Temperature shenanigans ####
    def TimeContribution(self, initial_time, final_time):
        """
        Calculate contribution of a single time domain within the diagram to the total time
        Returns
        -------
        Integer percentage of time contributed
        """
        percentage = (np.absolute(final_time - initial_time) / self.total_time) * 100
        return int(np.floor(percentage))

    def RampVector(self, initial_time, final_time, initial_temp, final_temp):
        """
        Generate a vector of temperatures as a function of time.
        This is over only a single time domain on the diagram
        Returns
        -------
        Tuple of (time, temperature) pairs of length proportional to contribution to total time
        """
        time_array = np.linspace(initial_time, final_time, self.TimeContribution(initial_time, final_time))
        z = [TemperatureFromTime(t, initial_time, final_time, initial_temp, final_temp) for t in time_array]
        return time_array, np.array(z)

    def CreateVectors(self):
        """
        Create vectors for plotting
        Generalized number of steps
        Returns
        -------
        ramp_vectors (list) = list of tuples of ramp vectors
        """
        ramp_vectors = []
        for coordinate in self.time_temp_pairs:
            time_coords, temp_coords = coordinate[0], coordinate[1]
            vector = self.RampVector(time_coords[0], time_coords[1], temp_coords[0], temp_coords[1])
            ramp_vectors.append(vector)
        return ramp_vectors

    #### Plotting shenanigans ####
    def PlotVectors(self, ax):
        """
        Help
        """
        for vector in self.CreateVectors():
            ax.plot(vector[0], vector[1], c="k", lw=2)
        return

    #### Annotating shenanigans ####
    def FunctionalTimeTickMarks(self, ax):
        """
        Add tick marks for functional times
        """
        ax.set_xlabel("Time (hr)")
        ax.set_xticks([t for t in self.function_times])
        ax.tick_params(axis="x", labelsize=6)
        return

    def FunctionalTempTickMarks(self, ax):
        """
        Add tick marks for functional times
        """
        ax.set_ylabel("Temp (\N{DEGREE SIGN}C)")
        ax.set_yticks([T for T in self.function_temps])
        ax.tick_params(axis="y", labelsize=6)
        return

    def AnnotateTemperatures(self, ax):
        """
        Annotate temperatures on reaction diagram
        Params
        ------
        ax (axis) = axis to plot onto. Must of be of type returned by plt.subplots()
        """
        # Annotation
        x_shift = self.total_time * 0.01 # Shift text 1% of total time so it doesn't overlap with plot
        y_shift = np.max(self.temperatures) * 0.01 # Shift text so it doesn't overlap with plot
        for vector_2D in self.time_temp_pairs[::2]: # Iterate over every OTHER vector to avoid repeats
            initial_time, initial_temp = vector_2D[0][0], vector_2D[1][0]  # Get initial time, temperature
            ax.annotate(
                f"{initial_temp}\N{DEGREE SIGN}C",
                (initial_time + x_shift, initial_temp + y_shift),
                ha="left", fontsize=12
            )
        return

    def AnnotateTimes(self, ax):
        """
        Annotate times on reaction diagram only for dwell steps
        Params
        ------
        ax (axis) = axis to plot onto. Must of be of type returned by plt.subplots()
        steps (dict) = dictionary of step vectors returned from CreateStepVectors3()
        """
        y_shift = np.max(self.temperatures) * 0.075  # Shift text so it doesn't overlap with plot
        for vector_2D in self.time_temp_pairs[::2]: # Iterate over every OTHER vector to avoid repeats
            # Get start and end time for domain as well as dwelling temperature
            initial_time, final_time, temp = vector_2D[0][0], vector_2D[0][-1], vector_2D[1][0]
            if final_time - initial_time != 0: # make sure we're not at the beginning or end
                ax.annotate(
                    f"{int(final_time - initial_time)} hr",
                    ((initial_time + final_time) / 2, temp - y_shift),
                    ha="center", fontsize=8
                )
        return

    # ALL OF THESE FUNCTIONS NEED TO BE WORKED ON
    def AnnotateRates(self, ax):
        """
        Annotate rates (of temperature change) on reaction diagram
        Params
        ------
        ax (axis) = axis to plot onto. Must of be of type returned by plt.subplots()
        steps (dict) = dictionary of step vectors returned from CreateStepVectors3()
        """
        x_shift = self.total_time * 0.01  # Shift text 1% of total time so it doesn't overlap with plot
        y_shift = np.max(self.temperatures) * 0.01  # Shift text so it doesn't overlap with plot
        for vector_2D in self.time_temp_pairs[1::2]: # Iterate over every OTHER vector to avoid repeats
            initial_time, final_time = vector_2D[0][0], vector_2D[0][1]  # Get initial, final time
            initial_temp, final_temp = vector_2D[1][0], vector_2D[1][1]  # Get initial, final temp
            ramp_rate = TemperatureRate(initial_temp, final_temp, initial_time, final_time)  # Get rate
            ramp_rate = np.absolute(int(round(ramp_rate, 0)))  # Round temperature rate to nearest (absolute) integer
            if initial_temp < final_temp and initial_time != 0: # Shift label depending on sign of slope
                ax.annotate(
                    f"{ramp_rate}\N{DEGREE SIGN}C/hr",
                    ((initial_time + final_time) / 2 - x_shift, (initial_temp + final_temp) / 2 + y_shift),
                    ha="left", fontsize=8, rotation=45
                )
            else:
                # Annotate
                ax.annotate(
                    f"{ramp_rate}\N{DEGREE SIGN}C/hr",
                    ((initial_time + final_time) / 2 + x_shift, (initial_temp + final_temp) / 2 + y_shift),
                    ha="left", fontsize=8, rotation=45
                )
        return


if __name__ == "__main__":
    ...
