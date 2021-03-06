###############################################################################
# plot_effsel_location: plot the effective selection function for a given 
#                       location
###############################################################################
import os, os.path
import sys
import pickle
import numpy
import matplotlib
matplotlib.use('Agg')
from galpy.util import save_pickles, bovy_plot
from matplotlib import rc, pyplot
import mwdust
import apogee.select.apogeeSelect
from define_rcsample import get_rcsample
_PLOTDIST= True
_LW= 1.5
_EXAGGERATE_ERRORS= 1.
def plot_effsel_location(location,plotname):
    # Setup selection function
    selectFile= '../savs/selfunc-nospdata.sav'
    if os.path.exists(selectFile):
        with open(selectFile,'rb') as savefile:
            apo= pickle.load(savefile)
    else:
        # Setup selection function
        apo= apogee.select.apogeeSelect()
        # Delete these because they're big and we don't need them
        del apo._specdata
        del apo._photdata
        save_pickles(selectFile,apo)
    effselFile= '../savs/effselfunc-%i.sav' % location
    if not os.path.exists(effselFile):
        # Distances at which to calculate the effective selection function
        distmods= numpy.linspace(7.,15.5,301)
        ds= 10.**(distmods/5-2.)
        # Setup default effective selection function
        do_samples= True
        gd= mwdust.Green15(filter='2MASS H',load_samples=do_samples)
        apof= apogee.select.apogeeEffectiveSelect(apo,dmap3d=gd)
        sf_default= apof(location,ds)
        # Also calculate for a sample of MH
        data= get_rcsample()
        MH= data['H0']-data['RC_DM']
        MH= numpy.random.permutation(MH)[:1000]
        sf_jkz= apof(location,ds,MH=MH)
        # Go through the samples
        sf_samples= numpy.zeros((20,len(ds)))
        if do_samples:
            for ii in range(20):
                # Swap in a sample for bestfit in the Green et al. (2015) dmap
                gd.substitute_sample(ii)
                apof= apogee.select.apogeeEffectiveSelect(apo,dmap3d=gd)
                sf_samples[ii]= apof(location,ds)          
        zerodust= mwdust.Zero(filter='2MASS H')
        apof= apogee.select.apogeeEffectiveSelect(apo,dmap3d=zerodust)
        sf_zero= apof(location,ds)
        drimmel= mwdust.Drimmel03(filter='2MASS H')
        apof= apogee.select.apogeeEffectiveSelect(apo,dmap3d=drimmel)
        sf_drimmel= apof(location,ds)
        marshall= mwdust.Marshall06(filter='2MASS H')
        apof= apogee.select.apogeeEffectiveSelect(apo,dmap3d=marshall)
        try:
            sf_marshall= apof(location,ds)
        except IndexError:
            sf_marshall= -numpy.ones_like(ds)
        sale= mwdust.Sale14(filter='2MASS H')
        apof= apogee.select.apogeeEffectiveSelect(apo,dmap3d=sale)
        try:
            sf_sale= apof(location,ds)
        except (TypeError,ValueError):
            sf_sale= -numpy.ones_like(ds)
        save_pickles(effselFile,distmods,sf_default,sf_jkz,sf_samples,
                     sf_zero,sf_drimmel,sf_marshall,sf_sale)
    else:
        with open(effselFile,'rb') as savefile:
            distmods= pickle.load(savefile)
            sf_default= pickle.load(savefile)
            sf_jkz= pickle.load(savefile)
            sf_samples= pickle.load(savefile)
            sf_zero= pickle.load(savefile)
            sf_drimmel= pickle.load(savefile)
            sf_marshall= pickle.load(savefile)
            sf_sale= pickle.load(savefile)
    # Now plot
    bovy_plot.bovy_print(fig_height=3.)
    rc('text.latex', preamble=r'\usepackage{amsmath}'+'\n'
       +r'\usepackage{amssymb}'+'\n'+r'\usepackage{yfonts}')
    if _PLOTDIST:
        distmods= 10.**(distmods/5-2.)
        xrange= [0.,12.]
        xlabel=r'$D\,(\mathrm{kpc})$'
        ylabel=r'$\textswab{S}(\mathrm{location},D)$'
    else:
        xrange=[7.,15.8],
        xlabel=r'$\mathrm{distance\ modulus}\ \mu$'
        ylabel=r'$\textswab{S}(\mathrm{location},\mu)$'
    line_default= bovy_plot.bovy_plot(distmods,sf_default,
                                      'b-',lw=_LW,zorder=12,
                                      xrange=xrange,
                                      xlabel=xlabel,
                                      yrange=[0.,1.2*numpy.amax(sf_zero)],
                                      ylabel=ylabel)
    pyplot.fill_between(distmods,
                        sf_default-_EXAGGERATE_ERRORS\
                            *(sf_default-numpy.amin(sf_samples,axis=0)),
                        sf_default+_EXAGGERATE_ERRORS\
                            *(numpy.amax(sf_samples,axis=0)-sf_default),
                        color='0.65',zorder=0)
    line_jkz= bovy_plot.bovy_plot(distmods,sf_jkz,'g-.',lw=2.*_LW,
                                   overplot=True,zorder=13)
    line_zero= bovy_plot.bovy_plot(distmods,sf_zero,'k--',lw=_LW,
                                   overplot=True,zorder=7)
    line_drimmel= bovy_plot.bovy_plot(distmods,sf_drimmel,'-',color='gold',
                                      lw=_LW,overplot=True,zorder=8)
    line_marshall= bovy_plot.bovy_plot(distmods,sf_marshall,'r-',lw=_LW,
                                       overplot=True,
                        zorder=9)
    line_sale= bovy_plot.bovy_plot(distmods,sf_sale,'c-',lw=_LW,overplot=True,
                                   zorder=10)
    if location == 4378:
        pyplot.legend((line_default[0],line_jkz[0],line_zero[0]),
                      (r'$\mathrm{Green\ et\ al.\ (2015)}$',
                       r'$\mathrm{Green\ et\ al.} + p(M_H)$',
                       r'$\mathrm{zero\ extinction}$'),
                      loc='lower right',#bbox_to_anchor=(.91,.375),
                      numpoints=8,
                      prop={'size':14},
                      frameon=False)
    elif location == 4312:
        pyplot.legend((line_sale[0],line_marshall[0],line_drimmel[0]),
                      (r'$\mathrm{Sale\ et\ al.\ (2014)}$',
                       r'$\mathrm{Marshall\ et\ al.\ (2006)}$',
                       r'$\mathrm{Drimmel\ et\ al.\ (2003)}$'),
                      loc='lower right',#bbox_to_anchor=(.91,.375),
                      numpoints=8,
                      prop={'size':14},
                      frameon=False)                      
    # Label
    lcen, bcen= apo.glonGlat(location)
    if numpy.fabs(bcen) < 0.1: bcen= 0.
    bovy_plot.bovy_text(r'$(l,b) = (%.1f,%.1f)$' % (lcen,bcen),
                        top_right=True,size=16.)
    bovy_plot.bovy_end_print(plotname)
    return None

if __name__ == '__main__':
    #4240 is 30,0
    plot_effsel_location(int(sys.argv[1]),sys.argv[2])
