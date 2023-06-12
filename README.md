
# SMS Simulation App Backend

## How to run

#### Step 1: Build Docker image

`docker build -f Dockerfile -t sim-server .`

#### Step 2: Run Docker image

`docker run -it -d --name simserver -p 5000:5000 sim-server`

#### Step 3: To stop client

`docker stop simserver`


## Endpoints

### POST `/sim/start`
Start SMS simulation

Example parameters
```
{
    "numMessages": 1200,
    "failurePct": 10,
    "numSenders": 4
}
```

Output
```
{
    "status": "SUCCESS"
}
```
`status` can  have the following values
```
SUCCESS - Job submission succeeded
INVALID - Invalid parameters
CONFLICT - Simulation is already running
```
### GET `/sim/status`
Retrieves simulation status

Example output:
```
{
    "isActive": true,
    "stats": {
        "avgProcessingTime": 0.33,
        "errors": 2,
        "processed": 6,
        "received": 8
    },
    "status": "SUCCESS"
```
`isActive` indicates whether there is an active job running. true if job is running.

If there is no active job running, `stats` shows the stats of the last run job. 

## Unit tests


#### Step 1: Setup environment

In the root director of the code run -
```
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ pip install pytest
```

#### Step 2: Run the tests
```
(venv) $ pytest -v tests
```
Expected output:

```
=========================================================================================================== test session starts ============================================================================================================
platform darwin -- Python 3.9.6, pytest-7.3.2, pluggy-1.0.0 -- /Users/kmynam/Downloads/Private/adg/backend/venv/bin/python3                                                                                                                                                                                                                      

tests/test_1_sim_start_param_validation.py::test_sim_start_1 PASSED                                                                                                                                                                  [ 12%]
tests/test_1_sim_start_param_validation.py::test_sim_start_2 PASSED                                                                                                                                                                  [ 25%]
tests/test_1_sim_start_param_validation.py::test_sim_start_3 PASSED                                                                                                                                                                  [ 37%]
tests/test_2_sim_start_job_validate.py::test_sim_status_begin PASSED                                                                                                                                                                 [ 50%]
tests/test_2_sim_start_job_validate.py::test_sim_start_1 PASSED                                                                                                                                                                      [ 62%]
tests/test_2_sim_start_job_validate.py::test_sim_start_2 PASSED                                                                                                                                                                      [ 75%]
tests/test_2_sim_start_job_validate.py::test_sim_status_end PASSED                                                                                                                                                                   [ 87%]
tests/test_home.py::test_base_route PASSED                                                                                                                                                                                           [100%]

============================================================================================================ 8 passed in 7.41s =============================================================================================================

```
