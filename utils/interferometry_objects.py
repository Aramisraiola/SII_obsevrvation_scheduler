import numpy as np


class angle_deg_min_sec:
    def __init__(self, lat_deg, lat_minutes, lat_seconds):
        self.lat_deg = lat_deg
        self.lat_minutes = lat_minutes
        self.lat_seconds = lat_seconds

    def get_angle_deg_min_sec(self):
        return np.array([self.lat_deg, self.lat_minutes, self.lat_seconds])

    def get_angle_deg(self):
        return self.lat_deg + self.lat_minutes/60 + self.lat_seconds/3600

    def get_angle_radians(self):
        deg_to_rad = np.pi / 180
        return (self.lat_deg + self.lat_minutes / 60 + self.lat_seconds / 3600) * deg_to_rad


class baseline:
    def __init__(self, coordinates_telescope_1, coordinates_telescope_2, latitude):
        self.coord_1 = coordinates_telescope_1
        self.coord_2 = coordinates_telescope_2

        self.baseline_vector = self.coord_1 - self.coord_2

        if not isinstance(latitude, angle_deg_min_sec):
            raise ValueError("Input latitude must be of the form: deg° min' sec'', i.e. it must be an instance from "
                             "class angle_deg_min_sec")

        elif latitude.get_angle_deg()>90:
            raise ValueError("Input latitude must be smaller than 90 degrees")

        else:
            self.latitude = latitude
            self.latitude_radians = latitude.get_angle_radians()

    def lat_rad(self):
        return self.latitude_radians

    def length(self):
        return np.linalg.norm(self.baseline_vector)

    def azimuth(self):
        return np.arctan2(self.baseline_vector[0], self.baseline_vector[1])

    def elevation(self):
        return np.arcsin(self.baseline_vector[2] / self.length())


class spatial_frequency:
    def __init__(self, baseline_value, obs_time, obs_time_binning, wavelength, declination):

        if not isinstance(baseline_value, baseline):
            raise ValueError("Input baseline_value must be an instance of class baseline")
        else:
            self.baseline = baseline_value

        if len(obs_time) != 2:
            raise ValueError("Observation time must be given as variation of Hour Angle [h1,h2]")
        else:
            self.obs_time_min = obs_time[0]
            self.obs_time_max = obs_time[1]

        if not isinstance(declination, angle_deg_min_sec):
            raise ValueError("Input declination must be of the form: deg° min' sec'', i.e. it must be an instance from "
                             "class angle_deg_min_sec")
        else:
            self.declination = declination

        self.t_bin = obs_time_binning
        self.wavelength = wavelength

        self.hour_angle = np.linspace(self.obs_time_min, self.obs_time_max, self.t_bin) * np.pi / 12

        lat = self.baseline.lat_rad()
        elev = self.baseline.elevation()
        az = self.baseline.azimuth()

        self.x_coord = self.baseline.length() * (np.cos(lat) * np.sin(elev) - np.sin(lat) * np.cos(elev) * np.cos(az))
        self.y_coord = self.baseline.length() * np.cos(elev) * np.sin(az)
        self.z_coord = self.baseline.length() * (np.sin(lat) * np.sin(elev) + np.cos(lat) * np.cos(elev) * np.cos(az))

    def get_hour_angle(self):
        return self.hour_angle

    def get_wavelength(self):
        return self.wavelength

    def u(self):
        return self.wavelength ** (-1) * (
                np.sin(self.hour_angle) * self.x_coord + np.cos(self.hour_angle) * self.y_coord) / 1000

    def v(self):
        return self.wavelength ** (-1) * (
                -np.sin(self.declination.get_angle_radians()) * np.cos(self.hour_angle) * self.x_coord + np.sin(
            self.declination.get_angle_radians()) * np.sin(self.hour_angle) * self.y_coord + np.cos(
            self.declination.get_angle_radians()) * self.z_coord) / 1000

    def w(self):
        return self.wavelength ** (-1) * (
                np.cos(self.declination.get_angle_radians()) * np.cos(self.hour_angle) * self.x_coord - np.cos(
            self.declination.get_angle_radians()) * np.sin(self.hour_angle) * self.y_coord + np.sin(
            self.declination.get_angle_radians()) * self.z_coord) / 1000

    def u_spatial(self):
        return np.sin(self.hour_angle) * self.x_coord + np.cos(self.hour_angle) * self.y_coord

    def v_spatial(self):
        return -np.sin(self.declination.get_angle_radians()) * np.cos(self.hour_angle) * self.x_coord + np.sin(
            self.declination.get_angle_radians()) * np.sin(self.hour_angle) * self.y_coord + np.cos(
            self.declination.get_angle_radians()) * self.z_coord

    def w_spatial(self):
        return np.cos(self.declination.get_angle_radians()) * np.cos(self.hour_angle) * self.x_coord - np.cos(
            self.declination.get_angle_radians()) * np.sin(self.hour_angle) * self.y_coord + np.sin(
            self.declination.get_angle_radians()) * self.z_coord

    def minor_axis(self):
        return np.sqrt(self.x_coord ** 2 + self.y_coord ** 2) / self.wavelength / 1000

    def major_axis(self):
        return self.minor_axis() * np.sin(self.declination.get_angle_radians())

    def ellipse_center(self):
        return self.z_coord / self.wavelength * np.cos(self.declination.get_angle_radians()) / 1000

    def minor_axis_spatial(self):
        return np.sqrt(self.x_coord ** 2 + self.y_coord ** 2)

    def major_axis_spatial(self):
        return self.minor_axis() * np.sin(self.declination.get_angle_radians())

    def ellipse_center_spatial(self):
        return self.z_coord * np.cos(self.declination.get_angle_radians())
