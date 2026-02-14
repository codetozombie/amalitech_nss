import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from helpers import assign_category, wrangle

# --- 1. CONFIG & DATA LOADING ---
st.set_page_config(page_title="Nutrient Matrix", layout="wide")

@st.cache_data
def load_data():
    # Load data using your helper function
    df = wrangle("dataset_vs.csv")
    
    # Apply your categorization helper
    df['high_level_category'] = df.apply(assign_category, axis=1)
    
    # Calculate Ratio Safely (Avoid division by zero)
    # We replace 0 sugar with 0.1 for the math
    df['safe_sugar'] = df['sugars_100g'].replace(0, 0.1)
    df['protein_sugar_ratio'] = df['proteins_100g'] / df['safe_sugar']
    
    return df

df = load_data()

# --- 2. DASHBOARD HEADER ---
st.title("🍎 The Nutrient Matrix Dashboard")
st.markdown("Identify product clusters and spot the **'High Protein, Low Sugar'** opportunity gap.")

# --- 3. SIDEBAR FILTERS ---
st.sidebar.header("Filter Settings")

# Get unique categories for the dropdown
all_cats = sorted(df['high_level_category'].unique())

selected_cats = st.sidebar.multiselect(
    "Select Categories:",
    options=all_cats,
    # Select a few defaults to make the chart look good initially
    default=[c for c in ['Nuts & Seeds', 'Meat & Seafood', 'Energy & Cereal Bars', 'Chips & Popcorn'] if c in all_cats]
)

if not selected_cats:
    st.warning("⚠️ Please select at least one category from the sidebar.")
    st.stop()

# Filter the dataframe
filtered_df = df[df['high_level_category'].isin(selected_cats)].copy()

# --- 4. STORY 4: THE RECOMMENDATION ENGINE ---
# Logic: Find the "Winning" Category in the Opportunity Zone
# Zone Definition: Protein > 15g AND Sugar < 5g
zone_df = filtered_df[
    (filtered_df['sugars_100g'] < 5) & 
    (filtered_df['proteins_100g'] > 15)
]

st.subheader("💡 Key Insight & Recommendation")

if not zone_df.empty:
    # 1. Identify the category with the most "Healthy" products (Validated Market)
    best_category = zone_df['high_level_category'].value_counts().idxmax()
    
    # 2. Calculate the average specs for that specific winning category
    # We only look at products belonging to the best category INSIDE the zone
    cat_stats = zone_df[zone_df['high_level_category'] == best_category]
    avg_prot = cat_stats['proteins_100g'].mean()
    avg_sug = cat_stats['sugars_100g'].mean()
    
    # 3. Display the Recommendation (Dynamic Text)
    st.success(f"Based on the data, the biggest market opportunity is in **{best_category}**, "
               f"specifically targeting products with **{avg_prot:.1f}g** of protein "
               f"and less than **{avg_sug:.1f}g** of sugar.")
else:
    st.info("No clear recommendation found with current filters. Try selecting 'Nuts & Seeds' or 'Meat & Seafood'.")

# --- 5. CHART & METRICS LAYOUT ---
col_chart, col_metrics = st.columns([3, 1])

with col_chart:
    # The Plotly Scatter Plot
    fig = px.scatter(
        filtered_df,
        x="sugars_100g",
        y="proteins_100g",
        color="high_level_category",
        hover_name="product_name",
        hover_data={
            "high_level_category": False,
            "proteins_100g": ":.1f g",
            "sugars_100g": ":.1f g",
            "protein_sugar_ratio": ":.1f"
        },
        title="<b>Nutrient Matrix:</b> Protein vs. Sugar Content",
        template="plotly_white",
        height=550,
        opacity=0.7
    )
    
    # Reference Lines
    fig.add_vline(x=5, line_dash="dash", line_color="red", annotation_text="Low Sugar (<5g)")
    fig.add_hline(y=15, line_dash="dash", line_color="green", annotation_text="High Protein (>15g)")
    
    # Green Zone Box
    fig.add_shape(type="rect", x0=0, y0=15, x1=5, y1=100, line=dict(width=0), fillcolor="green", opacity=0.1)
    
    st.plotly_chart(fig, use_container_width=True)

with col_metrics:
    st.subheader("📊 Zone Analysis")
    st.markdown("**Top-Left Quadrant Metrics**")
    
    st.metric("Total Products in Zone", zone_df.shape[0])
    
    if not zone_df.empty:
        vol_winner = zone_df['high_level_category'].value_counts().idxmax()
        vol_count = zone_df['high_level_category'].value_counts().max()
        st.metric("📦 Volume Leader", vol_winner, f"{vol_count} items")
        
        qual_winner = zone_df.groupby('high_level_category')['protein_sugar_ratio'].mean().idxmax()
        qual_score = zone_df.groupby('high_level_category')['protein_sugar_ratio'].mean().max()
        st.metric("💪 Quality Leader", qual_winner, f"{qual_score:.1f} Ratio")

# --- 6. LEADERBOARD ---
st.markdown("---")
st.subheader("🏆 Leaderboard: Top 5 'Power Foods'")

leaderboard = (
    filtered_df
    .sort_values(by='protein_sugar_ratio', ascending=False)
    .groupby('high_level_category')
    .head(5)
    [['high_level_category', 'product_name', 'proteins_100g', 'sugars_100g', 'protein_sugar_ratio']]
)

st.dataframe(
    leaderboard,
    use_container_width=True,
    hide_index=True,
    column_config={
        "high_level_category": "Category",
        "product_name": "Product Name",
        "proteins_100g": st.column_config.NumberColumn("Protein", format="%.1f g"),
        "sugars_100g": st.column_config.NumberColumn("Sugar", format="%.1f g"),
        "protein_sugar_ratio": st.column_config.NumberColumn("Ratio", format="%.1f x")
    }
)