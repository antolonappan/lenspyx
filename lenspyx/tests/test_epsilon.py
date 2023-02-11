""" This plots the accuracy of the fwd remapping on a subset of rings as function of epsilon accuracy parameters


"""
from lenspyx.tests.helper import syn_ffi_ducc, cls_unl, cls_len
from lenscarf import cachers
import healpy as hp, numpy as np
import pylab as pl
from time import time
from lenscarf.utils_scarf import Geom


#res, nside, nthreads = 1.71, 2048, 8
#lmax_len, mmax_len, dlmax = 4096, 4096, 1024
res, nside, nthreads = 1.7, 2048, 8
lmax_len, mmax_len, dlmax = 100, 100, 20
SAVE = lmax_len == 4096
OPTI = True

lmax_unl, mmax_unl = lmax_len + dlmax, lmax_len + dlmax
thingauss = False # healpix rings
dlm_fac = 1.


ffi_ducc, ref_geom = syn_ffi_ducc(lmax_len=lmax_len, dlmax=dlmax, dlm_fac=dlm_fac,
                                  nthreads=nthreads)
ffi_ducc.single_prec = False

#ffi_ducc_opti, ref_geom = syn_ffi_ducc(lmax_len=lmax_len, dlmax=dlmax, target_res=res, nside=nside, dlm_fac=dlm_fac,
#                                  nthreads=nthreads, thingauss=thingauss, optiversion=True)
ffi_ducc.verbosity = 0
eblm = np.array([hp.synalm(cls_unl['ee'][:lmax_unl+1]),
                 hp.synalm(cls_unl['bb'][:lmax_unl+1])])
Pexs = [] # exact pol.
pixels = []
phis = []
ofs_sorted = np.argsort(ffi_ducc.geom.ofs)
rings = [ffi_ducc.geom.weight.size//2, 0, 100, ffi_ducc.geom.weight.size-1]
for ir in rings:
    pixs = Geom.rings2pix(ffi_ducc.geom, [ofs_sorted[ir]])
    phi = Geom.rings2phi(ffi_ducc.geom, [ofs_sorted[ir]])

    if len(pixs) > 200:
        phi =  phi[:: len(pixs) // 100]
        pixs = pixs[:: len(pixs) // 100]
    Qex, Uex = ffi_ducc.gclm2lenpixs(eblm, mmax_unl, 2, pixs)
    Pexs.append(Qex + 1j * Uex)
    pixels.append(pixs)
    phis.append(phi)
ptg=ffi_ducc._get_ptg()
Colors = ['C%s'%s for s in range(10)]
ls = ['-', '--', '-.', ':']
pl.figure(figsize=(20, 5))
norm = None
for ie, epsilon in enumerate([1e-3, 1e-5, 1e-7, 1e-9][::-1]):
    tffi_ducc, _ = syn_ffi_ducc(lmax_len=lmax_len, dlmax=dlmax, dlm_fac=dlm_fac,
                                      nthreads=nthreads, epsilon=epsilon)
    tffi_ducc = tffi_ducc.change_dlm([ffi_ducc.dlm, None], ffi_ducc.mmax_dlm, cacher=cachers.cacher_mem(safe=False))
    tffi_ducc.single_prec = False

    tffi_ducc.verbosity = 0
    tffi_ducc.cacher.cache('ptg', ptg) # avoiding angle calculation overhead
    t0 = time()
    Q, U = tffi_ducc.gclm2lenmap(eblm, mmax_unl, 2, False, ptg=ptg)
    print(' %.3f exec time for eps' % (time() - t0), int(np.log10(epsilon)))

    if norm is None:
        norm = 1./np.sqrt(np.mean(Q ** 2 + U ** 2))
    for i, ir in enumerate(rings):
        # for rings with large numbers of theta we undersample
        tht = tffi_ducc.geom.theta[ofs_sorted[ir]]
        pl.semilogy(phis[i], norm * np.abs(Pexs[i] - (Q[pixels[i]] + 1j*U[pixels[i]])), c=Colors[i],ls=ls[ie], label=r'$\epsilon =10^{%i},  \theta = %.1f$ deg.'%(np.log10(epsilon), tht / np.pi * 180))

pl.xlabel(r'$\phi$', fontsize=13)
pl.ylabel(r'relative polarization error')
pl.xticks([0., np.pi * 0.5, np.pi , 3 * np.pi * 0.5, 2 * np.pi], [r'0', r'$\pi/2$',r'$\pi$',r'$3\pi/2$',r'$2\pi$' ])
pl.xlim(0. - 0.0125 * np.pi, 2 * np.pi + 0.0125 * np.pi)
if False and (lmax_unl <= 1000 or nside <= 2048): # plotlenspyx like at 1.78 res should add this
    ffi._fwd_angles()
    t0 = time()
    Q, U = ffi.gclm2lenmap(eblm, mmax_unl, 2, False)
    print(' %.3f JC exec time ' % (time() - t0))

    for i, ir in enumerate(rings):
        tht = ffi_ducc.geom.theta[ofs_sorted[ir]]
        pl.semilogy(phis[i], norm * np.abs(Pexs[i] - (Q[pixels[i]] + 1j*U[pixels[i]])), c='k')

#if SAVE:
#    assert 0, 'fix this'
#    pl.savefig('../../Tex/figs/epsilon.pdf', bbox_inches='tight')
pl.show()