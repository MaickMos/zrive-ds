#### **Changes Implemented**  
1. **Baseline Creation:**  
   - A baseline model was created to compare performance.  
   - Used **average surplus** (difference between current value and 5-year average).  
   - The model performed **better than the baseline**, but this could be due to **data leakage**.  

2. **Overfitting Check:**  
   - Used **binary log loss** to evaluate overfitting.  
   - Plotted its evolution as the number of trees increased.  
   - Initially, used **line plots**, later switched to **boxplots** for better visualization.  
   - **Observed overfitting** after a certain number of trees (log loss decreased in validation).  
   - **Limited the number of trees to 12** to prevent overfitting.  

3. **Feature Importance Analysis:**  
   - Detected **anomalous feature values** related to **The CYCC Case**.  
   - Identified and **removed features causing data leakage**.  

4. **Final Model Training:**  
   - Retrained models after removing data leakage and overfitting issues.  
   - **Performance decreased** but is now **free of biases**.  
   - Model now performs similarly to the **baseline**, but takes **riskier decisions**, achieving the same average return as a **more conservative benchmark**.

Code Writer: @sergiorozada12 