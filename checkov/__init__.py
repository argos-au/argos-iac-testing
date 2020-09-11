import logging

import azure.functions as func
import os
import subprocess


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    output = subprocess.run(["checkov", "-f", "./checkov/template.json", "--framework", "arm", "-o", "json"], capture_output=True)
    if output:
        return func.HttpResponse(f"{output}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
