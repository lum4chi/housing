# Housing
Data crawler & analysis to find housing.

Instruction: crawl some data first, then use notebooks to explore data.

## Crawler
Start Scrapyd daemon
> scrapyd

Build spider ("eggify")
> scrapyd-deploy

Start job
> curl http://localhost:6800/schedule.json -d project=housing -d spider=immobiliare-milano

Terminate job
> curl http://localhost:6800/cancel.json -d project=housing -d job=`jobid`

Delete project
> curl http://localhost:6800/delproject.json -d project=housing


## Exploration
Install also `plotly` renderer support for `jupyterlab`
> jupyter labextension install jupyterlab-plotly