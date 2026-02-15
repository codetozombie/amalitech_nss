# Market Gap Analysis

## A. The Executive Summary
[Insert Summary Here: e.g., "This analysis of the Open Food Facts dataset reveals a significant market gap in low-sugar, high-protein snacks in the West African region. While 60% of current products contain high sugar levels, consumer demand for healthier alternatives is rising. Our predictive model suggests that introducing a plant-based protein bar could capture a 15% market share within the first year."]

## B. Project Links
* **Notebook:** The fully work can be found in [GitHub repo link here](https://github.com/codetozombie/amalitech_nss) saved as `main.ipynb` and PDF and HTML files are also saved as `main.pdf` & `main.html` respectively. Furthermore the visualization for Story is saved as `app.py`
* **Dashboard:** [Link to Dashboard](https://codetozombie-amalitech-nss-app-iirfmj.streamlit.app/)
* **Presentation:** [Link to Slides (PDF/PPT)](YOUR_LINK_HERE)
* **Video Walkthrough (Optional):** [Link to YouTube](YOUR_LINK_HERE)

## C. Technical Explanation

### Data Cleaning
The full data cleaning and exploration was done in `helpers/task_1.ipynb` and a `wrangle` function was derived out it. The following was done clean the data.
1.  **Get rows with Snacks :** Subsetted the data to snacks only since we are dealing with Snacks
2.  **Drop Columns:** 
- Dropped coloumns with more than 80% of its values were missing
- Dropped "code", "url", "created_t", "created_datetime", "last_modified_t", 
    "last_modified_datetime", "last_modified_by", "last_updated_t", "last_updated_datetime" columns
    since I was not going to use them 
- Dropped columns  "categories", "categories_tags", "countries", "countries_tags", "main_category", "states", "states_tags". The duplicated each each other 
- Dropped columns "ingredients_tags", "ingredients_analysis_tags", "serving_size", "serving_quantity". I was not going to use them.
- Filled missing values in product_name and countries_en with "Unknown"
- Replace nutriscore_grade's missing vale with unknown
- replace missing nova_group(food_processed) with the most common value (mode)
- reomve rows with energy_kcal_100g > 900 i.e reaching its theoretical limits
- reomve rows with energy_100g > 4000 i.e reaching its theoretical limits
- reomve rows with fat_100g, sugars_100g, proteins_100g , fruits-vegetables-nuts-estimate-from-ingredients_100g, salt_100g, and cabohydrate_100g> 100 i.e reaching theoretical limits
- remove  saturated_fat_100g which did not satify the condition Saturated Fat must be <= Total Fat 
- reomve rows with fiber_100g > 40 i.e reaching theoretical limits
- reomve rows with nutrition-score-fr_100g < -15 or > 40 i. reaching its theoretical limits
- handle na values for categoies_en for snacks and convert to lowercase


3.  **Outlier Detection:** [e.g., Filtered out products with impossible values (e.g., sugar content > 100g per 100g).]

### Candidate's Choice
For the Candidate's Choice requirement, I implemented [Name of Feature/Analysis].
* **What I did:** [Brief description, e.g., "I added a sentiment analysis on product ingredients to flag potential allergens automatically."]
* **Why:** [Brief justification, e.g., "This feature helps users with dietary restrictions identify safe products instantly."]

---

## Project Structure
* `main.ipynb`: The main analysis code.
* `main.html` / `main.pdf`: Exported version of the analysis for easy viewing.
* `requirements.txt`: List of dependencies.
* `README.md`: Project documentation.
* `helpers/` : Consist each story attempted and rough work I did.
* `dataset/dataset_vs.csv` : The dataset is from the open food dataset where the first 100_000 rows where should. To get that after extracting the dataset on Windows run command in PowerShell ```Get-Content "en.openfoodfacts.org.products.csv" -TotalCount 100000 | Set-Content "openfoodfacts_100k.csv" ``` and Mac use this code in the Terminal ```head -n 100000 en.openfoodfacts.org.products.csv > openfoodfacts_100k.csv ``` and Linux use this command ```zcat en.openfoodfacts.org.products.csv.gz | head -n 100000 > openfoodfacts_100k.csv ```.
* `dataset/snacks.csv` : The formatted data to be used in the visualization.
* `app.py` : Script to open the visualizations using Streamlit.

## How to Run
1.  Clone the repository.
2. Create a `dataset` folder
2. Download the [Open Food Dataset](https://world.openfoodfacts.org/data) and extract the file in the `dataset` folder.
4. To get that after extracting the dataset on Windows run command in PowerShell ```Get-Content "en.openfoodfacts.org.products.csv" -TotalCount 100000 | Set-Content "openfoodfacts_100k.csv" ``` and Mac use this code in the Terminal ```head -n 100000 en.openfoodfacts.org.products.csv > openfoodfacts_100k.csv ``` and Linux use this command ```zcat en.openfoodfacts.org. Mind you rename accordingly.
2.  Install dependencies: `pip install -r requirements.txt`
3.  Open `main.ipynb` in Jupyter or VS Code and run all cells
4. To get the visualization run `streamlit run app.py` in the terminal