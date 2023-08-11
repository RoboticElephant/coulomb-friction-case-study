# Interview Case Study
This is a case study for <company>. The purpose is to output Coulomb friction

## Coulomb Friction
This is considered a dry friction. This simply means that there isn't any lubricant between the two surfaces.

## Assumptions
- Block is sliding on a horizontal surface
- No other forces are being imparted into the system during movement beyond what is given.
- Units are only in SI

## API Calls
### Coulomb Friction
#### GET all friction values
```
<url>/friction
```
This will return an array of all the friction values in the database
***Return***:
```json
[
  {
    "coef_friction": 0.3,
    "gravity": 9.81,
    "id": 1,
    "init_velocity": 15.0
  }
]
```

#### GET Specific Friction Data
```
<url>/friction/<int: friction_id>
```

This will get the specific values for a given friction input in the database
***Return***:
```json
{
  "coef_friction": 0.0,
  "gravity": 0.0,
  "id": 1,
  "init_velocity": 0.0,
  "idx": [],
  "distance": [],
  "velocities": []
}
```

#### POST data to perform Coulomb Friction on
For `<url>/friction` pass in a json:
```json
{
  "init_velocity": 10.0,
  "coef_friciton": 0.3,
  "gravity": 9.81
}
```

If successful, it will return status of 200 and a json with the above information and the `id` as well.

## Build and Deploy
This API was implemented in a docker file. This allows for portability and scalability of the service with very little code change required.

### Build
The docker command to build the service is:

```docker
docker build -t case-study-api .
```

This will build the image with the `tag`: `case-study-api`.

### Deploy
In order to deploy the docker image to a container, it is best to run it detached. Therefore, need to run:

```docker
docker run -dp 5005:5000 case-study-api
```

The above line will connect port `5000` to port `5005` of the image `case-study-api`.

## Architecture
```
├── app.py
├── engineering
│   ├── __init__.py
│   └── coulomb_friction.py
├── models
│   ├── __init__.py
│   └── friction.py
├── resources
│   ├── friction.py
│   ├── home.py
│   └── user.py
├── requirements.txt
├── Dockerfile
├── logging_config.py
├── schemas.py
├── db.py
├── .gitignore
├── testing
│   ├── conftest.py
│   ├── __init__.py
│   ├── engineering
│   │   ├── __init__.py
│   │   └── test_friction.py
│   └── resources
│       ├── __init__.py
│       ├── test_friction.py
│       └── test_home_page.py
└── venv
```

## Adding to the Service
### Engineering Formula
If you wish to add additional engineering formulas to the service, they can be added in the `engineering` package.

### Resources
Once any necessary formulas have been added, a new file in the `resources` folder will need to be added. The `resources` folder contains all the API calls and routes.

Once you have completed adding the necessary file and routes for the API, add the blueprint to `app.py`. This will allow the app to recognize and properly route any appropriate calls.

### Models
If your code has any information that needs to be added to the database, add the necessary information in a new file in `models` package. 
You will also need to add to the `__init__.py` file the necessary imports for your given model (i.e. `<package-name>Model`)

### Schemas
Add any necessary schema for the routes into the `schemas.py` file. 

### Testing
This API uses `pytest` to perform unit testing of all calls. Add any new tests to the appropriate folder under `testing` package.

To run `pytest` to perform the unit tests, run:

```
pytest --cov
```
This will return the code coverage for all the files.

#### Adding Tests
In order for `pytest` to be able to use the correct files and functions, make sure to name all files and functions as:

##### Files
```
test_<file-to-be-tested>.py
```

##### Functions
```
test_<function-name>_<expected-output>
```







