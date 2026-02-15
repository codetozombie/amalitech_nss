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
To ensure analysis accuracy, the following cleaning steps were performed:
1.  **Handling Missing Values:** [e.g., Imputed missing nutritional values using the median of their respective product categories.]
2.  **Duplicate Removal:** [e.g., Removed duplicate entries based on barcode (code) and product name.]
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