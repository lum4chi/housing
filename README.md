# Housing
Data crawler & analysis tools to find housing.

Instruction: crawl some data first, then use notebooks to explore data. ⚠ **Crawl responsibly!** ⚠

## Requirements
Install `pipenv` and run:
> pipenv install

## Crawler
Start Scrapyd daemon:
> scrapyd

Update the crawler of your choice and build the project ("eggify"):
> scrapyd-deploy

Start crawler:
> curl http://localhost:6800/schedule.json -d project=housing -d spider=`spider-name`

Terminate crawler:
> curl http://localhost:6800/cancel.json -d project=housing -d job=`jobid`

Delete project:
> curl http://localhost:6800/delproject.json -d project=housing


## Exploration
Install `plotly` renderer support for `jupyterlab`:
> jupyter labextension install jupyterlab-plotly

Install also widgets to use interactive plots:
> jupyter labextension install @jupyter-widgets/jupyterlab-manager plotlywidget


## Development
Every addition to this code is more than welcomed! Just remember to install the env including devs packages:
> pipenv install --dev


