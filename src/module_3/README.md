# Push Notifications Module #3
This PR delivers a predictive model for potential users interested in a product. Given a user and a product, it predicts whether they would buy that product if they were purchasing at that moment. Conditions: users must have purchased at least 5 products. A linear model is used.

## Dataset Preparation
From the `feature_frame` dataset, the data was loaded and the following modifications were applied:

### Filter for users purchasing more than 5 products
A filter was applied for clients who purchased 5 or more products in the same `order_id`, allowing the model to work only with users who meet the minimum product purchase requirement.

* After this filtering, the dataset contains 2,163,953 rows, with 1.4% belonging to the target class.

### Dataset Split
Two types of splits were tested:

1. Random split: 10% of the data for testing, ~20% for validation, and ~80% for training.  
    This approach introduces the problem of data leakage, as the model may learn trends from future data, directly affecting production performance. Therefore, this method was not implemented.

2. Temporal split, defined as follows:
 * Training 70%: 2020-10-05 to 2021-02-04
 * Testing 20%: 2021-02-04 to 2021-02-22
 * Validation 10%: 2021-02-22 to 2021-03-03  

    As observed in the sales behavior chart, market behavior changes over time, directly affecting the model’s predictions.  
    ![plots](https://github.com/MaickMos/zrive-ds/blob/686a77aed98b68f3ab4ad15dad5e737b30cef5ff/src/module_3/images/Image_1.png)

### Variable Removal
Variables that do not contribute to the model or unnecessarily increase complexity were removed:
* `Variant_Id`: Product ID
* `user_id`: User ID
* `created_at`: Order creation date
* `order_id`: Order number
* `product_type`: Product category
* `order_date`: Date and time of purchase
* `vendor`: Supplier name

### Normalization
Data standardization was performed using `StandardScaler()` from sklearn, based on mean and standard deviation.

## Evaluation Metrics
### Recall
Since the dataset is imbalanced, the model will always show high accuracy. Therefore, recall is used to measure the proportion of true positives.

### Precision-Recall Curve
For better understanding and visual comparison, a precision-recall curve was implemented.

### ROC Curve
The ROC curve measures recall (True Positive Rate) against False Positive Rate. A better performance is indicated when the curve is closer to the top-left corner (1.0, 0.0), allowing easy comparison between models.

## Models
### Baseline
A basic model without machine learning algorithms was first implemented. Using existing dataset metrics, predictions were made based on the `global_popularity` variable with a binary threshold of 0.5.  

* This basic prediction yields a recall of 0.0%, but the precision-recall curve shows acceptable behavior.  
* ROC curve value is 0.79, providing a solid baseline for comparison with other models.

### Logistic Regression
This model was implemented with default parameters, no regularization, no optimization algorithm, 500 iterations, and class imbalance adjustment.

#### Train
Predictions on the training set resulted in a recall of 63%. The precision-recall curve is above the baseline, showing better behavior. The ROC curve shows 0.83, confirming model learning.

#### Test
On the test set, the model fails to generalize, showing a recall of 6%. The precision-recall curve is below the baseline, and ROC is 0.6, indicating poor performance. This model is inefficient.

### Logistic Regression Ridge
The model was retrained with Ridge regularization (0.1). Results were similar to the original model on both train and test sets. The behavior was plotted against the baseline:

![plots](https://github.com/MaickMos/zrive-ds/blob/686a77aed98b68f3ab4ad15dad5e737b30cef5ff/src/module_3/images/Image_2.png)

Further analysis was performed with different regularization values using `plot_metrics()` from 1000 to 1e-8 in powers of 100.

**Training:**  
Behavior is similar to the base model; C=0.000001 shows improved performance in certain areas.  
![plots](https://github.com/MaickMos/zrive-ds/blob/686a77aed98b68f3ab4ad15dad5e737b30cef5ff/src/module_3/images/Image_3.png)

**Test:**  
Performance remains below the baseline; C=0.0000001 shows slightly better performance.  
![plots](https://github.com/MaickMos/zrive-ds/blob/686a77aed98b68f3ab4ad15dad5e737b30cef5ff/src/module_3/images/Image_4.png)

### Logistic Regression Lasso
Tests with Lasso regularization were performed, generally surpassing the baseline. The best performing model is Lasso C=0.0001 with ROC AUC 0.83.  
![plots](https://github.com/MaickMos/zrive-ds/blob/686a77aed98b68f3ab4ad15dad5e737b30cef5ff/src/module_3/images/Image_5.png)

## Variable Importance
Using the best model (Lasso), the main contributing variables were:
* `ordered_before`
* `global_popularity`
* `abandoned_before`

Other variables have zero contribution and can be omitted.

## Product Type
Training was performed with the three most important variables plus `product_type` using categorical encoding.  
A Logistic Regression model with Lasso and Ridge (C=0.0001) was trained and compared with the same model without the `product_type` variable.  
![plots](https://github.com/MaickMos/zrive-ds/blob/686a77aed98b68f3ab4ad15dad5e737b30cef5ff/src/module_3/images/Image_6.png)

**Observations:**  
* Ridge improves over baseline, but Lasso shows the best performance.  
* Lasso reduces low-weight coefficients to zero; only the three main variables remain.

The final Lasso model (C=0.0001) is saved with these three variables.

# Script to Load the Model
The script `load_model.py` was created to load the model and normalizer.  

It includes functions to:
* Load the dataset with original columns
* Preprocess data: given User and Product, outputs user and product features
* Load model from path
* Standardize data using `StandardScaler` from sklearn
* Predict probabilities: calls necessary functions to load the model and dataset and make predictions
