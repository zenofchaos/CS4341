Language: Python 3.6.0

Unzip project to desired folder.
Navigate to folder in command prompt and use the command:
python astar.py [world name] [Heuristic #]

If you have issues using the command, the program will alert you of any mistakes.
You can also use the command 'python astar.py -h' to access the help manual for the code.

The worlds and heuristics provided can be seen below.
board.txt is the sample world and unsovlable.txt is an unsolvable world.
The other worlds are each worlds whose sizes match their names.

Available [world name]:
board.txt
unsolvable.txt
world5x5.txt
world15x15.txt
world20x20.txt
world30x25.txt
world99x99.txt

Available [Heuristic #]:
1
2
3
4
5
6

Additionally, another file provided is createWorld.py.
This is the code used to generate the test worlds.
If you'd like to use this code to generate worlds run the following command:
python createWorld.py [width] [length] > [file name]

This command pipes stdout (The world) to the file you specify.
