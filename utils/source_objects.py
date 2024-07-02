import numpy as np
import matplotlib.pyplot as plt
import scipy
from utils.geometry import *


class uniform_disk:
    def __init__(self, diameter_masec, wavelength, bins=50, intensity_max=1, fov_mas=None):
        mas_to_radian = 4.84814e-6 / 1000

        self.wavelength = wavelength

        self.diameter_mas = diameter_masec
        self.diameter_rad = diameter_masec * mas_to_radian
        self.diameter_meters = self.diameter_rad / self.wavelength

        self.bins = bins
        self.intensity_max = intensity_max
        image_size = self.bins ** 2

        radius_mas = self.diameter_mas / 2
        radius_meters = self.diameter_meters / 2

        if fov_mas is None:
            self.fov_mas = self.diameter_mas * 1
            self.fov_meters = self.diameter_meters * 1
        else:
            self.fov_mas = fov_mas
            self.fov_meters = fov_mas * mas_to_radian / self.wavelength

        self.pixel_size_mas = self.fov_mas / image_size
        self.pixel_size_meters = self.fov_meters / image_size

        image_mas, _, _ = self.compute_disk(image_size, self.pixel_size_mas, radius_mas, self.intensity_max)
        image_meters, _, _ = self.compute_disk(image_size, self.pixel_size_meters, radius_meters, self.intensity_max)

        uv_plane_inv_mas = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(image_mas)))
        uv_plane_inv_meters = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(image_meters)))

        self.uv_amplitude_inv_mas = np.abs(uv_plane_inv_mas)
        self.uv_amplitude_inv_meters = np.abs(uv_plane_inv_meters)

        self.uv_extent_inv_mas = 1 / self.pixel_size_mas / self.wavelength
        self.uv_extent_inv_meters = 1 / self.pixel_size_meters / self.wavelength

        self.image_mas = image_mas
        self.image_meters = image_meters

    def compute_disk(self, image_size, pixel_size, radius, intensity_max):
        x = np.linspace(-image_size / 2, image_size / 2, image_size) * pixel_size
        y = np.linspace(-image_size / 2, image_size / 2, image_size) * pixel_size
        xv, yv = np.meshgrid(x, y)
        rv = np.sqrt(xv ** 2 + yv ** 2)
        disk = (rv <= radius) * intensity_max
        return disk, xv, yv

    def plot_fft(self, use_meters=True):
        if use_meters:
            uv_amplitude = self.uv_amplitude_inv_meters
            uv_extent = self.uv_extent_inv_meters
        else:
            uv_amplitude = self.uv_amplitude_inv_mas
            uv_extent = self.uv_extent_inv_mas

        plt.imshow(np.log(uv_amplitude + 1e-10), extent=(-uv_extent / 2, uv_extent / 2, -uv_extent / 2, uv_extent / 2))
        plt.colorbar(label='Log Amplitude')
        plt.title('FFT of Uniform Disk')
        plt.xlabel('u')
        plt.ylabel('v')



# Example usage:

    def get_uv_amplitude(self):
        return self.u, self.v

    def get_image_mas(self):
        return self.image_mas,self.fov_mas,self.uv_amplitude_inv_mas,self.uv_extent_inv_mas

    def get_image_meters(self):
        return self.image_meters,self.fov_meters,self.uv_amplitude_inv_meters,self.uv_extent_inv_meters

    def check_shape_mas(self):
        plot_image_and_FFT(self.image_mas, self.uv_amplitude_inv_mas, self.fov_mas, self.uv_extent_inv_mas, 'mas')

    def check_shape_meters(self):
        plot_image_and_FFT(self.image_meters, self.uv_amplitude_inv_meters, self.fov_meters, self.uv_extent_inv_meters,
                           'm')


class gaussian_disk:
    def __init__(self, diameter, intensity_center, bins):
        self.diameter = diameter
        self.intensity = intensity_center
        self.bins = bins

        x = np.linspace(-1, 1, self.bins)
        y = np.linspace(-1, 1, self.bins)
        X, Y = np.meshgrid(x, y)
        Z = np.exp(-(X ** 2 + Y ** 2))

        self.brightness_distribution = Z * self.intensity

        fft_2d = scipy.fft.fft2(self.brightness_distribution)

        self.visibility = np.abs(fft_2d)

    def get_brightness(self):
        return self.brightness_distribution

    def get_visibility(self):
        return self.visibility

    def show_disk(self):
        plt.figure()
        plt.imshow(self.brightness_distribution, interpolation='none')
        plt.show()

    def show_visibility(self):
        plt.figure()
        plt.imshow(self.visibility, interpolation='none', vmax=0.5)
        plt.show()


class gaussian_disk:
    def __init__(self, diameter, intensity_center, bins):
        self.diameter = diameter
        self.intensity = intensity_center
        self.bins = bins

        x = np.linspace(-1, 1, self.bins) / diameter
        y = np.linspace(-1, 1, self.bins) / diameter
        X, Y = np.meshgrid(x, y)
        Z = np.sqrt(X ** 2 + Y ** 2)

        self.brightness_distribution = Z * self.intensity

        fft_2d = np.fft.ifftshift(self.brightness_distribution)
        fft_2d = np.fft.fft2(fft_2d)
        fft_2d = np.fft.fftshift(fft_2d)

        self.visibility = np.abs(fft_2d)

    def get_brightness(self):
        return self.brightness_distribution

    def get_visibility(self):
        return self.visibility

    def show_disk(self):
        plt.figure()
        plt.imshow(self.brightness_distribution, interpolation='none')
        plt.show()

    def show_visibility(self):
        plt.figure()
        plt.imshow(self.visibility, interpolation='none', vmax=0.5)
        plt.show()
