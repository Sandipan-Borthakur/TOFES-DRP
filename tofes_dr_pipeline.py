'''
Currently auto_id is finding the peaks in the wavelength calibration spectrum and rejecting the lines.
Instead include a parameter which if True can directly fit a 2D wavelength solution on the linelist values
after cross correlation. This way we can get a wavelength solution each time.
'''

import numpy as np
import os
import sys
sys.path.append("/home/sborthakur/Documents/PhD_Tartu1/pyreduce_learning/PyReduce-master")
from pyreduce.configuration import get_configuration_for_instrument
from pyreduce.instruments.common import create_custom_instrument
from pyreduce.reduce import Reducer
from pyreduce.util import start_logging
from pyreduce.instruments.instrument_info import load_instrument


instrument_name = "tofes"

instrument = load_instrument(instrument_name)
config = get_configuration_for_instrument(instrument_name, plot=0)

# Define other parameter for PyReduce
target = "Sun"

# We define the path to the output directory
output_dir = f"TOFES-reduced-{target}"

# Define the path to support files if possible
# otherwise set them to None
flat_file = os.path.join(output_dir,"tofes.flat.fits")


# Vega
if target=="Vega":
    night = "2024-06-21"
    files = {
        "bias": ["2024-06-21/Bias_0s_20240621_221716-%d.fit"%i for i in np.arange(1,11)],
        "flat": ["2024-06-21/Flat_5s_20240621_192503-%d.fit"%i for i in np.arange(1,25)],
        "orders": [flat_file],
        "scatter":[flat_file],
        "science": ["2024-06-21/Vega_Object_25s_20240621_224908-%d.fit"%i for i in np.arange(1,2)],
        "wavecal_master":[
            "2024-06-21/Vega_Calibration_30s_20240621_225633-%d.fit"%i for i in np.arange(1,6)]
        }

# Sun
elif target=="Sun":
    night = "2024-06-21"
    files = {"bias": ["2024-06-21/Bias_0s_20240621_182026-%d.fit"%i for i in np.arange(1,11)],
             "flat": ["2024-06-21/Flat_5s_20240621_192503-%d.fit"%i for i in np.arange(1,25)],
             "orders": [flat_file],
             "scatter":["2024-06-21/Flat_5s_20240621_192503-%d.fit"%i for i in np.arange(1,25)],
             "science": ["2024-06-21/Sun_Object_20s_20240621_183427-%d.fit"%i for i in np.arange(1,2)],
             "wavecal_master":[ "2024-06-21/Sun_Calibration_35s_20240621_184136-%d.fit"%i for i in np.arange(1,11)]
        }

# Arcturus
elif target=="Arcturus":
    night = "2024-06-21"
    files = {"bias": ["2024-06-21/Bias_0s_20240621_232157-%d.fit"%i for i in np.arange(1,11)],
             "flat": ["2024-06-21/Flat_5s_20240621_232635-%d.fit"%i for i in np.arange(1,10)],
             "orders": [flat_file],
             "scatter":["2024-06-21/Flat_5s_20240621_232635-%d.fit"%i for i in np.arange(1,10)],
             "science": ["2024-06-21/Arcturus_Object_5s_20240621_230805-%d.fit"%i for i in np.arange(1,2)],
             "wavecal_master":[ "2024-06-21/Arcturus_Calibration_30s_20240621_231258-%d.fit"%i for i in np.arange(1,11)]
        }

# High S/N wavelength calibration
elif target=="wavecal_high_snr":
    night = "2025-01-07"
    files = {"bias": [night+"/Bias_0s_20250107_105310-%d.fit"%i for i in np.arange(1,11)],
             "flat": [night+"/Flat_30s_20250107_094902-%d.fit"%i for i in np.arange(1,25)],
             "orders": [flat_file],
             "scatter":[night+"/Flat_30s_20250107_094902-%d.fit"%i for i in np.arange(1,25)],
             "wavecal_master":[night+"/ThAr+flatid_Calibration_30s_20250107_084702-%d.fit"%i for i in np.arange(1,11)]
        }
else:
    ValueError ("No target found")

# (optional) We need to define the log file
log_file = os.path.join(output_dir,"log_file.txt")
start_logging(log_file)

mode = ""
steps = (
   "bias",
   "flat",
   "orders",
   # "scatter",
   "norm_flat",
   "wavecal_master",
    "wavecal",
   "science",
    "continuum",
    "finalize",
)

# Call the PyReduce algorithm
reducer = Reducer(
    files,
    output_dir,
    target,
    instrument,
    mode,
    night,
    config,
)
data = reducer.run_steps(steps=steps)