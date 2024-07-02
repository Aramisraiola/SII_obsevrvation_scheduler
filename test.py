
from utils.plot_observation import *
from utils.interferometry_objects import *
from utils.source_objects import *

coord_t_1 = np.array([100000000,900, 0.1])
coord_t_2 = np.array([110, 450, 0.2])

latitude = angle_deg_min_sec(45, 0, 0)
physical_baseline = baseline(coord_t_1, coord_t_2, latitude)

declination = angle_deg_min_sec(35,0,0)
duration = [-4, 4]

uvw = spatial_frequency(physical_baseline, duration,600,450e-9, declination)

gamma_cas = uniform_disk(0.45, 450e-9)
_, _, image, extent_im = gamma_cas.get_image_meters()
gamma_cas.plot_fft()
plt.plot(uvw.u(), uvw.v(), linewidth=2)
plt.show()
ax = plot_spatial_uv_plane_image(uvw, image, extent_im, baseline_name='(450 nm light)', fix_source=False)
