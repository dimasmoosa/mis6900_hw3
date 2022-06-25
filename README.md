# mis6900_hw3

Preface
=======

The layout of this project was from the cookiecutter template set up by running the following command (after doing a pip install of cookiecutter of course):

```bash
cookiecutter gh:misken/cookiecutter-datascience-simple
```

It has been modified a bit from the original structure to remove unecessary items.

Folder structure
-----------------

Here's the folder structure that gets created by `cookiecutter-datascience-simple`:

	├── mis6900_hw3	<- Your notebooks and scripts will live in the main project folder
		│   .gitignore					<- Common file types for git to ignore
		│   README.md					<- The top-level README 
		│   cafeteria.py				<- The file containing all of the code 
		│
		└───output						
				csv files				<- Wait time output files + summary stats output files. d = duration, k = number of kiosks, c = number of chefs, u = number of utensil dispensers, ts = timestamp


Documentation & How to Run
---------------------------
This is a pretty simple discrete event simulation model based off of my cafeteria at work. The code is inside `cafeteria.py`.

The model processes consist of ordering food at the kiosk, the chef making the ordered food, and then getting utensils if the food requires it and/or getting a drink if it was ordered.
Accordingly, the resources consist of the kiosk, the chef, the utensil dispenser, and the pop machine.

The distributions/randomness of the wait times of each process is currently hard-coded to how I remember the times to be based off of my experience. For example, I remember chefs taking anywhere from 3 to 7 minutes to make the food and that is what the `make_food` function is currently set to, a random number between 180 and 420 (seconds). 

It is recommended to run the `cafeteria.py` file on its own (inside of PyCharm for example). Changes to resource numbers, duration of the simulation, and whether to print out event timestamps to the console can be made inside `main`.

Each time the file is ran, there will be an output csv file with the full wait times for each event under the `output` folder (there are examples in there already) as well as a summary csv file. In addition, the summary statistics will also be printed out to the console along with the total average wait time.
All output files will have the configuration settings in the title (e.g. 'k' for number of kiosk resources) and a timestamp of when the file was ran so no files are overwritten.


Example scenarios
-----------------

First example is using 2 kiosks, 2 chefs, 4 utensil dispensers, and 2 pop machines. We are running this first simulation for 3 hours (about the time lunch was available). This scenario yields an average wait time of 19 minutes and 6 seconds. This seems a bit higher than what I remember the average wait being but then again there were days where the food took well over 30 minutes. 

For the second example, I am increasing the number of kiosks to 3, the number of chefs to 5, and leaving the number of utensil dispensers and pop machines the same at 4 and 2, respectively. I am also changing the runtime of the simulation to 2 hours intead, down from 3. With these settings, we see the average total wait time decrease to 7 minutes and 36 seconds. This made a very noticeable difference, taking the average wait time down by 12 minutes, more than half of what it was.

For the third and final scenario, I am leaving everything as is from the second scenario but changing the number of chefs back 2, what it was in the first example so that I can gauge how much of a difference those 3 chefs made. Yikes, the total average wait time shot up to 20 minutes. This makes sense since the range of wait time for a chef making food event is longer than ordering food at a kiosk event (3m to 7m, compared to 1m to 3m).


Future Enhancements
--------------------
Obviously this is a pretty bare bones project. Many enhancements can be made including making the random wait times distributed in a different probability distribution rather than uniform, creating a CLI, and adding more events and properties as well as stats.