"""
Reads Excel files (using your existing ExpInfoForm classes/functions)

Inputs: Excel path
Outputs: dictionary or DataFrames like:
{
    "form": {...},             # general exp info
    "sd_preparation": {...},   # sd7 info
    "sample_info": DataFrame,  # A01–H12 well data
    "readouts": DataFrame,     # same index, multiple analytes/wavelengths
}
"""

