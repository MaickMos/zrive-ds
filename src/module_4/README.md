# Push Notifications Module #4
This PR delivers the continuation of the predictive model for potential users interested in a product. Given a user and a product, it predicts whether they would buy that product if they were purchasing at that moment. Conditions: users must have purchased at least 5 products. This time, non-linear models were used.

## Dataset Preparation
The same dataset from the previous practice was used, along with a variation where the main features selected by a random forest were observed, resulting in 9 features.

## Evaluation Metrics
The same evaluation metrics were applied within a function, and new metrics were added:
- `roc_auc_score`
- `log_loss`
- `average_precision_score`

Previous metrics are still used:
- Recall
- Precision-Recall Curve
- ROC Curve

## Models
The best baseline and logistic regression models are retained for future comparisons.

### Random Forest
A test was performed with the random forest on the full dataset, yielding poor results: average precision of 0.014 and AUC in the precision-recall curve of 0.02 on the test set.  
Features with importance greater than 3% were selected, creating a new dataset with 9 variables.  
This dataset was compared with the previous 3-variable dataset. Better results were obtained, with the best performance on the 3-variable test set: AUC 0.10 and average precision 0.027.  

Finally, tests were performed with 5, 10, and 100 trees using the 3-variable dataset. Similar test results were obtained, with the best model using 10 trees (AUC 0.14, average precision 0.046).  
This model was selected as it performs similarly to the 100-tree default model.

### Gradient Boosting Trees
A test was performed with hyperparameters: `n_estimators=100`, `learning_rate=0.05`, and `max_depth=5`.  
Results were similar to the random forest.  
Variations in learning rate and tree depth were tested, with the best performance achieved at `learning_rate=0.05` and `max_depth=5`.

### Comparison
The four models were compared, and the conclusion was:

Logistic regression with Ridge regularization was the best model for recall values in the range 0.1 to 0.3, achieving an AUC of 0.16 in the precision-recall curve.  

Different dataset versions were tested: the full numerical dataset, the dataset with coefficients greater than 0.03, and the dataset with the three most important variables. In all models, the best performance was obtained using the three most important variables. Interestingly, this also applied to tree-based models, but no adjustment significantly improved their performance.  

All models outperformed the baseline, confirming their predictive value. Logistic regression remains the best choice in this case. Tree-based models may require deeper hyperparameter tuning, or the relationships between variables may be more linear, favoring regression.

# Script to Load the Model
## Fit
The script `fit.py` was created, which allows loading the configuration for a logistic regression model with the generated date and time, saving it to a path and returning the saved location.

## Predict
The script loads a saved model from a path, transforms the input data, and generates predictions.
