import requests, argparse
import common

parser = argparse.ArgumentParser(description='Ping tool')
parser.add_argument("command", nargs="+")

if __name__ == '__main__':
	args = common.parse_args(parser)

	headers = {'candidate-id': args.candidate_id}
	data = {'gcode': '\n'.join(args.command)}
	req = requests.post(url = args.endpoint + "/execute", data=data, headers = headers)
	print req.text