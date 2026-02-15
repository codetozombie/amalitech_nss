import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# data loading and processing
st.set_page_config(page_title="Nutrient Matrix", layout="wide")

@st.cache_data
def load_data():
    # Load your dataset
    df = pd.read_csv("dataset/snacks.csv")
    
    # Ensure numerical columns are actually numbers
    df['proteins_100g'] = pd.to_numeric(df['proteins_100g'], errors='coerce').fillna(0)
    df['sugars_100g'] = pd.to_numeric(df['sugars_100g'], errors='coerce').fillna(0)
    
    # Calculate Ratio Safely (Avoid division by zero)
    # We replace 0 sugar with 0.1 to allow for the math calculation
    df['safe_sugar'] = df['sugars_100g'].replace(0, 0.1)
    df['protein_sugar_ratio'] = df['proteins_100g'] / df['safe_sugar']
    
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}. Please ensure 'snacks.csv' is in the directory.")
    st.stop()

# dashboard title and description
st.title("The Nutrient Matrix Dashboard")
st.markdown("Identify product clusters and spot the **'High Protein, Low Sugar'** opportunity gap.")

# siderbar filters
st.sidebar.header("Filter Settings")

# get unique categories for the multiselect
all_cats = sorted(df['high_level_category'].unique())

selected_cats = st.sidebar.multiselect(
    "Select Categories:",
    options=all_cats,
    # select the defaults
    default=[c for c in ['Nuts & Seeds', 'Meat & Seafood', 'Energy & Cereal Bars', 'Chips & Popcorn'] if c in all_cats]
)

if not selected_cats:
    st.warning("Please select at least one category from the sidebar.")
    st.stop()

# filter the dataframe based on selected categories
filtered_df = df[df['high_level_category'].isin(selected_cats)].copy()

# recommendation logic
# define the "Opportunity Zone" as products with low sugar (<5g) and high protein (>20g)
zone_df = filtered_df[
    (filtered_df['sugars_100g'] < 5) & 
    (filtered_df['proteins_100g'] > 20)
]

st.subheader("Key Insight & Recommendation")

if not zone_df.empty:
    # group by category and calculate the average protein-to-sugar ratio as a "Quality Score"
    quality_scores = zone_df.groupby('high_level_category')['protein_sugar_ratio'].mean()
    
    # pick the category with the highest average ratio as the "Best Opportunity"
    best_category = quality_scores.idxmax()
    
    # get the average protein and sugar values for that category to provide specific targets
    cat_stats = zone_df[zone_df['high_level_category'] == best_category]
    avg_prot = cat_stats['proteins_100g'].mean()
    avg_sug = cat_stats['sugars_100g'].mean()
    
    # display the recommendation
    st.success(f"Based on the data, the biggest market opportunity is in **{best_category}**, "
               f"specifically targeting products with more than **{avg_prot:.0f}g** of protein "
               f"and less than **{avg_sug:.1f}g** of sugar.")
    
    st.caption(f"Why this category? While other categories may have more products, **{best_category}** "
               "offers the highest nutritional density (Protein-to-Sugar ratio), representing a 'Quality' gap in the market.")

else:
    st.info("No clear recommendation found with current filters. Try selecting 'Meat & Seafood' to see the opportunity.")

#chart and metrics
col_chart, col_metrics = st.columns([3, 1])

with col_chart:
    # plotly scatter plot
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
        template="plotly_dark", # color scheme
        height=550,
        opacity=0.7
    )
    
    # refine axes
    fig.add_vline(x=5, line_dash="dash", line_color="red", annotation_text="Low Sugar (<5g)")
    fig.add_hline(y=20, line_dash="dash", line_color="green", annotation_text="High Protein (>20g)")
    
    # highlight the "Opportunity Zone" with a shaded rectangle
    fig.add_shape(type="rect", x0=0, y0=20, x1=5, y1=100, line=dict(width=0), fillcolor="green", opacity=0.1)
    
    st.plotly_chart(fig, use_container_width=True)

with col_metrics:
    st.subheader("Zone Analysis")
    st.markdown("**Top-Left Quadrant Metrics**")
    
    st.metric("Total Products in Zone", zone_df.shape[0])
    
    if not zone_df.empty:
        # volume leader
        vol_winner = zone_df['high_level_category'].value_counts().idxmax()
        vol_count = zone_df['high_level_category'].value_counts().max()
        st.metric("Volume Leader (Saturated)", vol_winner, f"{vol_count} items")
        
        # quality leader 
        qual_winner = zone_df.groupby('high_level_category')['protein_sugar_ratio'].mean().idxmax()
        qual_score = zone_df.groupby('high_level_category')['protein_sugar_ratio'].mean().max()
        st.metric("Quality Leader (Opportunity)", qual_winner, f"{qual_score:.1f} Ratio")

#leaderboard
st.markdown("---")
st.subheader("Leaderboard: Top 5 'Power Foods'")

# sort by ratio and get top 5 per category
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