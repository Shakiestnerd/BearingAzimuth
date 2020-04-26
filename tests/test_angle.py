from bearing import angle

DEGREE = u'\N{DEGREE SIGN}'


class TestAngle:

    def test_bearing_print(self):
        b = angle.Bearing()
        # Quadrant 1
        b.set_bearing('N', 25, 10, 15, 'E')
        assert(b.__str__() == f"N25{DEGREE}10'15\"E : 25.1708{DEGREE}")
        b.set_bearing('N', 90, 0, 0, 'E')
        assert (b.__str__() == f"N90{DEGREE}00'00\"E : 90.0{DEGREE}")
        # Quadrant 2
        b.set_bearing('S', 1, 0, 0, 'E')
        assert (b.__str__() == f"S01{DEGREE}00'00\"E : 179.0{DEGREE}")
        b.set_bearing('S', 1, 0, 0, 'W')
        # Quadrant 3
        assert (b.__str__() == f"S01{DEGREE}00'00\"W : 181.0{DEGREE}")
        # Quadrant 4
        b.set_bearing('N', 1, 0, 0, 'W')
        assert (b.__str__() == f"N01{DEGREE}00'00\"W : 359.0{DEGREE}")
        b.set_bearing('N', 30, 0, 0, 'W')
        assert (b.__str__() == f"N30{DEGREE}00'00\"W : 330.0{DEGREE}")

    def test_dec_to_dms(self):
        """This bypasses the normal process by setting the _azimuth directly.
        Normally, you should not set variable beginning with underscore.
        """
        b = angle.Bearing()
        b._azimuth = 90.75
        b.dec_to_dms()
        assert(b.__str__() == f"S89{DEGREE}15'00\"E : 90.75{DEGREE}")

    def test_bearing(self):
        """ Displays instance attributes all zeroes"""
        b = angle.Bearing()
        assert(b.__str__() == "N00°00'00\"E : 0°")

    def test_azimuth(self):
        b = angle.Bearing()
        # Quadrant 1
        b.set_azimuth(90)
        assert (b.__str__() == f"N90{DEGREE}00'00\"E : 90{DEGREE}")
        # Quadrant 2
        b.set_azimuth(179)
        assert (b.__str__() == f"S01{DEGREE}00'00\"E : 179{DEGREE}")
        # Quadrant 3
        b.set_azimuth(225)
        assert (b.__str__() == f"S45{DEGREE}00'00\"W : 225{DEGREE}")
        b.set_azimuth(231)
        assert (b.__str__() == f"S51{DEGREE}00'00\"W : 231{DEGREE}")
        # Quadrant 4
        b.set_azimuth(270)
        assert (b.__str__() == f"N90{DEGREE}00'00\"W : 270{DEGREE}")
        b.set_azimuth(280.5)
        assert (b.__str__() == f"N85{DEGREE}30'00\"W : 280.5{DEGREE}")
