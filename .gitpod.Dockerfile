FROM gitpod/workspace-full

RUN sudo install-packages openscad

USER gitpod

RUN pyenv install 3.10.0
RUN pyenv global 3.10.0
RUN pyenv rehash

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --pre cadquery
RUN python3 -m pip install git+https://github.com/gumyr/cq_warehouse.git#egg=cq_warehouse

RUN npm install --global nodemon