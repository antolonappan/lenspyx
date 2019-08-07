# lenspyx

[![alt text](https://readthedocs.org/projects/lenspyx/badge/?version=latest)](https://lenspyx.readthedocs.io/en/latest)[![Build Status](https://travis-ci.com/carronj/lenspyx.svg?branch=master)](https://travis-ci.com/carronj/lenspyx)

Curved-sky python lensed CMB maps simulation package by Julien Carron.

This allows one to build very easily (if familiar with healpy) lensed CMB simulations.

The package basically provides two methods. Check the [doc](https://lenspyx.readthedocs.io/).

(This implementation is independent from the similar-sounding [lenspix](the https://cosmologist.info/lenspix/) package by A.Lewis)

### Installation

After cloning the repository, build an editable installation with
    
    pip install -e . [--user]

The –-user is required only if you don’t have write permission to your main python installation. A fortran compiler is required for a successful installation.

![ERC logo](https://erc.europa.eu/sites/default/files/content/erc_banner-vertical.jpg)
