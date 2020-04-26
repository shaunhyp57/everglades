EVERGLADES
----------
EVERGLADES is a synchronous, turn-based 1v1 strategy game originally developed by Lockheed Martin for reinforcement learning in real life combat situations. The primary objective of the game is to capture the opponent’s base, and the secondary objective is capturing nodes and eliminating enemy opponents.

The primary goals as the Robot Behavior Analytics team:

- Characterize Everglades match output to determine behaviors that most often lead to wins
- Create AI scripts of targeted behaviors to test hypothesis from characterization activity
- Develop a real-time analytics engine that runs simultaneously with Everglades match playback

TYPICAL INSTALLATION
--------------------
Clone this repository with ``git``
::
  git clone https://github.com/shaunhyp57/everglades.git
  cd everglades

Dependencies
____________
EVERGLADES runs in a Python3 environment. Ensure the python packages ``gym`` and ``numpy`` are installed. This can be done with:
::
  pip install numpy
  pip install gym

If your computing environment requires it, make sure to include the --cert and --proxy flags with the pip commands.

Installation
____________
From the root Everglades directory, install the EVERGLADES environment with:
::
  pip install -e gym-everglades/

Next, install the Everglades server with:
::
  pip install -e everglades-server/

Finally, edit the ``test_battle.py`` script to reflect the current working environment. Update the following lines with their path in the file system:
-  agent 0 file
-  agent 1 file
-  config directory
-  output directory

File and Directory Descriptions
_______________________________

./agents/
+++++++++

This is a common directory where any created agents for the Everglades game can be stored. Some example files are included with the package.

./config/
+++++++++

This directory contains setup files which are used for game logic. Currently only the DemoMap.json and UnitDefinitions.json files are used for gameplay. They can be swapped for files defining a different map or units, but note that any swaps likely will cause inflexible server logic to break.

./everglades-server/
++++++++++++++++++++

This directory contains the main logic for the Everglades game.

./game_telemetry/
+++++++++++++++++

This is the default output directory for any match telemetry output. It is only populated locally and not stored in the git repository.

./gym-everglades/
+++++++++++++++++

This directory is the OpenAI Gym for project Everglades. It follows the Gym API standards.

./test_battle.py
++++++++++++++++

This is the script to execute for running two agents against each other.

./README.md
+++++++++++

This file, explaining important directory structure and installation requirements.

./.gitignore
++++++++++++

This file tells git to ignore compiled files and telemetry output.



