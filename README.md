# pulsar-accretion-disk-interactions

This repository contains several scripts used investigating the non-thermal emission produced from neutron stars interacting with the accretion disk of Sgr A* (see description below). If using, make appropriate references to the following works:

i) Christie I. M., Petropoulou M., Mimica P., Giannios D., 2017, MNRAS, 468, L26 (https://ui.adsabs.harvard.edu/abs/2017MNRAS.468L..26C/abstract)

ii) Christie I. M., Petropoulou M., Mimica P., Giannios D., 2016, MNRAS, 459, 2420 (https://ui.adsabs.harvard.edu/abs/2016MNRAS.459.2420C/abstract)

## Introduction

At the center of our Galaxy lies a sumpermassive black hole (BH), roughly a million times more massive than our Sun, denoted as Sgr A* [3, 7]. Observations of Sgr A*, from radio frequencies up to X-rays, are made possible through the detection of photons (i.e. light) emitted by large bodies of gas surrounding the BH. This gas is thought to form an accretion disk, i.e. donut, surrounding, and eventually feeding, the BH. 

The emission detected from the accretion disk is produced from a variety of mechanisms, with low-frequencies produced from synchrotron emission while the X-rays are produced from thermal Bremsstrhalung [1]. Despite the large observational campaigns however, properties of the disk (e.g. number density, temperature, and speed of the gas) remain elusive. To combat this problem, we may use indirect methods of probing the accretion. One example is to study the interactions, and subsequent emission, of the disk with stars orbiting the BH [5, 6, 8]. 

One type of star we consider here is a neutron star (NS) (for a more detailed description, see [5]). A large population of these stars have been proposed to reside in our Galactic center, which could potentially explain the NASA Fermi-LAT observed GeV excess [2], but are obscured by large amounts of dust [4, 9]. If NS were to intercept the accretion disk gas, they could inject highly relativistic particle within the disk. The particles would be left to cool and radiate, via synchrotron emission, within the local magnetic fields of the disk. Detection of this emission would allow one to constrain properties of both the accretion disk and the NS!

## Before Running

You'll need to use [`poetry`](https://github.com/sdispater/poetry) to install the dependencies:
```bash
$ poetry install

$ poetry init
<answer the prompts, not adding dependencies interactively>

$ poetry add package1 package2 ... packageN

$ poetry run python3 _____.py
```


## Citations

[1] Baganoff F. K. et al., 2003, Astrophysical Journal, 591, 891 (https://ui.adsabs.harvard.edu/abs/2003ApJ...591..891B/abstract)

[2] Brandt T. D., Kocsis B., 2015, Astrophysical Journal, 812, 15 (https://ui.adsabs.harvard.edu/abs/2015ApJ...812...15B/abstract)

[3] Chatzopoulos S., Fritz T. K., Gerhard O., Gillessen S., Wegg C., Genzel R., Pfuhl O., 2015, MNRAS, 447, 948 (https://ui.adsabs.harvard.edu/abs/2015MNRAS.447..948C/abstract)

[4] Chennamangalam J., Lorimer D. R., 2014, MNRAS, 440, L86     (https://ui.adsabs.harvard.edu/abs/2014MNRAS.440L..86C/abstract)

[5] Christie I. M., Petropoulou M., Mimica P., Giannios D., 2017, MNRAS, 468, L26 (https://ui.adsabs.harvard.edu/abs/2017MNRAS.468L..26C/abstract)

[6] Christie I. M., Petropoulou M., Mimica P., Giannios D., 2016, MNRAS, 459, 2420 (https://ui.adsabs.harvard.edu/abs/2016MNRAS.459.2420C/abstract)

[7] Genzel R., Eisenhauer F., Gillessen S., 2010, Reviews of Modern Physics, 82, 3121 (https://ui.adsabs.harvard.edu/abs/2010RvMP...82.3121G/abstract)

[8] Giannios D., Lorimer D. R., 2016, MNRAS, 459, L95          (https://ui.adsabs.harvard.edu/abs/2016MNRAS.459L..95G/abstract)

[9] Wharton R. S., Chatterjee S., Cordes J. M., Deneva J. S., Lazio T. J. W., 2012, Astrophysical Journal, 753, 108 (https://ui.adsabs.harvard.edu/abs/2012ApJ...753..108W/abstract)
