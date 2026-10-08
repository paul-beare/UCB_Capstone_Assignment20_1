# UC Berkeley ML-AI-Cert
# Assignment 20 - Capstone Project Work in Progress Advances

## Project files
- [Notebook: SampleDataLoadandReviewwNoise.ipynb](SampleDataLoadandReviewwNoise.ipynb)
- [JSON Dataset: acp_mixed_outcomes_w_noise.json](acp_mixed_outcomes_w_noise.json)
- [Dataset Generator: acp_extended_generator_w_noise.py](acp_extended_generator_w_noise.py)


### Problem presented
ML has long been used in detecting digital payment fraud for “Traditional Human Payments” (e.g. online purchases, merchant POS purchases, etc.) in which a human was part of each payment transaction.
As we transition to service providers and merchants offering and accepting payments driven by autonomous Payment Agents, new strategies, data sources and ML/AI algorithms need to be developed and implemented.

Data needs
In addition to the typical fraud detection data, there is more work to be done to find data in the “footprint” of the transaction.  Since this is an industry still in development the data sources probably are not many and/or publicly available, so the model might need to be created using synthetic or simulated data.  

Thus, we had to generate data using a data generator.  Since the data generated had clear indicators in some features of the "fraudulent" transactions we added some noise in order to not have direct correlation between some of the feaatures and the "fraud" suspect column.

## Summary of findings

In this work in progress advance, we provide a baseline of 0.99 accuracy using Linear Regression.  Although it seems high, remember that this an unbalanced dataset which produces fraud samples in 5% of the cases.  So a baseline of 0,95 is already give by the data itself.
