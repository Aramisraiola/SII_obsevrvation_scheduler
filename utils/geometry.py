import numpy as np
import matplotlib.pyplot as plt


def plot_image_and_FFT(image, image_FFT, fov_extent, fov_extent_FFT, unit='mas'):
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.imshow(image, extent=[-fov_extent / 2, fov_extent / 2, -fov_extent / 2, fov_extent / 2])
    plt.title('Image Plane (Uniform Disk)')

    if unit == 'mas':
        plt.xlabel('Right ascension $\Delta$RA [mas]')
        plt.ylabel('Declination $\Delta\delta$ [mas]')

    elif unit == 'm':
        plt.xlabel('V [m]')
        plt.ylabel('U [m]')

    else:
        raise ValueError('Unit must be "mas" or "m"')

    plt.colorbar(label='Normalized Intensity [ ]', shrink=0.46)

    # Plot the UV plane
    plt.subplot(1, 2, 2)
    plt.imshow(image_FFT / np.amax(image_FFT),
               extent=[-fov_extent_FFT / 2, fov_extent_FFT / 2, -fov_extent_FFT / 2, fov_extent_FFT / 2])

    plt.title('UV Plane (Fourier Transform)')
    plt.xlabel('U - Spatial Frequency [$k\lambda$]')
    plt.ylabel('V - Spatial Frequency [$k\lambda$]')

    plt.colorbar(label='Normalized amplitude [ ]', shrink=0.46)

    plt.tight_layout()
    plt.show()


def compute_disk(image_size, pixel_size, radius, intensity_max=1):
    y, x = np.indices((image_size, image_size))
    x = (x - image_size // 2) * pixel_size
    y = (y - image_size // 2) * pixel_size
    r = np.sqrt(x ** 2 + y ** 2)

    image_2d = np.zeros((image_size, image_size))
    image_2d[r <= radius] = intensity_max

    return image_2d, x, y
