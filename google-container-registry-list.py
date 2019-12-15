#!/usr/bin/env python3
import argparse
import json
import requests


""" curl examples
# Reference: https://stackoverflow.com/questions/46450200/how-to-obtain-gcr-access-token-with-python-listing-docker-images
curl -s https://gcr.io/v2/{project-id}/{image-name}/tags/list -H 'Authorization: Basic {}'
"""


def get_token():
    import os
    with open(os.getenv('GOOGLE_APPLICATION_CREDENTIALS')) as f:
        from base64 import b64encode
        return b64encode(f'_json_key:{f.read()}'.encode()).decode()
    return None


def fetch_digests(index_url, token, project_id, image_name):
    return requests.get(
        f'{index_url}/v2/{project_id}/{image_name}/tags/list',
        headers={'Authorization': f'Basic {token}'}
    ).json()


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('project', help='ID of project to list versions of')
    p.add_argument('image', help='Name of image to list versions of')
    p.add_argument('-t', '--token', help='Auth token to use (automatically fetched if not specified)')
    p.add_argument('-i', '--index-url', default='https://gcr.io')

    args = p.parse_args()
    token = args.token or get_token()

    digests = fetch_digests(args.index_url, token, args.project, args.image)
    print(json.dumps(digests, indent=2))
