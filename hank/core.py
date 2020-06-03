import os
from glob import glob

import numpy as np
from astropy.io import fits
from h5py import File


__all__ = ['data_path', 'hdf5_path', 'write_to_hdf5', 'construct_lc_file_list',
           'construct_sc_file_list']

data_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         os.pardir, 'data'))

hdf5_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         os.pardir, 'data', 'archive.hdf5'))

cols = ['TIME',
 'TIMECORR',
 'CADENCENO',
 'SAP_FLUX',
 'SAP_FLUX_ERR',
 'SAP_BKG',
 'SAP_BKG_ERR',
 'PDCSAP_FLUX',
 'PDCSAP_FLUX_ERR',
 'SAP_QUALITY',
 'PSF_CENTR1',
 'PSF_CENTR1_ERR',
 'PSF_CENTR2',
 'PSF_CENTR2_ERR',
 'MOM_CENTR1',
 'MOM_CENTR1_ERR',
 'MOM_CENTR2',
 'MOM_CENTR2_ERR',
 'POS_CORR1',
 'POS_CORR2']


def construct_lc_file_list():
    """
    Long cadence light curve paths
    """
    paths = glob(os.path.join(data_path, '*llc.fits'))
    return paths


def construct_sc_file_list():
    """
    Short cadence light curve paths
    """
    paths = glob(os.path.join(data_path, '*slc.fits'))
    return paths


def header_to_dict(path):
    """
    Convert header from FITS file to a simple storable dictionary.
    """
    header = fits.getheader(path)

    storable_header_card_types = (int, str, float, bool)

    header_dict = {k: v for k, v in header.items()
                   if type(v) in storable_header_card_types}

    return header_dict


def write_to_hdf5(path):
    """
    Take FITS file at ``path`` and save it into the HDF5 archive
    """
    kid = path.split('kplr')[1].split('-')[0]

    lc_data = fits.getdata(path)

    if os.path.exists(hdf5_path):
        h = File(hdf5_path, 'a')
    else:
        h = File(hdf5_path, 'w')

    attrs = header_to_dict(path)

    if kid in h:
        group = h[kid]
    else:
        group = h.create_group(kid)

    dataset_name = f"q{attrs['QUARTER']}"
    if dataset_name not in group:
        dset = group.create_dataset(dataset_name,
                                    data=np.vstack([lc_data[col]
                                                    for col in cols]))

        for k, v in attrs.items():
            dset.attrs[k] = v

    h.flush()
    h.close()