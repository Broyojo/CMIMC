# run this file

# make sure that we are in the correct directory
from graders import MotPE, NFGC, Help, TNTRun
import os

os.chdir(os.path.dirname(__file__))


# MotPE and Help (the optimization problems) take in a gen argument,
# corresponding to (generator, parameter) for MotPE (but should be left as None
# for Help). The seed argument can also be set to generate the same state
# over multiple tests.

# record_logs=True can be passed to record all interactions your bot has
# with the grader, to help with debugging

# Uncomment any of the 4 lines below to run a test of that game,
# using the code provided in the source argument (make sure you save your
# files in the "bots" folder, or supply the correct file path).

# For games with multiple players, you can supply multiple source files
# corresponding to different bots (you may also use the same source file
# multiple times, to create multiple instances of the same bot).

# MotPE().test(gen=("random", 10), source="bots/motpe_starter.py", name="starter_random", save_replay=True, record_logs=False)
# MotPE().test(gen=("circles", 4), source="bots/motpe_starter.py", name="starter_circles", save_replay=True, record_logs=False)
# MotPE().test(gen=("path", 16), source="bots/motpe_starter.py", name="starter_path", save_replay=True, record_logs=False)

Help().test(
    source="../ikea.py",
    name="starter_test",
    save_replay=True,
    seed=1337,
    gen=None,
    record_logs=False,
)

# TNTRun().test(sources=["../tnt-run-cory.py"]*12,
#   name="starter_test", save_replay=True, record_logs=False)

# NFGC().test(sources=["bots/nfgc_starter.py"]*30, name="starter_test", save_replay=True, record_logs=False)
