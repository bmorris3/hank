import numpy as np
import matplotlib.pyplot as plt
from h5py import File

from .core import hdf5_path, cols

__all__ = ["LightCurve"]


class LightCurve(object):
    def __init__(self, time=None, timecorr=None, cadenceno=None, sap_flux=None,
                 sap_flux_err=None, sap_bkg=None, sap_bkg_err=None,
                 pdcsap_flux=None, pdcsap_flux_err=None, sap_quality=None,
                 psf_centr1=None, psf_centr1_err=None, psf_centr2=None,
                 psf_centr2_err=None, mom_centr1=None, mom_centr1_err=None,
                 mom_centr2=None, mom_centr2_err=None, pos_corr1=None,
                 pos_corr2=None, header=None):
        self.time = time
        self.timecorr = timecorr
        self.cadenceno = cadenceno
        self.sap_flux = sap_flux
        self.sap_flux_err = sap_flux_err
        self.sap_bkg = sap_bkg
        self.sap_bkg_err = sap_bkg_err
        self.pdcsap_flux = pdcsap_flux
        self.pdcsap_flux_err = pdcsap_flux_err
        self.sap_quality = sap_quality
        self.psf_centr1 = psf_centr1
        self.psf_centr1_err = psf_centr1_err
        self.psf_centr2 = psf_centr2
        self.psf_centr2_err = psf_centr2_err
        self.mom_centr1 = mom_centr1
        self.mom_centr1_err = mom_centr1_err
        self.mom_centr2 = mom_centr2
        self.mom_centr2_err = mom_centr2_err
        self.pos_corr1 = pos_corr1
        self.pos_corr2 = pos_corr2
        self.header = header

    def plot(self, ax=None, sap=True):
        """
        Plot a light curve.
        """
        if ax is None:
            ax = plt.gca()

        ax.plot(self.time, self.sap_flux)

        return ax

    @classmethod
    def from_hdf5(cls, kid):
        h = File(hdf5_path, 'r')
        quarters = h[f'{kid}']

        lightcurves = []
        for q in list(quarters):
            dataset = quarters[q]
            attrs = dict(dataset.attrs)
            data = dataset[:]
            constructor_dict = {c.lower(): data[i, :]
                                for i, c in enumerate(cols)}
            lightcurves.append(cls(header=attrs, **constructor_dict))

        h.close()

        return sum(lightcurves)

    def __add__(self, other):
        attrs = [c.lower() for c in cols]
        self_matrix = np.vstack([getattr(self, attr) for attr in attrs])
        other_matrix = np.vstack([getattr(other, attr) for attr in attrs])
        stacked = np.hstack([self_matrix, other_matrix])

        constructor_dict = {c.lower(): stacked[i, :]
                            for i, c in enumerate(cols)}

        return LightCurve(header=self.header, **constructor_dict)

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)