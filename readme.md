## Overview
CADI: [B2G-22-005](https://cms.cern.ch/iCMS/analysisadmin/cadilines?line=B2G-22-005&tp=an&id=2597&ancode=B2G-22-005)
This repository provides all nessecary information to reproduce the results of B2G-22-005: search for pair production of excited top quarks. Mainly, this involves combine datacards which can be used to produce signal & validation region distributions as well as exclusion limits and all other statistical tests. Information on other documentation is given at the bottom.

### Setup 
This repository requires [combine](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/)  to be set up, then it can be cloned as a sub-directory within. Most of the setup is based on jupyter notebooks, which can be (for example) ran using SWAN oder DESY JHUB, but of course could also simply be converted to python files.

### Datacards
Input datacards can be found in the `cards_combined` directory. They are generated from the output of the analysis framework using the [create_cards.ipynb](https://gitlab.cern.ch/cms-analysis/b2g/b2g-22-005/combine_setup/-/blob/master/create_cards.ipynb?ref_type=heads) notebook, which will construct cards for the individual eras of Run 2. Then, these can be combined using [combine_templates.ipynb](https://gitlab.cern.ch/cms-analysis/b2g/b2g-22-005/combine_setup/-/blob/master/combine_templates.ipynb?ref_type=heads), resulting in the files found in `cards_combined`.
Note that the default configuration stores signal templates normalized to 10 fb.

### Distribution plotting
Using the scripts in `niceplotter`, pre-fit figures of signal and validation region, can be created from the input cards. These will be created with full systematic uncertainties considered and allow some options to enable and disable bin width division and different signal normalization.
Note: The `niceplotter` scripts were written by C. Matthies and adapted for this analysis.

### Exclusion limits
Combine can be ran to obtain expected and observed exclusion limits. [create_limit_runner.ipynb](https://gitlab.cern.ch/cms-analysis/b2g/b2g-22-005/combine_setup/-/blob/master/create_limit_runner.ipynb?ref_type=heads) can be used to produce a bash script which can be executed to run combine. Different settings are available to select between expected and observed limits, different spin scenarios and regions, as well as lepton channels.
The resulting output files (by default found in a directory called `outputs`) can be used in [draw_limit_plot.ipynb](https://gitlab.cern.ch/cms-analysis/b2g/b2g-22-005/combine_setup/-/blob/master/draw_limit_plot.ipynb?ref_type=heads) to create exclusion limit plots. This also involves drawing of theory curves and exclusion limits from the previous analysis, for which all information is stored in [data.py](https://gitlab.cern.ch/cms-analysis/b2g/b2g-22-005/combine_setup/-/blob/master/data.py?ref_type=heads).

### Post-fit shapes
Post-fit shapes can be obtain using the [extract_post_fit_shapes.ipynb](https://gitlab.cern.ch/cms-analysis/b2g/b2g-22-005/combine_setup/-/blob/master/extract_post_fit_shapes.ipynb?ref_type=heads) notebook, which will perform a fit and produce an output file, which can then be used in the niceplotter to create post-fit plots.

### Other statistical tests
Other statistical tests can be ran using the various other notebooks, provided for GoF tests, impact plots and signal injection tests. The instructions for each of these steps are given as printouts in the respective notebooks.
