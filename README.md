
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

Run `pytest -v tests` from root directory