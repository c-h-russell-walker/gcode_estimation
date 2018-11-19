import os

def parse_args(parser):
	parser.add_argument("--candidate_id", default=None)
	parser.add_argument("--endpoint", default="https://gcode-interview.herokuapp.com")
	args = parser.parse_args()
	if args.candidate_id == None and "CANDIDATE_ID" in os.environ:
		args.candidate_id = os.environ['CANDIDATE_ID']
	if 'GCODE_INTERVIEW_ENDPOINT' in os.environ:
		args.endpoint = os.environ['GCODE_INTERVIEW_ENDPOINT']
	print "Candidate ID:", args.candidate_id
	print "Endpoint:", args.endpoint
	return args
