### Instructions for setup:

Be sure to be in solution directory.

`cd solution`

Make a [virtualenv](https://pypi.org/project/virtualenv/) in order to pip install requirements.

`mkvirtualenv gcode`

Install requirements (again be sure to be in solution directory).

`pip install -r requirements.txt`

### Instructions for use:

Be sure to be in solution directory.

`cd solution`

In virtualenv (`workon gcode`) run this command with one of the three size options listed.

`CANDIDATE_ID=<CANDIDATE_ID> python run_test_case.py small|medium|large`

Where `<CANDIDATE_ID>` is the supplied unique ID.  To reiterate the three options are 'small', 'medium' and 'large'.

### Solution TODOs:

1. Do more explicit error handling with more messages to user

1. Add unit tests

1. Add more documentation

1. Add more options to command line script in order to run a batch of all three sizes
