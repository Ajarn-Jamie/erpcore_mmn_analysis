# ERPCORE Scripts
This repository contains scripts for preprocessing and analyzing the MMN dataset from ERP CORE by Emily S. Kappenman and  Steven J. Luck (https://doi.org/10.18115/D5JW4R).

To run these scripts, first download the ERP CORE MMN dataset, then save the "*.set*" and "*.fdt*" files in a folder named "ERPCORE_MMN_SET_FILES" located in a level above the directory containing the scripts.

The file "analysis.py" preprocesses and analyzes data in the "ERPCORE_MMN_SET_FILES" folder and generates a file "erpcore_mean_amp.csv".

The file "bayes_factors.r" calculates pairwise t-test Bayes factors between mean amplitudes measured over 125-225 ms from consecutive 80 dB standards (sS), 70 dB deviants after 80 dB standards (sD), and 80 dB standards after 70 dB deviants (dS).

These sripts are shared under the terms of a Creative Commons license (CC BY-SA 4.0).
