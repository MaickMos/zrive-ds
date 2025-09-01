# Module 2 Submission
This PR includes the initial data analysis for understanding the problem space.

## Results
The datasets were loaded and manipulated. Data was checked to identify possible issues and corrected. An exploration of the problem was performed through data querying and hypothesis testing.  
Finally, the findings were documented in a Jupyter Notebook.  

A very similar process was carried out with the second dataset, where issues were discovered for proper analysis. All findings were documented in a Jupyter Notebook.

## Organization
Documents were organized by modules:
* Get the data
* Initial Checks
* Hypothesis Testing
* Insights
S
## Insights for _"Understanding the problem space"_
* Only 325 rows have certain columns; it could be a survey. These data are distributed across the entire data period.
* The percentage of people without babies, children, or pets is 38.77%
* The UKI region has the highest number of users, and the UKD region has the most proportional difference between user segments at 10.9%
* There are 448 products that are not _Regulars_
* _Long-life milk substitutes_ are the best-selling products
* Bioma is the largest supplier
* 28% of users had more than one order sequence
* 15.7% of products were purchased without inventory

## Insights for _Exploratory Data Analysis_
* The distribution of _"outcome"_ (purchased vs not purchased orders) is highly imbalanced, with a ratio of 99 to 1
* A purchase is more likely if the product was previously bought compared to other measured metrics such as abandoned, _snoozed_, or _set as regular_
* The best-selling product is _tinspackagedfoods_, and the top supplier is _biona_
* There is a correlation where families with more children tend to have more pets
* The number of people (excluding babies) is also correlated with the number of pets
* The distribution of _"outcome"_ with respect to _"count_adults"_ shows an inconsistent increase at the value of 2, because most values in the column were imputed from the main survey, affecting the analysis results

Code reviewer: @sergiorozada12
