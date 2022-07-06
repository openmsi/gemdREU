import numpy as np

class ReactionDiagram:
    def __init__(self, heat_time, dwell_time, cool_time, initial_temp, dwell_temp, final_temp):
        self.times = {"up": heat_time, "dwell": dwell_time, "down": cool_time}  # hr # Relies on dict naming
        self.function_times = (
            0,
            heat_time,
            dwell_time + heat_time,
            cool_time + dwell_time + heat_time,
        )
        self.total_time = sum(self.times.values())
        self.temperatures = (initial_temp, dwell_temp, final_temp)  # celsius
        return

    # Shenanigans
    def GetTemperatures(self):
        """Get temperatures of each step"""
        return self.temperatures

    def GetTimeIntervals(self):
        """Get time intervals"""
        return tuple(self.times.values())

    def GetFunctionalTimes(self):
        """Get functional times"""
        return self.function_times

    # Temperature shenanigans
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
        Rate of temperature change over specificed time and temp interval
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

    def HeatingCoolingDwellingVector(self, initial_time, final_time, initial_temp, final_temp):
        """
        Generate a vector of temperatures as a function of time.
        This is over only a single time domain on the diagram
        Returns
        -------
        Tuple of (time, temperature) pairs of length proportional to contribution to total time
        """
        time_array = np.linspace(initial_time, final_time, self.TimeContribution(initial_time, final_time))
        if initial_temp == final_temp:  # Check if dwelling
            z = [initial_temp for _ in time_array]
        else:  # If not dwelling, algorithm to create heating/cooling vector
            z = [self.TemperatureFromTime(t, initial_time, final_time, initial_temp, final_temp) for t in time_array]
        return time_array, np.array(z)

    def StartEndVector(self, temp, piece):
        """
        Builds piece of diagram for starting and ending steps.
        piece (int) is a bit to denote whether the piece is for the beginning or end
            piece = 0 denotes the starting piece. Any other character denotes the ending piece.
        Returns
        -------
        Tuple of (time, temperature) pairs of length which is 5% of the total time
        """
        contribution = self.TimeContribution(self.total_time / 7, 2 * self.total_time / 7)
        length = self.total_time * contribution / 100
        if piece == 0:
            time_array = np.linspace(self.function_times[0] - length, self.function_times[0], contribution)
        else:
            time_array = np.linspace(self.function_times[-1], self.function_times[-1] + length, contribution)
        z = [temp for _ in time_array]
        return time_array, np.array(z)

    def CreateStepVectors3(self, temps, functional_times):
        """
        Create vectors for plotting. Assumes three steps (excluding start and end steps).
        Params
        ------
        temps (array) = list of 3 temperatures for each step in reaction diagram
        functional_times (array) = list of 4 times to begin each step vector (~ tail of the vector)
        Returns
        -------
        steps (dict) = dictionary of segment:vector pairs where segment is portion of reaction diagram
        and vector is StartEndVector() or HeatingCoolingDwellingVector() types
        """
        steps = {}
        # Start
        steps["start"] = self.StartEndVector(temps[0], 0)
        # Ramp up
        steps["up"] = self.HeatingCoolingDwellingVector(
            functional_times[0], functional_times[1], temps[0], temps[1]
        )
        # Dwell
        steps["dwell"] = self.HeatingCoolingDwellingVector(
            functional_times[1], functional_times[2], temps[1], temps[1]
        )
        # Ramp down
        steps["down"] = self.HeatingCoolingDwellingVector(
            functional_times[-2], functional_times[-1], temps[-2], temps[-1]
        )
        # End
        steps["end"] = self.StartEndVector(temps[-1], 1)
        return steps

    # Plotting shenanigans
    # Should plotting be a different class entirely?
    # NOT as optimized as it should be
    def PlotStepVectors3(self, ax, steps, temps):
        # Is this function necessary? More annoying to control color, lw, etc., using it imo
        # Maybe combine with AnnotateStepVectors3()? Separate rn for better control over display
        """
        Plot steps on reaction diagram
        Params
        ------
        ax (axis) = axis to plot onto. Must of be of type returned by pyplot.subplots()
        steps (dict) = dictionary of step vectors returned from CreateStepVectors3()
        temps (array) = temperatures for each step in the reaction diagram
        """
        for key, vector in steps.items():
            # Plotting series
            ax.plot(vector[0], vector[1], c="k", lw=2)
        return

    def AnnotateTemperatures3(self, ax, steps):
        """
        Annotate temperatures on reaction diagram
        Params
        ------
        ax (axis) = axis to plot onto. Must of be of type returned by plt.subplots()
        steps (dict) = dictionary of step vectors returned from CreateStepVectors3()
        """
        # Annotation
        translate = 10  # Shift text so it doesn't overlap with plot
        for key, vector in steps.items():
            if key != "up" and key != "down":
                initial_time, initial_temp = vector[0][0], vector[1][0]  # Get time, temperature
                ax.annotate(
                    f"{initial_temp}\N{DEGREE SIGN}C",
                    (initial_time, initial_temp + translate),
                    ha="left", fontsize=12
                )
        return

    def AnnotateTimes3(self, ax, steps):
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
        for key, vector in steps.items():
            if key != "start" and key != "end":
                initial_time, final_time = vector[0][0], vector[0][-1]  # Get start and end time for domain
                ax.annotate(
                    f"{time_intervals[key]} hr",  # This is a band-aid fix
                    # Relies on the order in which key:vals are added to the dictionary
                    ((initial_time + final_time) / 2, np.min(self.GetTemperatures())),
                    ha="center", fontsize=10
                )
                ii += 1
        return

    def AnnotateRates3(self, ax, steps):
        """
        Annotate rates (of temperature change) on reaction diagram
        Params
        ------
        ax (axis) = axis to plot onto. Must of be of type returned by plt.subplots()
        steps (dict) = dictionary of step vectors returned from CreateStepVectors3()
        """
        for key, vector in steps.items():
            if key == "up" or key == "down":
                initial_temp, final_temp = vector[1][0], vector[1][-1]  # Get initial, final temp
                initial_time, final_time = vector[0][0], vector[0][-1]  # Get initial, final time
                ramp_rate = self.TemperatureRate(initial_temp, final_temp, initial_time, final_time)  # Get rate
                ramp_rate = np.absolute(int(round(ramp_rate, 0)))  # Round temperature rate to nearest integer
                # Annotate on the outside of the graph always
                if key == "up":
                    ax.annotate(
                        f"{ramp_rate}\N{DEGREE SIGN}C/hr",
                        ((initial_time + final_time) / 2 - 1, (initial_temp + final_temp) / 2),
                        ha="right", fontsize=12
                    )
                else:
                    ax.annotate(
                        f"{ramp_rate}\N{DEGREE SIGN}C/hr",
                        ((initial_time + final_time) / 2 + 1, (initial_temp + final_temp) / 2),
                        ha="left", fontsize=12
                    )
        return

if __name__ == "__main__":
    ...