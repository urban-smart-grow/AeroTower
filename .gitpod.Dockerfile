FROM gitpod/workspace-python-3.10

RUN sudo install-packages openscad

USER gitpod

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --pre cadquery
RUN python3 -m pip install git+https://github.com/gumyr/cq_warehouse.git#egg=cq_warehouse

RUN npm i -g nodemon