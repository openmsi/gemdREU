import numpy as np
import more_itertools

class ReactionDiagram:
    def __init__(self, times=[], temps=[], rates=[]):
        """
        times (array) = array of times FOR ALL RAMPING AND TEMP STEPS
        temps (array) = array of temps FOR ALL DWELLING STEPS
        rates (array) = array of rates FOR RAMPING STEPS
        """
        # Temperature shenanigans
        self.temperatures = temps  # celsius
        self.function_temps = self.CombineListsAlternatively(self.temperatures, self.temperatures)

        # Rate shenanigans
        self.rates = rates  # celsius/hr # inherently listed only for ramp steps

        # Time shenanigans
        self.times = times  # hr
        if not rates: # rates don't exist
            # Time lengths
            self.all_times = self.times.copy() # These are
            self.BufferList(self.all_times) # add 0 to start and end of all times
            self.ramp_times = [i for i in self.times if self.all_times.index(i) % 2 != 0] # get ramp times
            self.dwell_times = [i for i in self.times if self.all_times.index(i) % 2 == 0] # get dwell times
        else: # rates exist
            # Time lengths
            self.ramp_times = self.GetRampTimes() # get ramp times
            self.dwell_times = self.times
            self.all_times = self.CombineListsAlternatively(self.ramp_times, self.dwell_times)
            self.BufferList(self.all_times) # add 0 to start and end of all times
            self.BufferList(self.dwell_times) # add 0 to start and end of dwell times
        self.function_times = np.cumsum(self.all_times) # get functional times
        # Get time intervals
        self.time_intervals = [j-i for i, j in zip(self.function_times[:-1], self.function_times[1:])]
        self.time_intervals.insert(0, 0) # Buffer time intervals with zero in front
        self.total_time = sum(self.all_times)  # get total time

        # (Time, Temp) shenanigans
        self.function_times = np.insert(self.function_times, 0, 0)
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

    def CombineListsAlternatively(self, dwell_times, ramp_times):
        """
        Combine two lists in alternating fashion
        Used for combining ramp and dwell time arrays when rates are provided
        """
        res = [None] * (len(ramp_times) + len(dwell_times))
        res[::2] = dwell_times
        res[1::2] = ramp_times
        return res

    def BufferList(self, array):
        """"
        Function to add 0 to beginning and end of a list
        Useful for graphing start and end vectors in reaction diagram
        """
        array.insert(0, 0)
        array.append(0)
        return

    def GenerateTimeTempList(self):
        """
        Returns
        -------
        List of [((initial_time, final_time), (initial_temp, final_temp))]
        """
        res = []
        pairwise_times = more_itertools.pairwise(self.function_times)
        pairwise_temps = more_itertools.pairwise(self.function_temps)
        for t, T in zip(pairwise_times, pairwise_temps):
            res.append((t, T))
        return res

    #### Rate shenanigans ####
    def GetRampTimes(self):
        """
        Get list of times for Reaction Diagram given input of rates
        """
        rate_array = self.rates
        temp_array = self.temperatures
        temp_diffs = [j-i for i, j in zip(temp_array[:-1], temp_array[1:])]
        return [np.absolute(T/rate) for T, rate in zip(temp_diffs, rate_array)] # return array of times for ramping steps

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

    def TemperatureRate(self, initial_temp, final_temp, initial_time, final_time):
        """
        Get rate of temperature change
        Returns
        -------
        Rate of temperature change over specified time and temp interval
        """
        return (final_temp - initial_temp) / (final_time - initial_time)

    def TemperatureFromTime(self, time, initial_time, final_time, initial_temp, final_temp):
        """
        Get temperature as a function of time
        Returns
        -------
        # Equation for line of temperature as a function of time
        Temperature at time `time`
        """
        slope = self.TemperatureRate(initial_temp, final_temp, initial_time, final_time)
        return slope * (time - initial_time) + initial_temp

    def RampVector(self, initial_time, final_time, initial_temp, final_temp):
        """
        Generate a vector of temperatures as a function of time.
        This is over only a single time domain on the diagram
        Returns
        -------
        Tuple of (time, temperature) pairs of length proportional to contribution to total time
        """
        time_array = np.linspace(initial_time, final_time, self.TimeContribution(initial_time, final_time))
        z = [self.TemperatureFromTime(t, initial_time, final_time, initial_temp, final_temp) for t in time_array]
        return time_array, np.array(z)

    def CreateVectors(self):
        """
        Create vectors for plotting. Generalized number of steps
        Returns
        -------
        ramp_vectors (tuple) = tuple of ramp vectors
        """
        ramp_vectors = []
        for coordinate in self.time_temp_pairs:
            time_coord, temp_coord = coordinate[0], coordinate[1]
            vector = self.RampVector(time_coord[0], time_coord[1], temp_coord[0], temp_coord[1])
            ramp_vectors.append(vector)
        return ramp_vectors

    #### Plotting shenanigans ####
    def PlotVectors(self, ax, vector_array):
        """
        Help
        """
        for vector in vector_array:
            ax.plot(vector[0], vector[1], c="k", lw=2)
        return

    #### Annotating shenanigans ####
    # ALL OF THESE FUNCTIONS NEED TO BE WORKED ON
    def AnnotateTemperatures(self, ax):
        """
        Annotate temperatures on reaction diagram
        Params
        ------
        ax (axis) = axis to plot onto. Must of be of type returned by plt.subplots()
        steps (dict) = dictionary of step vectors returned from CreateStepVectors3()
        """
        # Annotation
        translate = 10  # Shift text so it doesn't overlap with plot
        for vector_2D in self.time_temp_pairs:
            initial_time, initial_temp = vector_2D[0][0], vector_2D[1][0]  # Get time, temperature
            ax.annotate(
                f"{initial_temp}\N{DEGREE SIGN}C",
                (initial_time, initial_temp + translate),
                ha="left", fontsize=12
                )
        return

    def AnnotateTimes(self, ax, vector_array):
        """
        Annotate times on reaction diagram
        Params
        ------
        ax (axis) = axis to plot onto. Must of be of type returned by plt.subplots()
        steps (dict) = dictionary of step vectors returned from CreateStepVectors3()
        """
        ii = 0
        time_intervals = self.times
        # Annotation
        for vector in vector_array:
            initial_time, final_time = vector[0][0], vector[0][-1]  # Get start and end time for domain
            ax.annotate(
                f"{final_time - initial_time} hr",
                # Relies on the order in which key:vals are added to the dictionary
                ((initial_time + final_time) / 2, np.min(self.GetTemperatures())),
                ha="center", fontsize=10
            )
            ii += 1
        return

    def AnnotateRates(self, ax, vector_array):
        """
        Annotate rates (of temperature change) on reaction diagram
        Params
        ------
        ax (axis) = axis to plot onto. Must of be of type returned by plt.subplots()
        steps (dict) = dictionary of step vectors returned from CreateStepVectors3()
        """
        for vector in vector_array:
            initial_temp, final_temp = vector[1][0], vector[1][-1]  # Get initial, final temp
            initial_time, final_time = vector[0][0], vector[0][-1]  # Get initial, final time
            ramp_rate = self.TemperatureRate(initial_temp, final_temp, initial_time, final_time)  # Get rate
            ramp_rate = np.absolute(int(round(ramp_rate, 0)))  # Round temperature rate to nearest integer

            # Annotate on the outside of the graph always
            ax.annotate(
                f"{ramp_rate}\N{DEGREE SIGN}C/hr",
                ((initial_time + final_time) / 2 - 1, (initial_temp + final_temp) / 2),
                ha="right", fontsize=12
            )
            ax.annotate(
                f"{ramp_rate}\N{DEGREE SIGN}C/hr",
                ((initial_time + final_time) / 2 + 1, (initial_temp + final_temp) / 2),
                ha="left", fontsize=12
            )
        return

if __name__ == "__main__":
    # Printing time stuff
    times = [5, 48, 4, 36, 5]
    temps = [25, 1200, 800, 25]
    dwell = ReactionDiagram(times=times, temps=temps)
    a = dwell.CreateVectors()
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    dwell.PlotVectors(ax, a)
    plt.savefig("weinger.pdf")


