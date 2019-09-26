#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
File: zenodo_api_access.py
Created Date: September 22nd 2019
Author: ZL Deng <dawnmsg(at)gmail.com>
---------------------------------------
Last Modified: 22nd September 2019 7:45:14 pm
'''

import requests
import json
import click
from os import path


@click.command()
@click.argument("token", type=str)
# @click.option("-t", "--type",
#               required=True,
#               type=click.Choice(["dataset", "software", "publication"]),
#               help="The type of the data to uploade")
@click.argument("metadata", type=click.Path(exists=True))
@click.argument("files", type=click.Path(exists=True), nargs=-1)
@click.option("-s", "--sandbox", is_flag=True,
              help="Test in sandbox for uploading")
def upload(token, metadata, files, sandbox):
    global BASE_URL
    BASE_URL = "https://sandbox.zenodo.org" if sandbox else "https://zenodo.org"
    global ACCESS_TOKEN
    ACCESS_TOKEN = token
    deposit_id = get_deposit_id(metadata)
    for file in files:
        filename = path.basename(file)
        upload_data = {'filename': filename}
        upload_file = {'file': open(file, 'rb')}
        r = requests.post("{}/api/deposit/depositions/{}/files".format(BASE_URL, deposit_id),
                          params={
            'access_token': ACCESS_TOKEN},
            data=upload_data,
            files=upload_file)
        print("Uploading {}".format(filename))
        if r.status_code >= 400:
            raise RuntimeError("Error occurred while uploading {}, status code: {}".format(filename,
                                                                                           str(r.status_code)))
    if click.confirm('''Do you want to publish the uploaded files? 
 Note, once a deposition is published, you can no longer delete it.'''):
        publish(deposit_id)
        print("Your deposition has been published!")
        print(
            "You can check your deposition here: {}/record/{}".format(BASE_URL, deposit_id))
        return
    print("Uploading done!")
    print("You can check your deposition here: {}/record/{}".format(BASE_URL, deposit_id))


def get_deposit_id(metadata):
    headers = {"Content-Type": "application/json"}
    with open(metadata, "r") as fh:
        metadata_content = json.load(fh)
        metadata_content = json.dumps(metadata_content, ensure_ascii=True)
    r = requests.post("{}/api/deposit/depositions".format(BASE_URL),
                      params={'access_token': ACCESS_TOKEN},
                      data=metadata_content,
                      json={},
                      headers=headers)

    if r.status_code >= 400:
        raise RuntimeError("Error occurred while creating deposit ID, status code: {}".format(
                           str(r.status_code)))

    deposit_id = r.json()['id']
    return deposit_id


def publish(deposit_id):
    r = requests.post("{}/api/deposit/depositions/{}/actions/publish".format(BASE_URL, deposit_id),
                      params={'access_token': ACCESS_TOKEN})
    if r.status_code >= 400:
        raise RuntimeError("Error occurred while publishing your deposition, status code: {}".format(
                           str(r.status_code)))


if __name__ == '__main__':
    upload()
