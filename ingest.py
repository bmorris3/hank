from hank import construct_lc_file_list, write_to_hdf5, LightCurve

lc_paths = construct_lc_file_list()

for path in lc_paths:
    write_to_hdf5(path)

import matplotlib.pyplot as plt
lc = LightCurve.from_hdf5('010000009')
lc.plot()
plt.show()