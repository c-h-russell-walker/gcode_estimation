import requests, argparse
import common

parser = argparse.ArgumentParser(description='Ping tool')

if __name__ == '__main__':
	args = common.parse_args(parser)

	headers = {'candidate-id': args.candidate_id}
	req = requests.get(url = args.endpoint + "/ping", headers = headers)
	print "Response:", req.text