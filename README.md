# AeroTower

The AeroTower is inspired by similar projects like [this one](https://www.thingiverse.com/thing:2403922),
but makes use of aeroponics instead of hydroponics. 
If you want to know more about it or build your own, [head over to the documentation site](https://urban-smart-grow.github.io/website/aerotower)

## Getting Started

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/urban-smart-grow/AeroTower)

The easiest way to get started is to edit this repository on gitpod. 
Alternatively you can spin up a local environment with the help of [devcontainers](https://code.visualstudio.com/docs/devcontainers/containers).

Once your workspace environment is set up, open the file of the part you want to modify from the `/src`-folder.
If you run this file with python, a `STL`-file is generated and saved to the `/exports`-folder. 
You can open these `STL`-files beside your code to view your changes.

You can use nodemon to automate the rendering process. The `STL`-viewer will update automatically.

`nodemon src/body.py`

## Trivia

This project is a complete redesign of [this project](https://github.com/mfillmer/3d-modelling/tree/master/smart_grow/aero_tower).
The legacy project was more of a playground and was built upon SolidPython. 

This project is more focused and uses [CADQuery 2](https://cadquery.readthedocs.io/en/latest/index.html) 
with the excellent [cq_warehouse plugin](https://cq-warehouse.readthedocs.io/en/latest/).
