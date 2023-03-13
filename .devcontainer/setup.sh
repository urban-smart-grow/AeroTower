sudo apt update
sudo apt install openscad -y

python3 -m pip install --upgrade pip
python3 -m pip install --pre cadquery
python3 -m pip install git+https://github.com/gumyr/cq_warehouse.git#egg=cq_warehouse

npm install --global nodemon