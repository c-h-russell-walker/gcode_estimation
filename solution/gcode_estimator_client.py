import json
import logging
import os
import sys

import requests

from constants import TEST_CASE_SIZES


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


"""
Use case:

gc_client = GcodeEstimatorClient()

s3_url, test_case_id = gc_client.get_test_case(size='small')

gcode_data = gc_client.get_gcode_data(url=s3_url)

estimate, _ = gc_client.execute(gcode_data)

resp = gc_client.post_estimate(estimate=estimate, test_case_id=test_case_id)

"""


class GcodeEstimatorClient(object):

    def __init__(self):
        self.base_url = 'https://gcode-interview.herokuapp.com'
        self.candidate_id = os.environ.get('CANDIDATE_ID')
        self.headers = {
            'candidate-id': self.candidate_id
        }

    def hello(self):
        return requests.get('{}/{}'.format(self.base_url, 'hello'))

    def get(self, url_suffix):
        """
        For use with /ping & /test_case/<SIZE>
        """
        url = '{}/{}'.format(self.base_url, url_suffix)
        return requests.get(
            url=url,
            headers=self.headers,
        )

    def ping(self):
        return self.get(url_suffix='ping')

    def get_test_case(self, size):
        """
        Returns tuple of url to fetch data and corresponding id
        """
        if size not in TEST_CASE_SIZES:
            raise RuntimeError('Size must be in {}'.format(TEST_CASE_SIZES))

        resp = self.get(
            url_suffix='test_case/{}'.format(size)
        )
        resp_json = resp.json()

        logger.info(json.dumps(resp_json, indent=2))

        return resp_json['url'], resp_json['test_case_id']

    def get_gcode_data(self, url):
        """
        For use with AWS S3 links
        Returns gcode data
        """
        resp = requests.get(url)

        logger.info(resp)

        return resp.text

    def post(self, url_suffix, json_data):
        url = '{}/{}'.format(self.base_url, url_suffix)
        return requests.post(
            url=url,
            headers=self.headers,
            json=json_data,
        )

    def execute(self, gcode):
        """
        Returns tuple of execution_time & lines_received
        """
        resp = self.post(
            url_suffix='execute',
            json_data={
                'gcode': gcode,
            }
        )
        resp_json = resp.json()

        logger.info(json.dumps(resp_json, indent=2))

        return resp_json['execution_time'], resp_json['lines_received']

    def post_estimate(self, estimate, test_case_id):
        """
        Returns tuple of ground_truth, timeout & already_completed
        """
        data = {
            'estimate': estimate,
            'test_case_id': test_case_id,
        }
        resp = self.post(
            url_suffix='test_case',
            json_data=data,
        )

        resp_json = resp.json()

        logger.info(json.dumps(resp_json, indent=2))

        return (
            resp_json['ground_truth'],
            resp_json['timeout'],
            resp_json['already_completed']
        )
