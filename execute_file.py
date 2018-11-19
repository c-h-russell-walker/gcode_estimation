import requests, argparse
import common

parser = argparse.ArgumentParser(description='Ping tool')
parser.add_argument("path")

def read_gcode(fn):
	lines = []
	with open(fn) as f:
		lines = f.read()
	return lines

if __name__ == '__main__':
	args = common.parse_args(parser)
	headers = {
		'candidate-id': args.candidate_id
	}
	request_body = {'gcode': read_gcode(args.path)}
	req = requests.post(url = args.endpoint + "/execute", data=request_body, headers = headers)
	print req.text
