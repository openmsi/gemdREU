class SpaceTime:
    def __init__(self, start_date, start_time, end_date="", end_time=""):
        if len(str(start_date)) != 8 or len(str(end_date)) != 8:
            raise ValueError("Date must be in 'YYYYMMDD' format")
        if len(str(start_time)) < 3 or len(str(start_time)) > 4:
            raise ValueError("Invalid time")
        self.start_date = str(start_date)  # YYYYMMDD # Start of experiment
        self.end_date = str(end_date)  # YYYYMMDD # End of experiment
        self.start_time = str(start_time) if len(str(start_time)) == 4 else f"0{start_time}"  # 24-hr clock
        self.end_time = str(end_time) if len(str(end_time)) == 4 else f"0{end_time}"  # 24-hr clock
        return

    ##
    def EndDate(self, end):
        """Define end date of experiment"""
        self.end_date = end
        return

    def EndTime(self, time):
        """Define end time of experiment"""
        self.end_time = time
        return

    def FormatDate(self, date):
        """Change date format to something readable. Using MM/DD/YYYY."""
        m, d, y = date[4:6], date[6:], date[:4]  # Get month, day, year
        return "{:s}/{:s}/{:s}".format(m, d, y)

    def Format24hrTime(self, time):
        """Change the time format to something (more) readable using a 24 hr clock"""
        return "{}:{}".format(int(time[:2]) % 24, time[2:])

    def Format12hrTime(self, time):
        """Change the time format to something (more) readable using a 12 hr clock"""
        hour_24, mn = int(time[:2]), time[2:]  # Get 24 hr representation of time
        hr = hour_24 % 12 if hour_24 != 12 else hour_24  # Convert to 12 hr representation
        meridiem = "AM" if hour_24 < 12 else "PM"  # TEMPORARY: Assumes nobody runs experiments at midnight
        return "{}:{} {}".format(hr, mn, meridiem)

    # Plotting shenanigans
    # Assumes the subplot is a 1x1 square
    def AnnotateStart(self, ax):
        """
        Annotate the start date (and time) of the experiment
        Returns
        -------
        pos (tuple) = position of annotation to be used later for other date/time annotations
        """
        pos = (0.25, 1)
        date = self.FormatDate(self.start_date)
        if self.start_time:
            time = self.Format12hrTime(self.start_time)
            ax.annotate(f"Start: {date}, {time}", pos, ha="left", c="k")
        else:
            ax.annotate(f"Start: {date}", pos, ha="left", c="k")
        return pos

    def AnnotateEnd(self, ax):
        """Annotate the end date (and time) of the experiment"""
        pos = self.AnnotateStart(ax)
        date = self.FormatDate(self.end_date)
        if self.end_time:
            time = self.Format12hrTime(self.end_time)
            ax.annotate(f"End: {date}, {time}", (0.25, pos[1] - 0.25), ha="left", c="k")
        else:
            ax.annotate(f"End: {date}", (0.25, pos[1] - 0.25), ha="left", c="k")
        return

if __name__ == "__main__":
    # Test
    time = SpaceTime(20221218, 245, 20221219, 1355)

    a = time.Format12hrTime(time.start_time)
    b = time.Format24hrTime(time.end_time)
    print("12 Hour Representation: {}".format(a))
    print("24 Hour Representation: {}".format(b))

    c = time.FormatDate(time.start_date)
    d = time.FormatDate(time.end_date)
    print("Date (MM/DD/YYYY): {}".format(c))
    print("Date (MM/DD/YYYY): {}".format(d))