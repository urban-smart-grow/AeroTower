FROM gitpod/workspace-full

USER gitpod

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --pre cadquery
RUN npm i -g nodemon