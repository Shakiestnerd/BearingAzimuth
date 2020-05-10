from bearing import angle
import pytest

DEGREE = "\N{DEGREE SIGN}"


class TestAngle:
    @pytest.mark.parametrize(
        "n,d,m,s,e,result",
        [
            ("N", 25, 10, 15, "E", f"N25{DEGREE}10'15\"E : 25.1708{DEGREE}"),
            ("N", 90, 0, 0, "E", f"N90{DEGREE}00'00\"E : 90.0000{DEGREE}"),
            ("S", 1, 0, 0, "E", f"S01{DEGREE}00'00\"E : 179.0000{DEGREE}"),
            ("S", 1, 0, 0, "W", f"S01{DEGREE}00'00\"W : 181.0000{DEGREE}"),
            ("N", 1, 0, 0, "W", f"N01{DEGREE}00'00\"W : 359.0000{DEGREE}"),
            ("N", 30, 0, 0, "W", f"N30{DEGREE}00'00\"W : 330.0000{DEGREE}"),
        ],
    )
    def test_bearing_print(self, n, d, m, s, e, result):
        """Basic loading the bearing and comparing the result to the class string
        representation.
        """
        b = angle.Bearing()
        b.set_bearing(n, d, m, s, e)
        assert b.__str__() == result

    def test_dec_to_dms(self):
        """This bypasses the normal process by setting the _azimuth directly.
        Normally, you should not set variable beginning with underscore.
        """
        b = angle.Bearing()
        b._azimuth = 90.75
        b.dec_to_dms()
        assert b._degree == 89 and b._minute == 15 and b._second == 0

    def test_bearing(self):
        """ Displays instance attributes all zeroes"""
        b = angle.Bearing()
        assert b.__str__() == "N00°00'00\"E : 0.0000°"

    @pytest.mark.parametrize(
        "az,result",
        [
            (90, f"N90{DEGREE}00'00\"E : 90.0000{DEGREE}"),
            (179, f"S01{DEGREE}00'00\"E : 179.0000{DEGREE}"),
            (225, f"S45{DEGREE}00'00\"W : 225.0000{DEGREE}"),
            (231, f"S51{DEGREE}00'00\"W : 231.0000{DEGREE}"),
            (270, f"N90{DEGREE}00'00\"W : 270.0000{DEGREE}"),
            (280.5, f"N79{DEGREE}30'00\"W : 280.5000{DEGREE}"),
        ],
    )
    def test_azimuth(self, az, result):
        """Testing the reverse calculation by setting the azimuth and comparing
        it to the string representation.
        """
        b = angle.Bearing()
        # Quadrant 1
        b.set_azimuth(az)
        assert b.__str__() == result

    def test_submit_bearing(self):
        """Looking at get_bearing and get_azimuth
        """
        b = angle.Bearing()
        b.submit_bearing("N", "45", "0", "0", "W")
        assert b.get_bearing() == f"N45{DEGREE}00'00\"W"
        assert b.get_azimuth() == 315.0000
