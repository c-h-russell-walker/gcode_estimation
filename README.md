# Gcode Completion Time Estimation Challenge

In this challenge, you will estimate the time it takes for a simulated 3D printer to complete a given set of machine instructions.

## Solution:
[Solution](/solution)

## Problem Statement

[Gcode](https://en.wikipedia.org/wiki/G-code) is machine code that is often used to control automated manufacturing tooling, such as 3D printers. Each line of gcode describes a single action, which will take a finite period of time to execute (often over a second). A single gcode file may have millions of commands, so it can take a long time to complete (often hours). For planning purposes, we often want to accurately estimate how long a gcode file will take to execute on a real machine, without actually executing it. This is nontrivial because the machine itself applies control and decides how to move. For example, it may decelerate near sharp corners to avoid overshooting. Your mission, should you choose to accept it, is to algorithmically estimate the time-to-completion of a given gcode file.

We have created a virtual 3D printer simulator to provide ground-truth time-to-completion statistics for arbitrary gcode. You can use our API to develop and test your solution. Information about this API, as well as our simplified gcode specification are provided below in the appendix.

## Getting started

We have provided a few Python scripts to demonstrate different interactions with our API. They are intended to be a reference. Feel free to take it or leave it; use whatever tools you see prefer!

### Installation

Make sure you have Python installed on your system, along with the 'requests' module.

```
$ pip install requests
```

You should also add your candidate identifier to an environment variable to avoid having to include it with every command line invocation (see common.py);

```
$ export CANDIDATE_ID=[your candidate ID]
```

### Usage

```
# ping our server, should return 'pong' if everything is working correctly
$ python ping.py

# Execute inline-specified gcode, should return a json object with execution_time and lines_received
$ python execute.py 'G00 X10' 'G00 Y10'

# Execute gcode from a file, should return a json object with execution_time and lines_received
$ python execute_file.py test_cases/test_small.gcode

# Request a small test case, should return a json object with test_case_id and url
$ python request_test_case.py small

# Post a time-estimate of 10 seconds for test case with ID cd456d14-4989-4134-8174-b9c75232be65
$ python post_estimate.py 10.0 cd456d14-4989-4134-8174-b9c75232be65
```

## FAQs

### Is there a time limit?

No, there's no strict time limit. That said, your time is valuable, and we don't want to waste it! We anticipate this should take roughly an hour to complete a decent solution. Feel free to spend some time interacting with our API to better characterize execution time and improve your model, but you don't need to spend all day on this.

### How good should my solution be?

That's up to you. Perfect solutions are possible, but not required. One naive solution which can easily be implemented in under an hour gives on average under 5% error on large test cases. However, this solution has high variance on small test cases, often returning estimates with over 25% error.

### What if I have an issue with the API?

Please let us know so we can investigate.

### I'm done, now what?

Please send us your code for review.

### How is my solution evaluated?

Once you complete our challenge, we will review both our server logs and your source code. We will mostly ignore any test case estimate posts where response["timeout"] or response["already_completed"] are true. We will primarily review several of your most recent successful posts to evaluate the performance of your algorithm, so once you perfect your code, you should run it a few times on small, medium, and large test cases!

# Appendix

## Gcode Definition

For this challenge, we will consider a simplified subset of gcode. Specifically, there will be one command, the "rapid positioning" command G00. Since 3D printers typically have 3 axes of head motion, plus an extruder, we will consider four axes X, Y, Z, and E. All axes are provided absolute positions (not relative to current position).

- **X:** The X-axis of the print head (in mm). Controls side-to-side positioning of the print head if you face the printer.
- **Y:** The Y-axis of the print head (in mm). Controls front-to-back positioning of the print head if you face the printer.
- **Z:** The Z-axis of the print bed (in mm). This controls the up-down positioning of the print bed relative to the print head.
- **E:** The "extrusion axis". This is the total amount of material extruded by the print head (in mm). If command E to position 10 from position 0, 10mm of filament is extruded. Keep in mind that this is an _absolute_ coordinate space, so commanding E to position 10 while already at position 10 would extrude no filament.

Notes:
- As is typical of gcode, each axis is optional. Omitted axes are supposed to simply stay where they are. For example, if you command "G00 Z10" you want the print bed to move, but the print head and extuder should remain stationary.
- At the beginning of each file, the printer starts at state (X=0, Y=0, Z=0, E=0)
- The max state is: (X=100, Y=100, Z=100, E=1,000,000)
- The min state is: (X=-100, Y=-100, Z=-100, E=0)
- Any inputs outside of these bounds will be clipped to the bounds
- Each line begins with the string "G00" followed axis names and desired positions
- The value for each axis comes immediately after the axis name, with no space, and may be either a float or integer value ("X1" is equvalent to "X1.0")
- Comments are indicated with the "#" character. Anything after a "#" will be ignored
- The axes are always provided in the order X, Y, Z, E. Providing out-of-order axes leads to undefined behavior.
- Each axis is expected to linearly vary with respect to other axes over the movement (but not necessarily with respect to time). In other words, if from (X=0, Y=0, Z=0, E=0) you command "G00 X10 E20", when the extruder is at position (X=5) it should also be at position (E=10).

Examples:
```
G00 X10.0 Y10 # Move to position X=10, Y=10. Z=0, E=0 implied by omission.
G00 Z5.0 # Move to position Z=5. X=10, Y=10, E=0 implied by omission.
G00 E10 # Extrude 10mm of filament. X=10, Y=10, Z=5 implied by omission.
```

You can see more complete examples in the test_cases directory.

## API Protocol

We have created a virtual 3D printer simulator which can interpret gcode and return the execution time of that gcode. You can interact with this simulator via a simple API which is detailed here.

### Endpoints

All authenticated endpoints require the 'candidate-id' header parameter to be defined with the key we provide you. All such endpoints will return:
- 'Invalid candidate-id' if your candidate is invalid or malformed
- 'No candidate-id header found' if the candidate-id header parameter is not present

#### GET /hello

Notes:
- Authenication **not** required

Returns:
- 'Hello, World!'

#### GET /ping

Notes:
- See ping.py
- Authenication required

Returns:
- 'pong' if you include your valid candidate ID

#### POST /execute

Notes:
- See execute.py and execute_file.py
- Authenication required
- Use this endpoint to interact with our printer simulator
- A ten second delay is intentionally included on all responses! This represents the fact that executing gcode on a real printer is not an instantaneous process.

Accepts:
- Json encoded body data with newline-separated gcode in the 'gcode' property. Example: {'gcode':'G00 X10\nG00 Y5'}

Returns
- A json object with execution time (in seconds) and the line count of received gcode. E.g. {"execution_time":0,"lines_received":1}
- 'Gcode parse error on line index [X]' if the input gcode does not conform the the above described specification.
- 'Input gcode must be a newline-separated string' if your gcode is not a string
- 'No gcode decoded' if the body['gcode'] field is empty

#### GET /test_case/[small|medium|large]

Notes
- See request_test_case.py
- Authenication required
- Query this endpoint to receive example gcode files/test cases
- You are not penalized for requesting test cases without posting an estimate, but please avoid hammering this endpoint with a high request volume

Returns
- A json object with the URL of the gcode file, and the test case identifier. E.g. {"url":"https://s3.amazonaws.com/interview-gcode/79fd40ca-65bf-40af-8c2b-c9cefea4eafe.gcode","test_case_id":"30e642b8-ec83-4692-b4ad-ef1891750fb1"}
- You will have to make a separate get request to the provided URL to access the actual Gcode
- 'Unexpected test size requested' if you request a URL ending in something other than "small", "medium", or "large"
- 'Internal server error' if something goes wrong with test case generation. Don't worry if this happens once or twice, but let us know if you see it with high frequency.

#### POST /test_case

Notes
- See post_estimate.py
- Authenication required
- Post to this endpoint to return the time-to-completion calculated by your algorithm
- After some amount of time (several days), we will delete the test case from our server!

Accepts
- Json encoded body data with:
	- Your time estimate in seconds in the 'estimate' property
	- The test case identifier from the source test case (returned from GET /test_case/[size]) in the 'test_case_id' property
	- Example: {'estimate': 10.0, 'test_case_id': ed482882-b590-4d3b-8743-88d2c8261c93}

Returns
- A json string with:
	- The ground-truth time-to-completion for the specified test case in the 'ground_truth' field
	- A boolean flag in the 'timeout' field which is true if the specified test case was requested greater than 15 seconds prior to posting the estimate
	- A boolean flag in the 'already_completed' field which is true if an estimate for the specified test case was already posted
- 'Invalid test case id (not provided to user)' if you request a test case which has not been provided to you
- 'Invalid test_case_id (format doesn't match expectation)' if your test_case_id is malformed
- 'test_case_id not found in post data' if the body['test_case_id'] field is empty
- 'Estimate not found in post data' if the body['estimate'] field is empty

