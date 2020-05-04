import math
from typing import Dict

DEGREE = u'\N{DEGREE SIGN}'


class Bearing:
    """
    The Bearing class handles storing the data for bearing and azimuth.
    It does the conversion between the two and returns the information in
    several formats.
    """
    def __init__(self):
        """
        Initialize the private class variables.  They are not intended to be
        addressed directly.  Use the included methods instead.
        """
        self._degree: int = 0
        self._minute: int = 0
        self._second: int = 0
        self._azimuth: float = 0
        self._north: str = 'N'
        self._east: str = 'E'

    def __str__(self) -> str:
        """
        Text output of both the bearing and azimuth
        """
        result: str = f"{self._north}{int(self._degree):02d}{DEGREE}{int(self._minute):02d}'" \
                      f"{int(self._second):02d}\"{self._east} : {self._azimuth}{DEGREE}"
        return result

    def __repr__(self) -> str:
        """
        Repr output of both the bearing and azimuth
        """
        result: str = f"{self._north}{int(self._degree):02d}{DEGREE}{int(self._minute):02d}'" \
                      f"{int(self._second):02d}\"{self._east} : {self._azimuth}{DEGREE}"
        return result

    def set_bearing(self, n: str, d: int, m: int, s: int, e: str) -> float:
        """
        Initialize a bearing and perform the azimuth conversion
        :arg n: northing (is always either 'N' or 'S')
        :arg d: degrees
        :arg m: minutes
        :arg s: seconds
        :arg e: easting (always either 'E' or 'W')
        :return: the azimuth as a float

        """
        self._north = str(n)
        self._degree = int(d)
        self._minute = int(m)
        self._second = int(s)
        self._east = str(e)
        self.calc_azimuth()
        return self._azimuth

    def set_azimuth(self, az: float) -> str:
        """
        Set the value of the azimuth and perform the bearing conversion.
        :arg az: azimuth value
        :return: The bearing as a string
        """
        self._azimuth = float(az)
        self.calc_bearing(az)
        return self.get_bearing()

    def calc_azimuth(self) -> None:
        """
        Performs the azimuth conversion using the private members
        :return: None
        """
        angle = round(self._degree + self._minute / 60 + self._second / 3600, 4)
        if self._north == "N" and self._east == "E":
            self._azimuth = angle
        if self._north == "N" and self._east == "W":
            self._azimuth = 360 - angle
        if self._north == "S" and self._east == "E":
            self._azimuth = 180 - angle
        if self._north == "S" and self._east == "W":
            self._azimuth = 180 + angle

    def calc_bearing(self, az: float) -> None:
        """
        Performs the bearing calculation.
        :arg az: Azimuth as a float
        :return: None
        """
        if az <= 90.0 or az >= 270.0:
            self._north = "N"
        else:
            self._north = "S"
        if 0.0 < az < 180.0:
            self._east = "E"
        else:
            self._east = "W"
        self.dec_to_dms()

    def dec_to_dms(self) -> None:
        """
        Adjust the angle based on north and sets the degrees, minutes, and
        seconds member variables.
        :return: None
        """
        if self._azimuth < -360 or self._azimuth > 360:
            raise ValueError(f"Azimuth angle must be between 0{DEGREE} and 360{DEGREE}.")

        angle = self._azimuth
        # adjust angle based on quadrant
        if 90 < self._azimuth <= 180:
            angle = 180 - self._azimuth
        elif 180 < self._azimuth < 270:
            angle = self._azimuth - 180
        elif 270 <= self._azimuth <= 360:
            angle = 360 - self._azimuth

        decimal, self._degree = math.modf(angle)

        remainder, self._minute = math.modf(decimal * 60)

        self._second = remainder * 60

    def get_bearing(self) -> str:
        """
        Return just the bearing as a formatted string.
        :return: bearing value
        """
        result: str = f"{self._north}{int(self._degree):02d}{DEGREE}{int(self._minute):02d}'" \
                      f"{int(self._second):02d}\"{self._east}"
        return result

    def get_bearing_dict(self) -> Dict:
        """
        Return the components of a bearing in a dictionary.
        """
        return {"northing": f"{self._north}", "degrees": f"{int(self._degree):02d}",
                "minutes": f"{int(self._minute):02d}",
                "seconds": f"{int(self._second):02d}", "easting": f"{self._east}"}

    def get_azimuth(self) -> float:
        """
        Since accessing the member variables directly is discouraged, this
        method returns the azimuth value
        :return: azimuth as a float
        """
        return self._azimuth

    def submit_bearing(self, n: str, d: str, m: str, s: str, e: str) -> float:
        """
        Initialize a bearing using string values for input.  submit_bearing
        does some extra validation and converts degrees minutes, and seconds
        to integers.
        :arg n: northing (is always either 'N' or 'S')
        :arg d: degrees
        :arg m: minutes
        :arg s: seconds
        :arg e: easting (always either 'E' or 'W')
        :return: the azimuth as a float or 0 on failure
        """
        valid_input = False
        if len(n) == 1 and len(e) == 1:
            if n in ["N", "S"] and e in ["E", "W"]:
                if 0 < len(d) < 3 and 0 < len(m) < 3 and 0 < len(s) < 3:
                    valid_input = True
                    return self.set_bearing(n, int(d), int(m), int(s), e)
                else:
                    return 0

    def submit_azimuth(self, az: str) -> Dict:
        """
        Sets the azimuth value when the input is a string.  Does some validation
        and returns the bearing as a dictionary.
        :return: bearing as a dict
        """
        try:
            value = float(az)
            if 0 <= value <= 360:
                self.set_azimuth(value)
        except ValueError:
            self.set_azimuth(0)

        return self.get_bearing_dict()


if __name__ == "__main__":
    b = Bearing()
    b.set_azimuth(90.75)
    print(b)
    assert (b.__str__() == f"S89{DEGREE}15'00\"E : 90.75{DEGREE}")
