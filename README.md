# Target Asset Closing Price Prediction Model with Forum Data(CS760)
## Description
This research project combines forum data to predict the closing price of the target asset. 

## Group Members 
Denis Xu (hxu880), Qinglong Li (qli914), Daorui Wang (dwan266), Xiaoyu Zhang (xzha710), Zhiyang Guo(zguo573), Qiyue Ma(qma052)
Team members are divided into two groups to complete tasks： **1 Data Processing** and **2 Model Architecture**.

## Model Architecture parts:
### Files
The model Architecture part contains the following files: ANN1.ipynb, Gold_CN.csv, Gold_UK.csv, Gold_UK_clean.csv, HotCopper_Gold.csv, MSE_Gold.csv, Reddit_Gold.csv and ZGCF_Gold.csv.

### Code
The code of ANN1.ipynb is designed to predict gold prices using a multi-layer miner regression model (MLPRegressor) and explain the contribution of the model predictions through SHAP (Shapley Additive exPlanations). The data includes sentiment analysis results of reviews from multiple sources and gold transaction data.

### Environment dependence
Before running this project, make sure you have the following libraries installed:
pandas //
numpy //
scikit-learn //
shap //
matplotlib //

### Data preprocessing
The sample code includes preprocessing steps for gold price data and review sentiment data.
**1. Calculate technical indicators:** We generate new features by calculating the moving average (MA) and standard deviation (SD) for different days, which can help the model better capture trends and fluctuations in the data.
**2. Clean data：** We read the CSV file, processed the date format, converted the volume units to standard units, and removed missing values. Next, we removed some unnecessary columns from the dataset and limited the dataset to the time range of interest.
**3. Preprocess stock data：** Call the clean function to process the stock data and read the processed CSV file.
**4. Calculate the weighted mean, variance, skewness, and kurtosis：** To better understand the impact of review data on prices, we calculate weighted mean, variance, skewness, and kurtosis. These weighted statistics use the review's relevance score as a weight to reflect the review's importance.
**5. Process forum data：** We process the review data, calculate the weighted average sentiment score, number of reviews, and popularity, and aggregate these features by date.
**6. Generate review factors：** By processing the review data of each country, review factors for different countries are generated and merged.

### Model training and prediction
**1. Train the model and predict:** Use the MLPRegressor model to train and predict gold prices.
**2. Calculation error:** Calculate the root mean square error (RMSE), mean absolute percentage error (MAPE), and mean bias error (MBE) of the forecast results.
**3. Plot the error:** Plot a scatterplot of the prediction errors to observe the error distribution visually.

### Model weight interpretation
**4. Interpret the model using SHAP:** Use SHAP to interpret model predictions, calculating and plotting SHAP values ​​to understand the contribution of each feature to the predictions.





















