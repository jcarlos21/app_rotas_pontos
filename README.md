# 🗺️ OSRM + KMZ – Rotas por Pontos

Aplicação web interativa desenvolvida em **Python** com **Streamlit**, **OSRM API** e **streamlit-folium**, que permite criar rotas urbanas passando por ruas, avenidas ou rodovias, com exportação para **KMZ** para visualização no Google Earth.

## ✨ Funcionalidades
- **Upload de arquivos** com múltiplos pontos (`CSV`, `XLSX`, `KML`, `KMZ`) contendo as colunas `NOME`, `LATITUDE`, `LONGITUDE`.
- **Entrada manual** de duas coordenadas no formato `lat, lon`.
- Geração de **rota sequencial** passando por todos os pontos na ordem fornecida.
- Visualização da rota em **mapa interativo responsivo** (via `streamlit-folium`).
- Exportação da rota para **arquivo KMZ** com um clique.
- Escolha do **perfil de rota** (`driving`, `cycling`, `foot`).
- Configuração de **URL OSRM** (usar servidor público ou instância própria).

## 🛠️ Tecnologias e bibliotecas
- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [OSRM](http://project-osrm.org/)
- [Folium](https://python-visualization.github.io/folium/)
- [streamlit-folium](https://github.com/randyzwitch/streamlit-folium)
- [Geopy](https://geopy.readthedocs.io/)
- [SimpleKML](https://simplekml.readthedocs.io/)
- [Shapely](https://shapely.readthedocs.io/)
- [fastkml](https://fastkml.readthedocs.io/)

## 🚀 Como executar
```bash
# Clonar repositório
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO

# Criar e ativar ambiente virtual
python -m venv venv
# Windows
venv\\Scripts\\activate
# Linux/macOS
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
streamlit run app.py
```

## 📂 Estrutura de pastas
```
.
├── app.py              # Aplicação principal (Streamlit)
├── osrm_client.py      # Cliente OSRM para rotas com múltiplos pontos
├── parsers.py          # Leitura e normalização de arquivos CSV/XLSX/KML/KMZ
├── kmz_utils.py        # Função para gerar KMZ a partir de coordenadas
├── geo_utils.py        # Funções auxiliares geoespaciais
├── requirements.txt    # Dependências do projeto
└── README.md           # Documentação do projeto
```
