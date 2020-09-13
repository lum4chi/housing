# Housing
Data crawler & analysis tools to find housing.

Instruction: crawl some data first, then use notebooks to explore data.

## Requirements
Install `pipenv` and run:
> pipenv install

## Crawler
Start Scrapyd daemon:
> scrapyd

Build spider ("eggify"):
> scrapyd-deploy

Start crawler:
> curl http://localhost:6800/schedule.json -d project=housing -d spider=immobiliare-milano

Terminate crawler:
> curl http://localhost:6800/cancel.json -d project=housing -d job=`jobid`

Delete project:
> curl http://localhost:6800/delproject.json -d project=housing


## Exploration
Install also `plotly` renderer support for `jupyterlab`:
> jupyter labextension install jupyterlab-plotly  
> jupyter labextension install @jupyter-widgets/jupyterlab-manager plotlywidget


## Development
Every addition to this code is more than welcomed! Just remember to install the env including devs packages:
> pipenv install --dev


