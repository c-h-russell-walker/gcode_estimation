import requests, argparse
import common

parser = argparse.ArgumentParser(description='Ping tool')
parser.add_argument("estimate", type=float)
parser.add_argument("test_case_id", type=str)

if __name__ == '__main__':
	args = common.parse_args(parser)

	headers = {'candidate-id': args.candidate_id}
	data = {'estimate': args.estimate, 'test_case_id': args.test_case_id}
	req = requests.post(url = args.endpoint + "/test_case", data=data, headers = headers)
	print req.text
