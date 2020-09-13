import logging

import azure.functions as func
import os
import subprocess
import json
import yaml

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    provider = req.params.get('provider')
    file_type = req.params.get('file_type')
    req_body = req.get_json()

    if file_type == 'json':
        template = '/tmp/template.json'
        logging.info('Creating temp file now')
        with open(template, 'w') as outfile:
            json.dump(req_body, outfile, indent=4)
        logging.info('Creating temp file worked')
    elif file_type == 'yaml':
        template = '/tmp/template.yaml'
        with open(template, 'w') as outfile:
            yaml.dump(req_body, outfile, indent=4)

    output = subprocess.run(["checkov", "-f", template, "--framework", provider, "-o", "json", "--quiet"], capture_output=True)

    if os.path.exists(template):
        os.remove(template)
    else:
        print("The file does not exist")
    if output:
        return func.HttpResponse(f"{output.stdout}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
