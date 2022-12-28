FROM gitpod/workspace-full

RUN sudo install-packages openscad

USER gitpod

RUN pip3 install solidpython2