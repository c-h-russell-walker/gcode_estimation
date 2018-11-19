from argparse import ArgumentParser
import logging
import sys

from constants import TEST_CASE_SIZES
from gcode_estimator_client import GcodeEstimatorClient


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    parser = ArgumentParser()
    parser.add_argument('size', type=unicode)

    args = parser.parse_args()

    size = args.size
    if size not in TEST_CASE_SIZES:
        raise RuntimeError('Size must be in {}'.format(TEST_CASE_SIZES))

    else:
        gc_client = GcodeEstimatorClient()

        s3_url, test_case_id = gc_client.get_test_case(size='small')

        gcode_data = gc_client.get_gcode_data(url=s3_url)

        estimate, _ = gc_client.execute(gcode_data)

        ground_truth, timeout, already_completed = gc_client.post_estimate(
            estimate=estimate,
            test_case_id=test_case_id
        )

        logger.info(
            'ground_truth: {} timeout: {} already_completed: {}'.format(
                ground_truth, timeout, already_completed
            )
        )


if __name__ == '__main__':
    main()
