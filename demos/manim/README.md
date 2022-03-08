# Manim Proof of Concept 

Here you can create a docker container to aide the development of Manim animations. 

## Building the Docker Container 

To build the container run:

```bash
docker build . -t manim-poc
```

## Building Specific Animations 

It will be easiest to specify which animation you want to run by first accessing the command line of the container and then running a manim function to specify animations.

```bash
docker run -it --rm -v $PWD:/code manim-1 /bin/bash
```
Then:
```bash
manim -pql manim_examples.py Example_2
```

In this example ^ Example_2 is the name of the class whose `construct()` function creates the animation. 

## Running Python Files that Call Construct Functions

If your python file calls a specific manim contruct function then you can just run the python file and generate an animation with:

```bash
docker run --rm -v $PWD:/code -w /code manim-1 python manim_examples.py
```

## Viewing Amimated MP4 Videos 

When you use the above functions to run your docker containers, they mount the container's file system to the local machine's working directory so that videos generated in the container will also be created on the local machine. 

All those videos will be added to a `./media` folder. The full video can be found in `./media/videos/480p15/` or whichever video quality you specified.
