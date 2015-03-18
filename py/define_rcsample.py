###############################################################################
# define_rcsample: definitions of the sample used
###############################################################################
import numpy
import esutil
from galpy.util import bovy_coords
import apogee.tools.read as apread
from apogee.samples.rc import rcdist
import isodist
_FEHTAG= 'FE_H'
_AFETAG= 'AVG_ALPHAFE'
_AFELABEL= r'$[\left([\mathrm{O+Mg+Si+S+Ca}]/5\right)/\mathrm{Fe}]$'
def get_rcsample():
    """
    NAME:
       get_rcsample
    PURPOSE:
       get the RC sample
    INPUT:
       None so far
    OUTPUT:
       sample
    HISTORY:
       2015-02-10 - Started - Bovy (IAS@KITP)
    """
    data= apread.rcsample()
    # Cut to statistical sample
    data= data[data['STAT'] == 1]
    # Add the M_H-based distances
    data= esutil.numpy_util.add_fields(data,[('RC_DIST_H', float),
                                             ('RC_DM_H', float),
                                             ('RC_GALR_H', float),
                                             ('RC_GALPHI_H', float),
                                             ('RC_GALZ_H', float)])
    rcd= rcdist()
    jk= data['J0']-data['K0']
    z= isodist.FEH2Z(data['METALS'],zsolar=0.017)
    data['RC_DIST_H']= rcd(jk,z,appmag=data['H0'],mh=True)
    data['RC_DM_H']= 5.*numpy.log10(data['RC_DIST_H'])+10.
    XYZ= bovy_coords.lbd_to_XYZ(data['GLON'],
                                data['GLAT'],
                                data['RC_DIST_H'],
                                degree=True)
    R,phi,Z= bovy_coords.XYZ_to_galcencyl(XYZ[:,0],
                                          XYZ[:,1],
                                          XYZ[:,2],
                                          Xsun=8.,Zsun=0.025)
    data['RC_GALR_H']= R
    data['RC_GALPHI_H']= phi
    data['RC_GALZ_H']= Z
    # Add the average alpha/Fe
    data= esutil.numpy_util.add_fields(data,[('AVG_ALPHAFE', float)])
    weight_o= numpy.ones(len(data))
    weight_s= numpy.ones(len(data))
    weight_si= numpy.ones(len(data))
    weight_ca= numpy.ones(len(data))
    weight_mg= numpy.ones(len(data))
    weight_o[data['O_H'] == -9999.0]= 0.
    weight_s[data['S_H'] == -9999.0]= 0.
    weight_si[data['SI_H'] == -9999.0]= 0.
    weight_ca[data['CA_H'] == -9999.0]= 0.
    weight_mg[data['MG_H'] == -9999.0]= 0.
    data['AVG_ALPHAFE']= (weight_o*data['O_H']+weight_s*data['S_H']
                          +weight_si*data['SI_H']+weight_ca*data['CA_H']
                          +weight_mg*data['MG_H'])/(weight_o+weight_s
                                                    +weight_si+weight_ca
                                                    +weight_mg)\
                                                    -data['FE_H']-0.05
    # Remove locations outside of the Pan-STARRS dust map
    data= data[data['LOCATION_ID'] != 4266] #240,-18
    data= data[data['LOCATION_ID'] != 4331] #5.5,-14.2
    data= data[data['LOCATION_ID'] != 4381] #5.2,-12.2
    data= data[data['LOCATION_ID'] != 4332] #1,-4
    data= data[data['LOCATION_ID'] != 4329] #0,-5
    data= data[data['LOCATION_ID'] != 4351] #0,-2
    data= data[data['LOCATION_ID'] != 4353] #358,0
    data= data[data['LOCATION_ID'] != 4385] #358.6,1.4
    return data
    
# Define the low-alpha, low-iron sample
def _lowlow_lowfeh(afe):
    # The low metallicity edge
    return -0.5
def _lowlow_highfeh(afe):
    # The high metallicity edge
    return -0.15
def _lowlow_lowafe(feh):
    # The low alpha edge (-0.15,-0.075) to (-0.5,0)
    return (0--0.075)/(-0.5--0.15)*(feh--0.15)-0.075
def _lowlow_highafe(feh):
    # The high alpha edge (-0.15,0.075) to (-0.5,0.15)
    return (0.15-0.075)/(-0.5--0.15)*(feh--0.15)+0.075

def get_lowlowsample():
    """
    NAME:
       get_lowlowsample
    PURPOSE:
       get the RC sample at low alpha, low iron
    INPUT:
       None so far
    OUTPUT:
       sample
    HISTORY:
       2015-03-18 - Started - Bovy (IAS)
    """
    # Get the full sample first
    data= get_rcsample()
    # Now cut it
    lowfeh= _lowlow_lowfeh(0.)
    highfeh= _lowlow_highfeh(0.)
    indx= (data[_FEHTAG] > lowfeh)*(data[_FEHTAG] <= highfeh)\
        *(data[_AFETAG] > _lowlow_lowafe(data[_FEHTAG]))\
        *(data[_AFETAG] <= _lowlow_highafe(data[_FEHTAG]))
    return data[indx]
