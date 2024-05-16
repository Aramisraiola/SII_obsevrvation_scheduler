import numpy as np
import matplotlib.pyplot as plt
import scipy

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

        x = np.linspace(-1, 1, self.bins)/diameter
        y = np.linspace(-1, 1, self.bins)/diameter
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


