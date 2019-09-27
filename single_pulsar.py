# This code was developed by I. Christie (in collaboration with Z. Mitchell).
# If using, make references to the following works:

# i) Christie I. M., Petropoulou M., Mimica P., Giannios D., 2017, MNRAS, 468,
# L26   (https://ui.adsabs.harvard.edu/abs/2017MNRAS.468L..26C/abstract)
#
# ii) Christie I. M., Petropoulou M., Mimica P., Giannios D., 2016, MNRAS, 459,
# 2420  (https://ui.adsabs.harvard.edu/abs/2016MNRAS.459.2420C/abstract)

# This scripts considers the interactions of a single pulsar
# with the accretion disk of Sgr A*. Using several of the few
# free parameters (listed below), the script follows the pulsar
# when it first intercepts the disk, computing the accelerated
# particle distribution at the shock interface. We follow the
# particle distibution as it cools within the local magnetic
# fields of the disk all the way to the accretion timescale all
# while computing the synchrotron spectrum. The final result is
# a plot which displays the temporal evolution of the synchrotron
# spectrum and particle distribution, the former being compared with
# the spectral energy distribution of Sgr A*.

import numpy as np
from scipy.special import kv
import scipy.integrate as integrate
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
import matplotlib.patches as patches
from tables import (synchrotron_log10_f_x,
    synchrotron_log10_x, sgr_a_observations_radio_frequency,
    sgr_a_observations_radio_luminosity, sgr_a_observations_xray_frequency,
    sgr_a_observations_xray_luminosity, sgr_a_observations_IR_frequency,
    sgr_a_observations_IR_luminosity)


#################### Definition of Physical Constants ####################
##########################################################################

# Electron mass in grams.
electron_mass = 9.10938 * (10**-28.)

# Speed of light in cm/seconds.
speed_light = 3 * (10**10.)

# Thomson cross-section in cm^2.
thomson_cross_section = 6.6524 * (10**-25.)

# Electric charge in statcoloumb.
electric_charge = 4.8032068 * (10**-10.)

##########################################################################
##########################################################################


#################### Input Parameters ####################
##########################################################

# Spin-down luminosity of the pulsar in erg/seconds.
spin_down_L = 3. * 10**35.

# Slope of injected particle distribution (assumed to be a power-law).
particle_slope = 2.2

# Fraction of energy imparted to accelerated electrons and magnetic fields.
epsilon_e = 0.1
epsilon_B = 0.1

# Particle number density, in cm^-3, at the Bondi radius.
Bondi_num_den = 10**2

# Minimum Lorentz factor of the injected particle distribution.
gamma_min = 10**3.

# Pericenter distance of the pulsar and Bondi Radius in cm.
pericenter_dist = 5. * 10**(16.)
Bondi_radius = 10**17.

# Alpha-viscosity parameter of the accretion disk (see for more
# details). Used in estimating the accretion timescale (see eqn.
# 3 in Christie et al. 2017).
alpha_viscosity = 0.01

# Pericenter time, i.e. the time it takes the pulsar to traverse
# through the accretion disk, in s.
pericenter_time = 3 * (10**7.) * (pericenter_dist / (10**16.))**(3. / 2.)

# Accretion timescale in seconds.
accretion_time = 600 * pericenter_time * (alpha_viscosity / 0.01)**(-1)

# Time, in seconds, from when the pulsar first intercepts the accretion disk to
# the pericenter time.
timestable = np.array([10**-6, 10**-4, 10**-2, 1, 10, 50, 100, accretion_time /
    pericenter_time]) * pericenter_time

# Magnetic field strength at the pericenter distance in Gauss.
# Note that we follow the parametric scalings provided in the
# Christie et al. 2017.
pericenter_mag_field = 0.007 * np.sqrt((epsilon_B / 0.1) * (Bondi_num_den /
    100.) * (Bondi_radius / (10**17.))) * (pericenter_dist / (10**16.))**(-1)


print("\nPericenter time is " + str(pericenter_time) + " s = " + str(
    pericenter_time / 3600.) + " hr.\n")
##########################################################
##########################################################


#################### Particle Distribution ####################
###############################################################

# Maximum Lorentz factor of particle distribution assuming a Bohm
# acceleration.
gamma_max = 1.4 * (10**9.) * ((epsilon_B / 0.1) * (Bondi_num_den / 100.) *
	(Bondi_radius / (10**17.)))**(-1. / 4.) * (pericenter_dist / (10**16.))**(1. /
    2.)

# Table of Lorentz factors ranging from 1 to gamma_max.
gamma_table = np.logspace(0, np.log10(gamma_max), 99)

# Normalization factor of the injected particle distribution (see eqn. 6).
particle_distribution_norm = epsilon_e * spin_down_L * (particle_slope - 2) / (
    electron_mass * speed_light**2 * (gamma_min**(2 - particle_slope) -
        gamma_max**(2 - particle_slope)))

# Factor b defined just after eqn. 5 in the paper.
b = pericenter_mag_field**2 * thomson_cross_section / (6 * np.pi *
    electron_mass * speed_light)

# Cooling Lorentz factors gc1(t) and gc2(t), defined following eqn. 8 in
# Christie et al. 2017.
gamma_cool_1 = gamma_max / (1 + timestable * b * gamma_max)
gamma_cool_2 = gamma_min / (1 + b * timestable * gamma_min)

# Initialize particle distribution.
particle_distribution = np.zeros((np.shape(timestable)[0], np.shape(gamma_table
    )[0]))
# Initialize an array which stores the different components of the
# piecewise function provided in eqn. 8 of Christie et al. 2017.
f = 0 * gamma_table

# For each time value provided in the timestable, we compute
# the particle distribution at that particular step.
for i in range(np.shape(timestable)[0]):
    # Below, we go through each of the four parts of the piecewise function,
    # provided in eqn. 8, and add it to the existing particle distibution. Note
    # that they are listed in the same order as eqn. 8 and that this if-section
    # corresponds to times below the pericenter time.
    if timestable[i] <= pericenter_time:
        f = (gamma_table > gamma_min) * (gamma_table < gamma_cool_1[i]) * (1 -
            (1 - b * gamma_table * timestable[i])**(particle_slope - 1))
        f[np.isnan(f)] = 0
        particle_distribution[i] += f

        f = 0 * gamma_table
        f = (gamma_cool_1[i] < gamma_table) * (gamma_table < gamma_max) * (1 -
            (gamma_max / gamma_table)**(1 - particle_slope))
        f[np.isnan(f)] = 0
        particle_distribution[i] += f

        f = 0 * gamma_table
        f = (gamma_cool_1[i] < gamma_table) * (gamma_table < gamma_min) * ((1 -
            (gamma_max / gamma_min)**(1 - particle_slope)) * (gamma_min /
            gamma_table)**(1 - particle_slope))
        f[np.isnan(f)] = 0
        particle_distribution[i] += f

        f = 0 * gamma_table
        f = (gamma_cool_2[i] < gamma_table) * (gamma_table < gamma_min) * ((
            gamma_min / gamma_table)**(1 - particle_slope) - (1 - b *
            timestable[i] * gamma_table)**(particle_slope - 1))
        f[np.isnan(f)] = 0
        particle_distribution[i] += f

        particle_distribution[i] *= (particle_distribution_norm *
            gamma_table**(-1 - particle_slope) / (b * (particle_slope - 1)))

    # For times, above the pericenter time, we first interpolate the particle
    # distribution at the pericenter time and then compute the updated
    # particle distribution with the new Lorentz factor following eqn. 9 in
    # Christie et al. 2017.
    else:
        f = 0 * gamma_table
        interp_particle_distribution_tp = interp1d(np.log(gamma_table),
            particle_distribution[np.sum(timestable <= pericenter_time) - 1])
        gamma_large_tp = 1 - b * gamma_table * (timestable[i] -
            pericenter_time)
        f = interp_particle_distribution_tp(np.log(
            gamma_table / gamma_large_tp)) * gamma_large_tp**(-2)
        f[np.isnan(f)] = 0.
        particle_distribution[i] = f

###############################################################
###############################################################


#################### Synchrotron Spectrum ####################
##############################################################

# Below, we create an array of x values tand appropriate F(x) values (see eqn.
# in Rybicki & Lightman). This allows for easier computation of the single
# particle electron emissivity.
f_interp = interp1d(synchrotron_log10_x, synchrotron_log10_f_x)

# Table of photon frequency values in Hertz.
photon_frequency = np.logspace(7, 28, 99)

# Value of x-values (i.e. nu/nu_c) for our chosen Lorentz factors
# and frequency values.
x = np.zeros((np.shape(photon_frequency)[0], np.shape(gamma_table)[0]))
for i in range(np.shape(photon_frequency)[0]):
    x[i] = 4. * np.pi * electron_mass * speed_light * photon_frequency[i] / (3.
    	* electric_charge * pericenter_mag_field * gamma_table**2)

# Single particle synchrotron emissivity (see eqn. in Rybicki
# and Lightman.
p_single = np.zeros((np.shape(photon_frequency)[0], np.shape(gamma_table)[0]))
for i in range(np.shape(photon_frequency)[0]):
    for j in range(np.shape(gamma_table)[0]):

        if (x[i, j] >= 10**-20.) * (x[i, j] <= 100.) == 1:
            p_single[i, j] = (np.sqrt(3.) * (electric_charge**3.) *
                pericenter_mag_field / (electron_mass
            	* (speed_light**2.))) * (10**f_interp(np.log10(x[i, j])))
            pass
        pass
    pass

# Synchrotron power in erg/seconds.
synchrotron_pow = np.zeros((np.shape(timestable)[0],
    np.shape(photon_frequency)[0]))
for i in range(np.shape(timestable)[0]):
    for j in range(np.shape(photon_frequency)[0]):
        integrand = gamma_table * (np.log(gamma_table[1]) -
            np.log(gamma_table[0])) * p_single[j] * particle_distribution[i]
        synchrotron_pow[i, j] = photon_frequency[j]*np.sum(integrand)
        pass
    pass
##############################################################
##############################################################

####### Plots of Particle Distribution & Synchrotron Spectrum #######
#####################################################################

fig, axs = plt.subplots(2, 1)
for i in range(np.shape(timestable)[0]):
    axs[0].loglog(gamma_table, particle_distribution[i])
    axs[0].set_xlim([10**1., 10**10.])
axs[0].set_xlabel(r'$\gamma$')
axs[0].set_ylabel(r'N$^e$($\gamma , t$)')

for i in range(np.shape(timestable)[0]):
    axs[1].loglog(photon_frequency, synchrotron_pow[i])
    axs[1].set_xlim([10**7., 10**26.])
    axs[1].set_ylim([10**26., 10**37.])
# axs[1].loglog(1.4*(10**14.), 6*1.15*(10**34.), 'bx')
axs[1].loglog(10**sgr_a_observations_radio_frequency,
    10**sgr_a_observations_radio_luminosity, 'x', color='black')
axs[1].loglog(10**sgr_a_observations_IR_frequency,
    10**sgr_a_observations_IR_luminosity, 'x', color='lime')

# Creates a rectangular patch representing Chandra's
# X-ray observations.
xray_nu_1 = 10**sgr_a_observations_xray_frequency[0]
xray_nu_2 = 10**sgr_a_observations_xray_frequency[1]
xray_lumionsity_1 = 10**sgr_a_observations_xray_luminosity[0]
xray_lumionsity_2 = 10**sgr_a_observations_xray_luminosity[1]
rect = patches.Rectangle((xray_nu_1, xray_lumionsity_1), xray_nu_2 - xray_nu_1,
    xray_lumionsity_2 - xray_lumionsity_1, linewidth=1, edgecolor='magenta',
    facecolor='magenta', alpha=0.5)
# Add the patch to the Axes
axs[1].add_patch(rect)
axs[1].set_xlabel(r'$\nu$ (Hz)')
axs[1].set_ylabel(r'$\nu \, L_\nu$ (erg/s)')

fig.tight_layout()
plt.show()
#####################################################################
#####################################################################
