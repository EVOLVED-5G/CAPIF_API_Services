# Usage

In order to achieve independence of underlying machine we build a docker with robot binary to use this tool in a deacoplated, static and controlled way.

## Generate robot-test docker image

To generate container unit use the following

The image will be built and pushed to artifact.

The docker image is stored at dockerhub.hi.inet/5ghacking/robot-test-image:latest

# To build image

Under "robot" directory, execute this:

docker build . -t dockerhub.hi.inet/5ghacking/robot-test-image:latest

## To run test with container
```
docker run -t --rm 
       -v <ROBOT_COMMON_DIRECTORY>:/opt/robot-tests/common 
       -v <ROBOT_TESTS_DIRECTORY>:/opt/robot-tests/tests 
       dockerhub.hi.inet/5ghacking/robot-test-image:latest
       <RELATIVE_PATH_TO_TEST>
```

If RELATIVE_PATH_TO_TEST is not set, it will execute alll tests placed in <ROBOT_TEST_DIRECTORY>, in other case, robot.test should be call relate to <ROBOT_TEST_DIRECTORY>

# To run bash in container
```
docker run -ti --entrypoint=/bin/bash --rm 
       -v <ROBOT_COMMON_DIRECTORY>:/opt/robot-tests/common 
       -v <ROBOT_TESTS_DIRECTORY>:/opt/robot-tests/tests 
       dockerhub.hi.inet/5ghacking/robot-test-image:latest

```
