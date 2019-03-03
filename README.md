[![CircleCI](https://circleci.com/gh/alankbi/statsify-api.svg?style=svg&circle-token=c2ffe9a2217c5e449c419594312254feb900cbb9)](https://circleci.com/gh/alankbi/statsify-api)

# Statsify REST API
_See also: [Statsify Website](https://github.com/alankbi/statsify-website) and [Statsify Chrome Extension](https://github.com/alankbi/statsify-extension)_

[Statsify](https://www.statsify.us) is a web application that allows you to view beautiful statistics and info about the web pages and websites you visit, with insights such as the following:

• Ratio of internal vs. outbound links  
• Most frequent words  
• Key phrases  
• Total word count  
• Most frequent pages  
• And more...  

Statsify is available in three formats: a website, a chrome extension, and a public API.

## Installation

To install the Statsify API locally, type the following into your command line: 

```
git clone https://github.com/alankbi/statsify-api.git   
cd statsify-api
# Recommended to create a virtual environment first
pip install -r requirements.txt
```

A list of the requirements can be found [here](https://github.com/alankbi/statsify-api/blob/master/requirements.txt). 

## Running Locally

To run the Statsify API on Flask's development server, you can use the following: 

`python api.py`

To run using gunicorn: 

`gunicorn api:app`

With multiple workers: 

`gunicorn api:app --workers 2`

Once your local server is running, you can now access the API at `localhost:PORT`. For details about the API endpoints, see [here](https://www.statsify.us/api). 

Example call: `localhost:8000/page?url=alanbi.com`


## Usage Tracking Configuration

Your API usage statistics can be seen at `/dashboard/overview`. To configure the admin password or the path to your database (such as if you wanted to use PostgreSQL instead of the default SQLite), you can set the `STATSIFY_DASHBOARD_PASSWORD` and `STATSIFY_DB_URL` environment variables to your machine; when run, the [api.py](https://github.com/alankbi/statsify-api/blob/master/api.py) file creates the [config.cfg](https://github.com/alankbi/statsify-api/blob/master/config_template.cfg) file from these values in order to keep them hidden from commit history. For more details about the dashboard, see [here](https://flask-monitoringdashboard.readthedocs.io/en/master/). 

## Contributing 

Feel free to submit an issue or pull request if you find a bug or would like to add a feature. If you're adding large amounts of code, please be sure to include unit tests as well. 

## Contact
Please reach out to me at [alan.bi326@gmail.com](mailto:alan.bi326@gmail.com) if you have any questions or feedback! 
