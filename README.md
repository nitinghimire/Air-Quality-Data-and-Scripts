# Air-Quality-Data-and-Scripts

## Overview

This repository contains scripts and datasets related to air quality monitoring and prediction. It includes tools for visualizing PM data, preprocessing time series data, and applying machine learning models to forecast pollution levels.

---

## Folder Structure

```
├── monthly-data/
├── scripts/
│   ├── data-visualization/
│   ├── datapreprocessing/
│   └── predictive-models/
├── tests/
└── README.md
```

### `monthly-data/`

Contains monthly CSV data files. Each file is named using the end date of the data it contains. For example, `influxdata_2025-04-05T13_21_36Z.csv` includes data collected from **2025-03-05 to 2025-04-05**.

---

## Usage

### Visualization Scripts

All scripts for generating visual plots (like PM2.5 and PM10) using `matplotlib` can be found in:

```
scripts/data-visualization/
```

Generated figures are saved in the `figures/` subdirectory inside this folder.

### Statistical Tests

The `tests/` directory contains scripts and figures for evaluating stationarity using the Augmented Dickey-Fuller (ADF) test.

### Data Preprocessing

Data loading and cleaning scripts are located in:

```
scripts/datapreprocessing/
```

Use these utilities to prepare time series for modeling.

### Predictive Modeling

Machine learning scripts such as the ARIMA model are located in:

```
scripts/predictive-models/
```

These scripts apply forecasting models to historical air pollution data.

---

## Notes

- Ensure required Python packages (e.g., `pandas`, `matplotlib`, `statsmodels`) are installed.
- This project is part of an ongoing effort to predict and visualize trends in air pollution data for public health awareness.
