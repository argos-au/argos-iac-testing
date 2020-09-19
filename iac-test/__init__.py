import logging

import azure.functions as func
import os
import subprocess
import json
import yaml

def main(req: func.HttpRequest) -> func.HttpResponse:
    provider = req.params.get('provider')
    if ((provider != "arm") and (provider != 'cloudformation')):
        return func.HttpResponse(
            "ERROR: provider = must be arm or cloudformation",
            status_code=400
        )
    file_type = req.params.get('file_type')
    if ((file_type != "json") and (file_type != "yaml")):
        return func.HttpResponse(
            "ERROR: file_type = must be json or yaml",
            status_code=400
        )
    req_body = req.get_json()
    template = ""
    if file_type == 'json':
        template = '/tmp/template.json'
        with open(template, 'w') as outfile:
            json.dump(req_body, outfile, indent=4)
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
        func.HttpResponse.mimetype = 'application/json'
        func.HttpResponse.charset = 'utf-8'
        return func.HttpResponse(output.stdout, status_code=200)
    else:
        return func.HttpResponse(
             "An error happened.",
             status_code=400
        )
