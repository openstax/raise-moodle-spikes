# Demo Enclave Container

## Code example

This demo envlave container takes `grades.csv` and `oneroster_demographics.csv` and gives us the average 
`grade_percentage` based on sex. 

Using the Pandas library we import the files into DataFrames.
We must get the environment variables passed into the container using `os.getenv`.
Using the envioronment variables we can get the files and figure out where to output the file.


```py
import pandas as pd
import os

INPUT_PATH = os.getenv('DATA_INPUT_DIR')
RESULTS_OUTPUT_PATH = os.getenv('RESULT_OUTPUT_DIR')

grades = pd.read_csv(f'{INPUT_PATH}/grades.csv')
demographic = pd.read_csv(f'{INPUT_PATH}/oneroster_demographics.csv')
```

Now we join the data sets on the `user_uuid` so we can map the sex of the student to the exam score. 

```py
merged_data = pd.merge(grades, demographic, on='user_uuid', how='outer')

```

We can now run the group by `sex` and `grade_percentage` to find the average grade based on sex. 

```py
average_grade_by_sex = merged_data[["sex", "grade_percentage"]].groupby('sex').mean()
```

Now we can write to the output directory the  `RESULTS_OUTPUT_PATH` environment variable defines for us.

```py
average_grade_by_sex.to_csv(f'{RESULTS_OUTPUT_PATH}/average_grades_by_sex.csv')

```

## Building and running the container 

First we have to build the container. The -t flag allows us to name the container so we can 
call it in the following run command. 

The following command is ran in the directory with the Dockerfile in it. 
```bash 

docker image build -t enclave_container .
```

Now we can run the container, pass the environment variables and mount volumes to the container. 

```bash
docker run --rm -e DATA_INPUT_DIR=/input -e RESULT_OUTPUT_DIR=/output -v $PWD/enclave-input:/input -v $PWD/enclave-output:/output enclave_container
```