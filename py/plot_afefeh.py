###############################################################################
# plot_afefeh: the basic [a/Fe] vs. [Fe/H] plot for the data section
###############################################################################
import sys
import matplotlib
import numpy
from scipy import special
matplotlib.use('Agg')
from galpy.util import bovy_plot
from matplotlib import pyplot
import define_rcsample
def plot_afefeh(plotfilename):
    # Load the data
    data= define_rcsample.get_rcsample()
    # Plot the data
    bovy_plot.bovy_print()
    bovy_plot.scatterplot(data[define_rcsample._FEHTAG],
                          data[define_rcsample._AFETAG],
                          'k.',ms=.8,
                          levels=special.erf(numpy.arange(1,2)/numpy.sqrt(2.)),
                          xrange=[-1.,0.4],
                          yrange=[-0.15,0.35],
                          xlabel=r'$[\mathrm{Fe/H}]$',
                          ylabel=define_rcsample._AFELABEL)
    # Overplot sub-samples
    # low alpha, low feh
    lowfeh= define_rcsample._lowlow_lowfeh(0.)
    highfeh= define_rcsample._lowlow_highfeh(0.)
    pyplot.plot([lowfeh,lowfeh],[define_rcsample._lowlow_lowafe(lowfeh),
                                 define_rcsample._lowlow_highafe(lowfeh)],
                'k--',lw=2.)
    pyplot.plot([highfeh,highfeh],[define_rcsample._lowlow_lowafe(highfeh),
                                   define_rcsample._lowlow_highafe(highfeh)],
                'k--',lw=2.)
    pyplot.plot([lowfeh,highfeh],[define_rcsample._lowlow_lowafe(lowfeh),
                                  define_rcsample._lowlow_lowafe(highfeh)],
                'k--',lw=2.)
    pyplot.plot([lowfeh,highfeh],[define_rcsample._lowlow_highafe(lowfeh),
                                  define_rcsample._lowlow_highafe(highfeh)],
                'k--',lw=2.)
    # high alpha
    lowfeh= define_rcsample._highalpha_lowfeh(0.)
    highfeh= define_rcsample._highalpha_highfeh(0.)
    pyplot.plot([lowfeh,lowfeh],[define_rcsample._highalpha_lowafe(lowfeh),
                                 define_rcsample._highalpha_highafe(lowfeh)],
                'k--',lw=2.)
    pyplot.plot([highfeh,highfeh],[define_rcsample._highalpha_lowafe(highfeh),
                                   define_rcsample._highalpha_highafe(highfeh)],
                'k--',lw=2.)
    pyplot.plot([lowfeh,highfeh],[define_rcsample._highalpha_lowafe(lowfeh),
                                  define_rcsample._highalpha_lowafe(highfeh)],
                'k--',lw=2.)
    pyplot.plot([lowfeh,highfeh],[define_rcsample._highalpha_highafe(lowfeh),
                                  define_rcsample._highalpha_highafe(highfeh)],
                'k--',lw=2.)
    # solar
    lowfeh= define_rcsample._solar_lowfeh(0.)
    highfeh= define_rcsample._solar_highfeh(0.)
    pyplot.plot([lowfeh,lowfeh],[define_rcsample._solar_lowafe(lowfeh),
                                 define_rcsample._solar_highafe(lowfeh)],
                'k--',lw=2.)
    pyplot.plot([highfeh,highfeh],[define_rcsample._solar_lowafe(highfeh),
                                   define_rcsample._solar_highafe(highfeh)],
                'k--',lw=2.)
    pyplot.plot([lowfeh,highfeh],[define_rcsample._solar_lowafe(lowfeh),
                                  define_rcsample._solar_lowafe(highfeh)],
                'k--',lw=2.)
    pyplot.plot([lowfeh,highfeh],[define_rcsample._solar_highafe(lowfeh),
                                  define_rcsample._solar_highafe(highfeh)],
                'k--',lw=2.)
    # high [Fe/H]
    lowfeh= define_rcsample._highfeh_lowfeh(0.)
    highfeh= define_rcsample._highfeh_highfeh(0.)
    pyplot.plot([lowfeh,lowfeh],[define_rcsample._highfeh_lowafe(lowfeh),
                                 define_rcsample._highfeh_highafe(lowfeh)],
                'k--',lw=2.)
    pyplot.plot([highfeh,highfeh],[define_rcsample._highfeh_lowafe(highfeh),
                                   define_rcsample._highfeh_highafe(highfeh)],
                'k--',lw=2.)
    pyplot.plot([lowfeh,highfeh],[define_rcsample._highfeh_lowafe(lowfeh),
                                  define_rcsample._highfeh_lowafe(highfeh)],
                'k--',lw=2.)
    pyplot.plot([lowfeh,highfeh],[define_rcsample._highfeh_highafe(lowfeh),
                                  define_rcsample._highfeh_highafe(highfeh)],
                'k--',lw=2.)
    # Label them
    bovy_plot.bovy_text(-0.4,0.265,r'$\mathrm{high}\ [\alpha/\mathrm{Fe}]$',
                         size=15.,backgroundcolor='w')
    bovy_plot.bovy_text(-0.975,0.05,r'$\mathrm{low\ [Fe/H]}$',
                         size=15.,backgroundcolor='w')
    bovy_plot.bovy_text(0.,-0.125,r'$\mathrm{high\ [Fe/H]}$',
                         size=15.,backgroundcolor='w')
    bovy_plot.bovy_text(-0.225,-0.125,r'$\mathrm{solar}$',
                         size=15.,backgroundcolor='w')
    # Loci
    if False:
        haloc= define_rcsample.highalphalocus()
        bovy_plot.bovy_plot(haloc[:,0],haloc[:,1],'k-',lw=2.,overplot=True)
        haloc= define_rcsample.lowalphalocus()
        bovy_plot.bovy_plot(haloc[:,0],haloc[:,1],'k-',lw=2.,overplot=True)
    bovy_plot.bovy_end_print(plotfilename)
    return None

if __name__ == '__main__':
    plot_afefeh(sys.argv[1])
