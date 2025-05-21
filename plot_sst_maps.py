# Plotar a Média Mensal da Temperatura da Superfície do Mar (SST)

# Importando as Bibliotecas
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from matplotlib.colors import ListedColormap, BoundaryNorm
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import os
import glob
from shapely.geometry import Polygon
import cartopy.crs as ccrs
#------------------------------------------------------------------------------
# Diretório onde estão os dados organizados como NOAA_SST/ano/mês/
input_dir = glob.glob("NOAA_SST_MENSAL/*.nc")
# Diretório para salvar os arquivos mensais
output_dir = "Plot_NOAA/stt"
os.makedirs(output_dir, exist_ok=True)
#------------------------------------------------------------------------------    
# Coordenadas das regiões Niño
regioes_nino = [
    {
        "nome": "Nino 1+2",
        "coords": [(-90, 0), (-80, 0), (-80, -10), (-90, -10)]
    },
    {
        "nome": "Nino 3",
        "coords": [(-150, 5), (-90, 5), (-90, -5), (-150, -5)]
    },
    {
        "nome": "Nino 3.4",
        "coords": [(-170, 5), (-120, 5), (-120, -5), (-170, -5)]
    },
    {
        "nome": "Nino 4",
        "coords": [(-200, 5), (-150, 5), (-150, -5), (-200, -5)]
    },
]

# Lista de polígonos (shapely)
nino_polygons = [Polygon(r["coords"]) for r in regioes_nino]
#------------------------------------------------------------------------------
for file in input_dir:
    # Ano e Mês do Plot
    data_plot = file.split('\\')[1].split('_')[1].strip('.nc')
    data_plot = data_plot[:4] + '_' + data_plot[4:]
    
    # Cria o caminho do diretório de saída: Plot_NOAA/ano
    year_dir = os.path.join(output_dir, f"{data_plot[:4]}")
    os.makedirs(year_dir, exist_ok=True)  # Cria os diretórios se não existirem

    # Abrir arquivo de média mensal
    ds = xr.open_dataset(file)
    
    # Corrige a longitude para centralizar no Pacífico
    ds = ds.assign_coords(lon=(((ds.lon + 180) % 360) - 180))
    ds = ds.sortby('lon')
    sst = ds['sst'].squeeze()
    
    # Define os níveis e a paleta de cores com branco no início
    levels = np.arange(0, 33, 1)  # 0, 2, 4, ..., 30
    colors = ['white'] + plt.cm.jet(np.linspace(0, 1, len(levels) - 1)).tolist()
    cmap = ListedColormap(colors)
    norm = BoundaryNorm(boundaries=levels, ncolors=len(colors))
    
    # Figura
    fig = plt.figure(figsize=(12, 6))
    proj = ccrs.PlateCarree(central_longitude=180)
    ax = plt.axes(projection=proj)
    
    # Contorno
    cf = ax.contourf(ds['lon'], ds['lat'], sst,
                     levels=levels, cmap=cmap, norm=norm,
                     transform=ccrs.PlateCarree())
    
 # =============== Adiciona elementos do mapa =========================================================================== 
    ax.coastlines()
    ax.add_feature(cfeature.LAND, facecolor='lightgray')
    ax.set_global()
    # Adiciona os polígonos das regiões Niño
    for poly, reg in zip(nino_polygons, regioes_nino):
        ax.add_geometries([poly], crs=ccrs.PlateCarree(),
                          facecolor='none', edgecolor='black', linewidth=1.5)
        # Posiciona o nome logo abaixo do centro do polígono
        x, y = poly.centroid.x, poly.centroid.y
        ax.text(x, y - 6, reg["nome"], transform=ccrs.PlateCarree(),
                fontsize=9, ha='center', va='top')
 # ======================================================================================================================================= 
    # === Ajusta TICKS para LAT e LON ===
    
    # Latitudes padrão
    yticks = np.arange(-90, 91, 30)
    ax.set_yticks(yticks, crs=ccrs.PlateCarree())
    ax.yaxis.set_major_formatter(LATITUDE_FORMATTER)
    
    # Longitudes ajustadas ao centramento
    xticks_deg = [-0.001, -60, -120, 180, 120, 60, 0]  # Em graus (centralizado em 180°)
    xtick_labels = ['0', '60°W', '120°W', '180', '120°E', '60°E', '0']  # Correspondentes
    
    ax.set_xticks(xticks_deg, crs=ccrs.PlateCarree())
    ax.set_xticklabels(xtick_labels)
    
    # Ticks externos
    ax.tick_params(labelsize=10, direction='out')
    
    # Título e barra de cores
    ax.set_title(f"Média Mensal SST - {data_plot}", fontsize=14)
    cbar = plt.colorbar(cf, ax=ax, orientation='horizontal', pad=0.05, aspect=50, shrink=0.5)
    cbar.set_label("°C")
    
    plt.tight_layout()
    
    # Nome do arquivo de saída
    nome_saida = f"SST_{data_plot}"
    caminho_saida = os.path.join(year_dir, nome_saida)
    plt.savefig(caminho_saida, dpi=400)
    print(f"✅ Plot SST mensal de {data_plot} salva: {caminho_saida}")
plt.show()
