# NOAA-SST

## NOAA SST Data - Download, Processing and Visualization

Este repositório contém scripts em Python desenvolvidos para:

    🔽 Download automático dos dados diários de Temperatura da Superfície do Mar (SST, do inglês Sea Surface Temperature) disponibilizados pela NOAA (https://www.ncei.noaa.gov/data/sea-surface-temperature-optimum-interpolation/v2.1/access/avhrr);

    🧮 Cálculo das médias mensais de SST a partir dos dados diários;

    📊 Visualização da SST e da anomalia de SST, com destaque para as regiões do Pacífico Equatorial associadas aos fenômenos El Niño / La Niña (áreas Niño 1+2, Niño 3, Niño 3.4 e Niño 4).

Os scripts utilizam bibliotecas como xarray, netCDF4, numpy, matplotlib e cartopy para facilitar o processamento e a visualização dos dados oceânicos.

#### Estrutura do repositório

    Download_NOAA_Data.ipynb: Faz o download dos dados diários de SST da NOAA.

    compute_monthly_mean.ipynb: Processa os dados diários para calcular médias mensais.

    plot_sst_maps.ipynb: Gera mapas da SST e da anomalia de SST, com destaque para as áreas Niño.
