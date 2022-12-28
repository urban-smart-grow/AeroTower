FROM gitpod/workspace-full

RUN sudo install-packages openscad
RUN pip install -r requirements.txt