from utils.plot_observation import *
from utils.source_objects import *

if __name__ == '__main__':
    coord_t_1 = np.array([25.095, -9.095, 0.045])
    coord_t_2 = np.array([90.284, 26.380, -0.226])
    latitude = angle_deg_min_sec(-30,-43,-17.34)
    declination = angle_deg_min_sec(-30,-43,-17.34)
    duration = [-4, 4]

    physical_baseline = baseline(coord_t_1, coord_t_2, latitude)

    uvw = spatial_frequency(physical_baseline, duration,600,450e-9, declination)
    uwu_2 = spatial_frequency(physical_baseline, duration,600,500e-9, declination)
    uwu_3 = spatial_frequency(physical_baseline, duration, 600, 550e-9, declination)
    uwu_4 = spatial_frequency(physical_baseline, duration, 600, 600e-9, declination)

    ax=plot_uv_plane(uvw, baseline_name='(450 nm light)')
    plot_uv_plane(uwu_2, ax=ax, baseline_name='(500 nm light)')
    plot_uv_plane(uwu_3, ax=ax, baseline_name='(550 nm light)')
    plot_uv_plane(uwu_4, ax=ax, baseline_name='(600 nm light)')
    plot_telescopes_delay(uvw)

    plot_spatial_uv_plane(uwu_2, baseline_name='')

    disk=gaussian_disk(1000,1,1000)
    disk.show_visibility()
    disk.show_disk()
    plt.show()




