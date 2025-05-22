# Air-Quality-Data-and-Scripts

## Where to look

The foler structure is as follows:
├───monthly-data  \
└───scripts  \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├───data-visualization  \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└───predictive-models  \

monthly-data directory contains the data of 1 month prior to the date specified in the filename. For example, in the influxdata_2025-04-05T13_21_36Z csv contains the data collected in 1 month from 2025-03-05 to 2025-04-05.

scripts directory contains some visualization scripts using matplotlib in the data-visualization directory, and some machine learning techniques to predict the pollution trends using models like arima in the predictive-models directory.
