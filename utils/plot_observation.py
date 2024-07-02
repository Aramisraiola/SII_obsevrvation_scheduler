import matplotlib.pyplot as plt
from utils.interferometry_objects import *


def plot_uv_plane(spatial_freq, show_full_observation=False, ax=None, plot_legend=True, baseline_name=''):
    if not isinstance(spatial_freq, spatial_frequency):
        raise ValueError('The spatial_frequencies argument must be a spatial_frequency class instance')

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.set_box_aspect(1)

    num_existing_plots = len(ax.lines)
    baseline_color = plt.cm.viridis(num_existing_plots / 5)

    ax.plot(spatial_freq.u(), spatial_freq.v(), label='Baseline {}'.format(baseline_name), color=baseline_color,
            linewidth=2)
    ax.plot(-spatial_freq.u(), -spatial_freq.v(), color=baseline_color, linewidth=2)

    if show_full_observation:
        theta = np.linspace(0, 2 * np.pi, 100)
        x_real = spatial_freq.minor_axis() * np.cos(theta)
        y_real = spatial_freq.ellipse_center() + spatial_freq.major_axis() * np.sin(theta)

        x_im = spatial_freq.minor_axis() * np.cos(theta)
        y_im = - spatial_freq.ellipse_center() + spatial_freq.major_axis() * np.sin(theta)

        ax.plot(x_real, y_real, linestyle='--')
        ax.plot(x_im, y_im, linestyle='--')

    ax.set_xlabel('u  [k$\lambda$]')
    ax.set_ylabel('v  [k$\lambda$]')
    ax.set_title('Observation UV-plane (real space')
    if plot_legend:
        ax.legend()

    return ax


def plot_spatial_uv_plane(spatial_freq, show_full_observation=False, ax=None, plot_legend=True, baseline_name=''):
    if not isinstance(spatial_freq, spatial_frequency):
        raise ValueError('The spatial_frequencies argument must be a spatial_frequency class instance')

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.set_box_aspect(1)

    num_existing_plots = len(ax.lines)
    baseline_color = plt.cm.viridis(num_existing_plots / 5)

    ax.plot(spatial_freq.u_spatial(), spatial_freq.v_spatial(), label='Baseline {}'.format(baseline_name),
            color=baseline_color, linewidth=2)
    ax.plot(-spatial_freq.u_spatial(), -spatial_freq.v_spatial(), color=baseline_color, linewidth=2)

    if show_full_observation:
        theta = np.linspace(0, 2 * np.pi, 100)
        x_real = spatial_freq.minor_axis_spatial() * np.cos(theta)
        y_real = spatial_freq.ellipse_center_spatial() + spatial_freq.major_axis_spatial() * np.sin(theta)

        x_im = spatial_freq.minor_axis_spatial() * np.cos(theta)
        y_im = - spatial_freq.ellipse_center_spatial() + spatial_freq.major_axis_spatial() * np.sin(theta)

        ax.plot(x_real, y_real, linestyle='--', color=baseline_color)
        ax.plot(x_im, y_im, linestyle='--', color=baseline_color)

    ax.set_xlabel('u  [m]')
    ax.set_ylabel('v  [m]')
    ax.set_title('Observation projected baseline')
    if plot_legend:
        ax.legend()

    return ax


def plot_telescopes_delay(spatial_freq, ax=None, color='tab:blue', baseline_name=''):
    if not isinstance(spatial_freq, spatial_frequency):
        raise ValueError('The spatial_frequencies argument must be a spatial_frequency class instance')

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.set_box_aspect(1)

    c = 3e8
    delay = spatial_freq.w() * spatial_freq.get_wavelength() / c

    sec_to_ps = 1e12

    ax.plot(spatial_freq.get_hour_angle(), delay * sec_to_ps, color=color, label='Baseline {}'.format(baseline_name))

    ax.set_xlabel('Observation time [hours]')
    ax.set_ylabel('Optical delay [ps]')
    ax.set_title('Baseline optical delay')

    ax.legend()

    return ax

def plot_spatial_uv_plane_image(spatial_freq, source_image, fov_extent, show_full_observation=False, fix_source=False, ax=None, plot_legend=True, baseline_name=''):
    if not isinstance(spatial_freq, spatial_frequency):
        raise ValueError('The spatial_frequencies argument must be a spatial_frequency class instance')

    if ax is None:
        fig,ax=plt.subplots()

    num_existing_plots = len(ax.lines)
    baseline_color = plt.cm.viridis(num_existing_plots / 5)

    ax.imshow(source_image, extent=[-fov_extent / 2, fov_extent / 2, -fov_extent / 2, fov_extent / 2], cmap='inferno')
    ax.plot(spatial_freq.u(), spatial_freq.v(), label='Baseline {}'.format(baseline_name),
            color=baseline_color, linewidth=2)
    ax.plot(-spatial_freq.u(), -spatial_freq.v(), color='yellow', linewidth=2)
    print(spatial_freq.u())

    if show_full_observation:
        theta = np.linspace(0, 2 * np.pi, 100)
        x_real = spatial_freq.minor_axis_spatial() * np.cos(theta)
        y_real = spatial_freq.ellipse_center_spatial() + spatial_freq.major_axis_spatial() * np.sin(theta)

        x_im = spatial_freq.minor_axis_spatial() * np.cos(theta)
        y_im = - spatial_freq.ellipse_center_spatial() + spatial_freq.major_axis_spatial() * np.sin(theta)

        ax.plot(x_real, y_real, linestyle='--', color=baseline_color)
        ax.plot(x_im, y_im, linestyle='--', color=baseline_color)

    if fix_source:
        ax.set_xlim(-fov_extent / 2, fov_extent / 2)
        ax.set_ylim(-fov_extent / 2,fov_extent / 2)

    ax.set_xlabel('u  [m]')
    ax.set_ylabel('v  [m]')
    ax.set_title('Observation projected baseline')

    if plot_legend:
        ax.legend()

    plt.tight_layout()
    plt.show()
    return ax
