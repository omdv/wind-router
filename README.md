# Overview

Vectorized wind routing for sail boats using [geovectorslib](https://github.com/omdv/geovectors). **Work in Progress.**

![Build](https://github.com/omdv/wind-router/workflows/Build/badge.svg)
[![Coverage Status](https://img.shields.io/coveralls/omdv/wind-router/master.svg)](https://coveralls.io/r/omdv/wind-router)
[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/omdv/wind-router.svg)](https://scrutinizer-ci.com/g/omdv/wind-router/?branch=master)

### Screenshots / Progress

- Visualization of barbs from grib files
- Great circle route with geovectorslib
- Vectorized isochrone method for high speed/resolution
- Visualization of best route, only at fixed forecast hour
![Pages](https://github.com/omdv/wind-router/blob/master/screenshots/map.png)


## Requirements
* Python 3.7+

## Installation
`make install`

## Usage
`python app.py`

## References
- [Henry H.T. Chen's PhD Thesis](http://resolver.tudelft.nl/uuid:a6112879-4298-40a6-91c7-d9a431a674c7)
- Modeling and Optimization Algorithms in Ship Weather Routing, doi:10.1016/j.enavi.2016.06.004
- Optimal Ship Weather Routing Using Isochrone Method on the Basis of Weather Changes, doi:10.1061/40932(246)435
- Karin, Todd. Global Land Mask. October 5, 2020. doi:10.5281/zenodo.4066722
- [GFS grib2 filter](https://nomads.ncep.noaa.gov/)
- [Boat polars - 1](https://jieter.github.io/orc-data/site/)
- [Boat polars - 2](https://l-36.com/polar_polars.php)