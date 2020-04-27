EVERGLADES
----------
EVERGLADES is a synchronous, turn-based 1v1 strategy game originally developed by Lockheed Martin for reinforcement learning in real life combat situations. The primary objective of the game is to capture the opponent’s base, and the secondary objective is capturing nodes and eliminating enemy opponents.

The primary goals as the Robot Behavior Analytics team:

- Characterize EVERGLADES match output to determine behaviors that most often lead to wins
- Create AI scripts of targeted behaviors to test hypothesis from characterization activity
- Develop a real-time analytics engine that runs simultaneously with EVERGLADES match playback

TYPICAL INSTALLATION
--------------------
Clone this repository with ``git``
::
  git clone https://github.com/shaunhyp57/everglades.git
  cd everglades

DEPENDENCIES
------------
EVERGLADES runs in a Python3 environment. Ensure the python packages ``gym`` and ``numpy`` are installed. This can be done with:
::
  pip install numpy
  pip install gym

If your computing environment requires it, make sure to include the ``--cert`` and ``--proxy`` flags with the ``pip`` commands.

INSTALLATION
------------
From the root ``everglades`` directory, install the EVERGLADES environment with:
::
  pip install -e gym-everglades/

Next, install the EVERGLADES server with:
::
  pip install -e everglades-server/

Finally, edit the ``test_battle_rtengine.py`` script to reflect the current working environment. Update the following lines with their path in the file system:

-  agent 0 file
-  agent 1 file
-  config directory
-  output directory

FILE AND DIRECTORY DESCRIPTION
------------------------------

``./agents/``

This is a common directory where any created agents for the EVERGLADES game can be stored. Some example files are included with the package.

``./analysis_everglades/``

This directory contains analysis and machine learning modeling for the EVERGLADES game

``./docs/``

This directory contains the Design Documents and presentation for the Robot Behavior Analysis and Real Time Engine creation

``./database/``

This directory contains the database schema and information

``./config/``

This directory contains setup files which are used for game logic. Currently only the ``DemoMap.json`` and ``UnitDefinitions.json`` files are used for gameplay. They can be swapped for files defining a different map or units, but note that any swaps likely will cause inflexible server logic to break.

``./engine_analysis/``

This directory contains the files used for performance metrics for the Real Time Engine

``./everglades-server/``

This directory contains the main logic for the EVERGLADES game.

``./game_prediction_info/``

This directory contains prediction summaries from running the Real Time Engine

``./gym-everglades/``

This directory is the OpenAI Gym for project EVERGLADES. It follows the Gym API standards.

``./rte_model_training/``

This directory contains the models trained for the Real Time Engine

``./RT_Engine_Class.py``

This is a class imported in the ``test_battle_rtengine.py`` script

``./test_battle_rtengine.py``

This is the script to execute for running two agents against each other for the Real Time Engine.

``./test_battles/``

This directory contains other versions of the ``test_battle_rtengine.py`` script

``./README.rst``

This file, explaining important directory structure and installation requirements.

``./.gitignore``

This file tells git to ignore compiled files and telemetry output.

Please read the `wiki page for the EVERGLADES Analytics and Engine`_ to learn more about the game and the analytics.

AUTHORS
-------
- `Brian Catrett`_
- `Chandler Epes`_
- `Shauna Hyppolite`_
- `Sebastian Krupa`_
- `Read O'Quinn`_

.. _`Brian Catrett` : https://github.com/BCatrett
.. _`Chandler Epes` : https://github.com/cfepes
.. _`Shauna Hyppolite` : https://github.com/shaunhyp57
.. _`Sebastian Krupa` : https://github.com/sebciomax
.. _`Read O'Quinn` : https://github.com/ReadOQ
.. _`wiki page for the EVERGLADES Analytics and Engine` : https://github.com/shaunhyp57/everglades/wiki
