# bash commands for installing your package

git clone https://github.com/grantseiter/Tax-Cruncher-ARP
cd Tax-Cruncher
conda install PSLmodels::taxcalc PSLmodels::behresp "conda-forge::paramtools>=0.15.1" "bokeh<2.0.0"
pip install -e .
cd taxcalc_arp
pip install -e .