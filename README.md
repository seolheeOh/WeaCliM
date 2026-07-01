# WeaCliM: Self-Supervised Learning of Climate Signals from Weather Fields

## Overview

This repository contains the source code, datasets, and analysis scripts used in the manuscript:

"Self-Supervised Learning of Climate Signals from Weather Fields for Global Climate Forecasts"

WeaCliM is a self-supervised climate prediction framework that first pretrains a general encoder using the Bootstrap Your Own Latent (BYOL) algorithm and subsequently trains lightweight downstream regressors for seasonal precipitation prediction.

This capsule includes the code and files required to reproduce the results presented in <Main Fig. 2> of the manuscript. The complete repository additionally contains the source code for model training, Grad-CAM analysis, feature analysis, and figure generation.

---

# Repository Structure

```
- README
- Dataset/
  - NMME
  - Dyn
- Features/
- GradCam/
- LICENSE
- Model/
  - byol/
- Outputs/
- Scripts/
- environment.yml
- figures/
- utils_src.py
```

### Dataset/

The datasets used in this study are publicly available. ERA5 reanalysis data are available from the ECMWF repository (https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysisv5). Seasonal dynamical prediction outputs from the North American Multi-Model Ensemble (NMME) are available through the International Research Institute for Climate and Society (IRI) Data Library (https://iridl.ldeo.columbia.edu). Additional seasonal forecasts used for comparisons of extreme precipitation index anomalies are available from the Copernicus Climate Data Store (https://cds.climate.copernicus.eu/datasets/seasonal-original-single-levels). Global Precipitation Climatology Project (GPCP) precipitation data are available from the Copernicus Climate Data Store (https://cds.climate.copernicus.eu/datasets/satellite-precipitation). The processed datasets required to reproduce the results presented in this study are provided in the accompanying Code Ocean capsule.

---

### Model/

Contains the neural network architectures used in this study.

- WeaCliM downstream regressor.
- Reference CNN models using daily and monthly inputs.
- `byol/`
  - BYOL-based self-supervised encoder pretraining.

---

### Scripts/

Contains executable scripts for model training and evaluation.

These scripts perform

- BYOL encoder pretraining,
- downstream regressor training and evaluation,
- reference CNN training and evaluation.

---

### GradCam/

Contains scripts for generating Grad-CAM outputs from the WeaCliM and reference CNN models. These outputs were used to produce Extended Data Figs. 3 and 4.

---

### Features/

Contains scripts for extracting feature representations from the convolutional layers of the trained models. The extracted features were used for the EOF analysis presented in Extended Data Fig. 5.

---

### Outputs/

Stores outputs generated during training and evaluation, including

- trained model weights,
- prediction results,
- training logs (CSV).

Subdirectories include

- `BYOL`
- `BYOL_GradCam`
- `BYOL_feature`
- `ref_CNN_daily`
- `ref_CNN_daily_GradCam`
- `ref_CNN_daily_feature`
- `ref_CNN_monthly`

---

### figures/

Contains scripts used to generate the figures in the manuscript.

For reproducibility, the scripts and required files for reproducing Main Fig. 2 are organized in

```
figures/figure2/
```

Execute the scripts sequentially according to their filenames, and finally run

```
9.figure2.py
```

to reproduce Main Fig. 2.

---

### environment.yml

Conda environment file describing the software environment used in this study.

---

### utils_src.py

Utility functions for model evaluation and statistical calculations.

---

# Requirements

The software environment used in this study is provided in

```
environment.yml
```

The original experiments were performed using

- Python 3.8
- PyTorch 2.0.1
- CPU environment

---

# Quick Start

## 1. Pretrain the WeaCliM encoder

```bash
Scripts/run_pretrain.csh
```

---

## 2. Train downstream regressors

```bash
Scripts/run_regressor.csh
```

---

## 3. Train the reference CNN models (optional)

Daily-input CNN

```bash
Scripts/run_CNN_daily.csh
```

Monthly-input CNN

```bash
Scripts/run_CNN_monthly.csh
```

---

# Demo

## Reproducing Main Fig. 2

Run the scripts in

```
figures/figure2/
```

sequentially according to their filenames.

Finally execute

```
python 9.figure2.py
```

Expected output

- Main Fig. 2 of the manuscript

Expected runtime

- Approximately 5 minutes on a standard desktop computer.

---

# Outputs

The generated outputs include

- trained model weights,
- prediction results,
- training loss (CSV),
- intermediate analysis results.

---

# Acknowledgements

The BYOL implementation used in this study was adapted from the open-source <PyTorch-BYOL> implementation by Sthalles:

https://github.com/sthalles/PyTorch-BYOL

The original implementation was extensively modified for the WeaCliM framework, including

- adaptation to global weather-field inputs,
- implementation of the WeaCliM network architecture,
- customized positive-pair construction,
- downstream climate prediction,
- training and evaluation pipeline.

---

# License

This project is distributed under the <MIT License>.

See the `LICENSE` file for details.
