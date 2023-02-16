import healpy as hp
import numpy as np
import os
from plancklens.utils import camb_clfile
from lenscarf import utils_scarf
from lenscarf import cachers
import lenspyx
from lenspyx.remapping.deflection import deflection as duccd
from lenspyx.remapping.deflection_029 import deflection as duccd29

from lenscarf.remapping import deflection as scarfd
from lenspyx.remapping import utils_geom
path2cls = os.path.dirname(lenspyx.__file__)
cls_unl  = camb_clfile(path2cls + '/data/cls/FFP10_wdipole_lenspotentialCls.dat')
cls_len  = camb_clfile(path2cls + '/data/cls/FFP10_wdipole_lensedCls.dat')

def syn_ffi_ducc(lmax_len = 4096, dlmax=1024, epsilon=1e-5, dlm_fac=1., nthreads=0, dlmax_gl=1024):
    """"Returns realistic LCDM deflection field scaled by dlm_fac

    """
    lmax_unl = lmax_len + dlmax
    lmax_dlm, mmax_dlm = lmax_unl, lmax_unl
    lmaxthingauss = lmax_unl + dlmax_gl
    plm = hp.synalm(cls_unl['pp'][:lmax_dlm + 1], new=True)
    dlm = hp.almxfl(plm, dlm_fac * np.sqrt(np.arange(lmax_dlm + 1, dtype=float) * np.arange(1, lmax_dlm + 2)))
    ref_geom = utils_scarf.Geom.get_thingauss_geometry(lmaxthingauss, 2)
    pbref_geom = utils_scarf.pbdGeometry(ref_geom, utils_scarf.pbounds(0., 2 * np.pi))
    ffi_ducc = duccd(pbref_geom, dlm, mmax_dlm, numthreads=nthreads, verbosity=1, dclm=None, epsilon=epsilon, cacher=cachers.cacher_mem(safe=False))
    return ffi_ducc, ref_geom

def syn_ffi_ducc_29(lmax_len = 4096, dlmax=1024, epsilon=1e-5, dlm_fac=1., nthreads=0, dlmax_gl=1024):
    """"Returns realistic LCDM deflection field scaled by dlm_fac

    """
    lmax_unl = lmax_len + dlmax
    lmax_dlm, mmax_dlm = lmax_unl, lmax_unl
    lmaxthingauss = lmax_unl + dlmax_gl
    plm = hp.synalm(cls_unl['pp'][:lmax_dlm + 1], new=True)
    dlm = hp.almxfl(plm, dlm_fac * np.sqrt(np.arange(lmax_dlm + 1, dtype=float) * np.arange(1, lmax_dlm + 2)))
    ref_geom = utils_geom.Geom.get_thingauss_geometry(lmaxthingauss, 2)
    ffi_ducc = duccd29(ref_geom, dlm, mmax_dlm, numthreads=nthreads, verbosity=1, dclm=None, epsilon=epsilon, cacher=cachers.cacher_mem(safe=False))
    return ffi_ducc, ref_geom

def syn_ffi_lenscarf(lmax_len = 4096, dlmax=1024, target_res=1.7, dlm_fac=1., nthreads=4, dlmax_gl=1024, verbose=False, nbands=1):
    """"Returns realistic LCDM deflection field scaled by dlm_fac

    """
    lmax_unl = lmax_len + dlmax
    lmax_dlm, mmax_dlm = lmax_unl, lmax_unl
    lmaxthingauss = lmax_unl + dlmax_gl


    plm = hp.synalm(cls_unl['pp'][:lmax_dlm + 1], new=True)
    dlm = hp.almxfl(plm, dlm_fac * np.sqrt(np.arange(lmax_dlm + 1) * np.arange(1, lmax_dlm + 2)))
    ref_geom = utils_scarf.Geom.get_thingauss_geometry(lmaxthingauss, 2)
    pbref_geom = utils_scarf.pbdGeometry(ref_geom, utils_scarf.pbounds(0., 2 * np.pi))
    fft_tr, sht_tr = nthreads, nthreads
    ffi = scarfd(pbref_geom, target_res, dlm, mmax_dlm, fft_tr, sht_tr, verbose=verbose, dclm=None, cacher=cachers.cacher_mem(safe=False))
    return ffi, ref_geom