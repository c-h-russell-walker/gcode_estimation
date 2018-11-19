import requests, argparse
import common

parser = argparse.ArgumentParser(description='Ping tool')
parser.add_argument("test_size")

if __name__ == '__main__':
	args = common.parse_args(parser)

	headers = {'candidate-id': args.candidate_id}
	req = requests.get(url = args.endpoint + "/test_case/%s" % args.test_size, headers = headers)
	print req.text
