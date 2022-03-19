Starter code can be found in the /bots folder.

Graders can be run locally via the test_runner.py script.
Before running, open test_runner.py, and uncomment the games you want to test,
along with modifying the appropriate arguments. Running will produce replays in
the /replays folder, which can then be viewed via the visualizer.

To print out intermediate data while your program is running, use
    print(<your output here>, file = sys.stderr)
Printing normally will send text to the grader, causing an error.

Visualizations of played matches will be available online shortly after
they are played in the match results tab. To visualize locally-played matches,
run visualization_hoster.py from the contest handout locally, and go to the
Local Visualization tab. The browser visualizers will pull data off the
hoster’s server, without sending any data to CMIMC.

To use the online visualizer, click on the "Load" button on a replay to load it.
Then, you can use left/right arrow to go forwards/backwards one step, up/down to
zoom in and out, and you may click and drag using the mouse.
