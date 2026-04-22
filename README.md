Intelligent State-Space Routing Engine for Mobile Connectivity on the London Underground

This repository contains the code and supporting files for my COMP1682 Final Year Project at the University of Greenwich.

Overview
This project implements a connectivity-aware routing engine for the London Underground. It extends shortest-path routing by penalising disconnected underground segments and line interchanges.

Core Logic
- 300-minute penalty for no-signal segments
- 5-minute interchange penalty
- 2.5-minute baseline correction for zero or invalid travel-time values

Main Files
- router.py — routing engine and weighted graph search
- gui.py — Tkinter graphical user interface
- build_network.py — base topology generation
- add_signal.py — signal enrichment
- add_travel_times.py — travel-time enrichment
- COMPLETE_tube_network_dataset.csv — final offline dataset used by the routing engine

Running the Final Project
1. Make sure Python is installed.
2. Ensure the final dataset CSV is in the project folder.
3. Run `gui.py` to launch the interface.

Rebuilding the Dataset
The final demonstrator runs offline and does not require a TfL API key.

The API-based scripts are included only for rebuilding the dataset from scratch. To use them, replace `API_KEY = "YOUR_KEY_HERE"` with your own TfL API key locally.
