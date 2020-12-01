import argparse

ds_name = ""
minSup = 1
params = ""

parser = argparse.ArgumentParser()
parser.add_argument(
    '-ds', '--dataset_name',
    type=str,
    default='',
    help='str, database name'
)
parser.add_argument(
    '-s', '--support',
    type=float,
    default=1,
    help='The support as float 10% = 0.1'
)
parser.add_argument(
    '-p', '--params',
    type=str,
    default='',
    help='Extra parameters for the gSpan mining process'
)
parser.add_argument('--graphlet', action='store_true')
parser.add_argument('--cork', action='store_true')
parser.add_argument('--random', action='store_true')
