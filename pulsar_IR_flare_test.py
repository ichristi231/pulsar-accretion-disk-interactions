import numpy as np
from scipy.special import kv
import scipy.integrate as integrate
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt


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
spin_down_L = 10**35.

# Slope of injected particle distribution (assumed to be a power-law).
particle_slope = 2.2

# Fraction of energy imparted to accelerated electrons and magnetic fields.
epsilon_e = 0.1
epsilon_B = 0.1

# Pericenter distance of the pulsar and Bondi Radius in cm.
pericenter_dist = 10**(15.)
Bondi_radius = 10**17.

# Pericenter time, i.e. the time it takes the pulsar to traverse
# through the accretion disk, in s.
pericenter_time = 3 * (10**7.) * (pericenter_dist / (10**16.))**(3. / 2.)

# Time, in seconds, from when the pulsar first intercepts the accretion disk to
# the pericenter time.
timestable = np.array([10**-6, 10**-4, 10**-2, 1]) * pericenter_time

# Particle number density, in cm^-3, at the Bondi radius.
Bondi_num_den = 10**2

# Magnetic field strength at the pericenter distance in Gauss.
# Note that we follow the parametric scalings provided in the
# paper.
pericenter_mag_field = 0.007 * np.sqrt((epsilon_B / 0.1) * (Bondi_num_den / 100.) * (Bondi_radius / (10**17.))) * (pericenter_dist / (10**16.))**(-1)
# print("Magnetic field strength: " + str(pericenter_mag_field) + " G. \n")


# Minimum Lorentz factor of the injected particle distribution.
gamma_min = 10**2.

print("\nPericenter time is " + str(pericenter_time) + " s = " + str(pericenter_time / 3600.) + " hr.\n")

##########################################################
##########################################################


#################### Particle Distribution ####################
###############################################################

# Maximum Lorentz factor of particle distribution assuming a Bohm
# acceleration.
gamma_max = 1.4 * (10**9.) * ((epsilon_B / 0.1) * (Bondi_num_den / 100.) *
	(Bondi_radius / (10**17.)))**(-1. / 4.) * (pericenter_dist / (10**16.))**(1. / 2.)

# Table of Lorentz factors ranging from 1 to gamma_max.
gamma_table = np.logspace(0, np.log10(gamma_max), 99)

# Normalization factor of the injected particle distribution (see eqn. 6).
particle_distribution_norm = epsilon_e * spin_down_L * (particle_slope - 2) / (electron_mass
	* speed_light**2 * (gamma_min**(2 - particle_slope) - gamma_max**(2 - particle_slope)))

# Factor b defined just after eqn. 5 in the paper.
b = pericenter_mag_field**2 * thomson_cross_section / (6 * np.pi * electron_mass * speed_light)

# Cooling Lorentz factors gc1(t) and gc2(t), defined following eqn. 8.
gamma_cool_1 = gamma_max / (1 + timestable * b * gamma_max)
gamma_cool_2 = gamma_min / (1 + b * timestable * gamma_min)

# Initialize particle distribution.
particle_distribution = np.zeros((np.shape(timestable)[0], np.shape(gamma_table)[0]))
# Initialize an array which stores the different components of the
# piecewise function provided in eqn. 8.
f = 0 * gamma_table

# Below, we go through each of the four parts of the piecewise function,
# provided in eqn. 8, and add it to the existing particle distibution. Note
# that they are listed in the same order as eqn. 8.
for i in range(np.shape(timestable)[0]):
    f = (gamma_table > gamma_min) * (gamma_table < gamma_cool_1[i]) * (1 - (1 - b * gamma_table * timestable[i])**(particle_slope - 1))
    f[isnan(f)] = 0
    particle_distribution[i] += f

    f = 0 * gamma_table
    f = (gamma_cool_1[i] < gamma_table) * (gamma_table < gamma_max) * (1 - (gamma_max / gamma_table)**(1 - particle_slope))
    f[isnan(f)] = 0
    particle_distribution[i] += f

    f = 0 * gamma_table
    f = (gamma_cool_1[i] < gamma_table) * (gamma_table < gamma_min) * ((1 - (gamma_max / gamma_min)**(1 - particle_slope)) * (gamma_min / gamma_table)**(1 - particle_slope))
    f[isnan(f)] = 0
    particle_distribution[i] += f

    f = 0 * gamma_table
    f = (gamma_cool_2[i] < gamma_table) * (gamma_table < gamma_min) * ((gamma_min / gamma_table)**(1 - particle_slope) - (1 - b * timestable[i] * gamma_table)**(particle_slope - 1))
    f[isnan(f)] = 0
    particle_distribution[i] += f

    particle_distribution[i] *= (particle_distribution_norm * gamma_table**(-1 - particle_slope) / (b * (particle_slope - 1)))
###############################################################
###############################################################


#################### Synchrotron Spectrum ####################
##############################################################

# Below, we create an array of x values tand appropriate F(x) values (see eqn.
# in Rybicki & Lightman). This allows for easier computation of the single
# particle electron emissivity.
x_store = np.logspace(-20, 2, 99)
f_store = 0 * x_store
for i in range(np.shape(x_store)[0]):
    f_store[i] = x_store[i] * integrate.quad(lambda y: np.exp(y) * kv(5./3., np.exp(y)), np.log(x_store[i]), np.log(10**5.))[0]
f_interp = interp1d(np.log10(x_store), np.log10(f_store))

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
            p_single[i, j] = (np.sqrt(3.) * (electric_charge**3.) * pericenter_mag_field / (electron_mass
            	* (speed_light**2.))) * (10**f_interp(np.log10(x[i, j])))
            pass
        pass
    pass

# Synchrotron power in erg/seconds.
synchrotron_pow = np.zeros((np.shape(timestable)[0], np.shape(photon_frequency)[0]))
for i in range(np.shape(timestable)[0]):
    for j in range(np.shape(photon_frequency)[0]):
        integrand = gamma_table * (np.log(gamma_table[1]) - np.log(gamma_table[0])) * p_single[j] * particle_distribution[i]
        synchrotron_pow[i, j] = photon_frequency[j]*np.sum(integrand)
        pass
    pass
##############################################################
##############################################################

#################### Plots of Particle Distribution & Synchrotron Power ####################
############################################################################################

fig, axs = plt.subplots(2, 1)
for i in range(np.shape(timestable)[0]):
    axs[0].loglog(gamma_table, particle_distribution[i])
axs[0].set_xlabel(r'$\gamma$')
axs[0].set_ylabel(r'N$^e$($\gamma , t$)')

for i in range(np.shape(timestable)[0]):
    axs[1].loglog(photon_frequency, synchrotron_pow[i])
    axs[1].set_xlim([10**7., 10**26.])
    axs[1].set_ylim([10**21., 10**36.])
axs[1].loglog(1.4*(10**14.), 6*1.15*(10**34.), 'bx')
axs[1].set_xlabel(r'$\nu$ (Hz)')
axs[1].set_ylabel(r'$\nu \, L_\nu$ (erg/s)')

fig.tight_layout()
plt.show()
############################################################################################
############################################################################################
