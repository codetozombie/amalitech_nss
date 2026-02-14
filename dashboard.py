import streamlit as st
import plotly.express as px
import pandas as pd
from helpers import assign_category, wrangle

# 1. SETUP & DATA LOAD
st.set_page_config(page_title="Nutrient Matrix", layout="wide")

# Assume 'df' is loaded or load it here
df = wrangle("dataset_vs.csv")

# Apply your classifier function
df['high_level_category'] = df.apply(assign_category, axis=1)

# 2. DASHBOARD HEADER
st.title("🍎 The Nutrient Matrix Dashboard")
st.markdown("Identify product clusters and spot the **'High Protein, Low Sugar'** opportunity gap.")

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filters")
selected_cats = st.sidebar.multiselect(
    "Select Categories:",
    options=df['high_level_category'].unique(),
    default=df['high_level_category'].unique() # Select all by default
)

# Filter Data based on selection
filtered_df = df[df['high_level_category'].isin(selected_cats)]

# --- INTERACTIVE PLOT (Plotly) ---
col1, col2 = st.columns([3, 1])

with col1:
    fig = px.scatter(
        filtered_df,
        x="sugars_100g",
        y="proteins_100g",
        color="high_level_category",
        hover_name="product_name", 
        # FIX: Removed 'brands' because it is missing from your CSV
        hover_data=["sugars_100g", "proteins_100g"],
        title="Sugar vs. Protein Content",
        template="plotly_white",
        height=600,
        opacity=0.7
    )

    # Add Quadrant Lines (The "Golden Cross")
    fig.add_vline(x=5, line_dash="dash", line_color="red", annotation_text="Low Sugar (<5g)")
    fig.add_hline(y=15, line_dash="dash", line_color="green", annotation_text="High Protein (>15g)")

    st.plotly_chart(fig, use_container_width=True)

# --- METRICS SECTION (Right Column) ---
# --- METRICS SECTION (Right Column) ---
with col2:
    st.subheader("📊 Key Insights")
    
    # 1. Define the "Opportunity Zone"
    opportunity_df = filtered_df[
        (filtered_df['sugars_100g'] < 5) & 
        (filtered_df['proteins_100g'] > 15)
    ].copy() # Use .copy() to avoid SettingWithCopy warnings
    
    # Calculate Ratio for the metrics (Safe division)
    opportunity_df['safe_sugar'] = opportunity_df['sugars_100g'].replace(0, 0.1)
    opportunity_df['ratio'] = opportunity_df['proteins_100g'] / opportunity_df['safe_sugar']

    # Metric 1: Total Count
    opportunity_count = opportunity_df.shape[0]
    st.metric(label="Products in Opportunity Zone", value=opportunity_count)
    
    if not opportunity_df.empty:
        # Metric 2: Volume Winner (The Category with the MOST items)
        top_vol_cat = opportunity_df['high_level_category'].value_counts().idxmax()
        top_vol_count = opportunity_df['high_level_category'].value_counts().max()
        st.metric(
            label="🏆 Most Options (Volume)", 
            value=top_vol_cat, 
            delta=f"{top_vol_count} products"
        )

        # Metric 3: Quality Winner (The Category with the BEST Average Ratio)
        # We group by category and take the MEAN of the ratio
        best_ratio_cat = opportunity_df.groupby('high_level_category')['ratio'].mean().idxmax()
        best_ratio_val = opportunity_df.groupby('high_level_category')['ratio'].mean().max()
        
        st.metric(
            label="🚀 Best Nutrition (Avg Ratio)", 
            value=best_ratio_cat, 
            delta=f"{best_ratio_val:.1f} P:S Ratio",
            help="Average Protein-to-Sugar ratio for products in the zone."
        )
    else:
        st.warning("No products found in the Opportunity Zone with current filters.")

    st.info("The 'Opportunity Zone' is defined as >15g Protein and <5g Sugar.")

# --- LEADERBOARD SECTION (Bottom) ---
st.markdown("---")
st.subheader(f"🏆 Top 5 High-Protein Products per Category")

# 1. Calculate the Ratio SAFELY
# We create a temporary 'safe_sugar' column where 0 is replaced by 0.1
# This avoids division by zero errors while keeping the math sortable.
filtered_df['safe_sugar'] = filtered_df['sugars_100g'].replace(0, 0.1)
filtered_df['protein_sugar_ratio'] = filtered_df['proteins_100g'] / filtered_df['safe_sugar']

# 2. Logic to get Top 5
top_products = (
    filtered_df
    .sort_values(by=['protein_sugar_ratio'], ascending=False) # Sort by your new Ratio!
    .groupby('high_level_category')
    .head(5)
    # Select the columns to display
    [['high_level_category', 'product_name', 'proteins_100g', 'sugars_100g', 'protein_sugar_ratio']]
)

# 3. Display with nice formatting
st.dataframe(
    top_products, 
    use_container_width=True,
    hide_index=True,
    column_config={
        "high_level_category": "Category",
        "product_name": "Product Name",
        "proteins_100g": st.column_config.NumberColumn("Protein (g)", format="%.1f"),
        "sugars_100g": st.column_config.NumberColumn("Sugar (g)", format="%.1f"),
        "protein_sugar_ratio": st.column_config.NumberColumn(
            "Protein:Sugar Ratio", 
            format="%.1f x", # Displays as "5.0 x" (5 times more protein than sugar)
            help="Higher is better. Shows how much Protein you get for every 1g of Sugar."
        ),
    }
)