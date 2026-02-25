"""
Palm Oil Sourcing Optimization - Streamlit App
Interactive dashboard using precomputed optimization results
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import pickle
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Palm Oil Sourcing Optimization",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2E8B57;
        margin: 0.5rem 0;
    }
    .success-metric {
        color: #28a745;
        font-weight: bold;
    }
    .warning-metric {
        color: #ffc107;
        font-weight: bold;
    }
    .danger-metric {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_precomputed_data():
    """Load all precomputed data files."""
    try:
        # Load scenarios summary
        scenarios_df = pd.read_csv('precomputed_results/precomputed_scenarios_summary.csv')
        
        # Load detailed results
        with open('precomputed_results/precomputed_detailed_results.json', 'r') as f:
            detailed_results = json.load(f)
        
        # Load metadata
        with open('precomputed_results/precomputed_metadata.pkl', 'rb') as f:
            metadata = pickle.load(f)
        
        # Load supplier allocations if available
        try:
            allocations_df = pd.read_parquet('precomputed_results/precomputed_supplier_allocations.parquet')
        except:
            allocations_df = None
        
        return scenarios_df, detailed_results, metadata, allocations_df
    
    except Exception as e:
        st.error(f"Error loading precomputed data: {str(e)}")
        return None, None, None, None

def get_available_parameters(scenarios_df):
    """Extract available parameter values from the data."""
    return {
        'volumes': sorted(scenarios_df['volume'].unique()),
        'risk_weights': sorted(scenarios_df['risk_weight'].unique()),
        'max_shares': sorted(scenarios_df['max_share'].unique()),
        'min_suppliers': sorted(scenarios_df['min_supplier'].unique())
    }

def find_matching_scenario(scenarios_df, volume, risk_weight, max_share, min_supplier):
    """Find the scenario that matches the selected parameters."""
    # First try exact match
    mask = (
        (scenarios_df['volume'] == volume) &
        (scenarios_df['risk_weight'] == risk_weight) &
        (scenarios_df['max_share'] == max_share) &
        (scenarios_df['min_supplier'] == min_supplier)
    )
    
    matching_scenarios = scenarios_df[mask]
    if len(matching_scenarios) > 0:
        return matching_scenarios.iloc[0]
    
    # If no exact match, find closest volume and risk_weight
    scenarios_df['volume_diff'] = abs(scenarios_df['volume'] - volume)
    scenarios_df['risk_diff'] = abs(scenarios_df['risk_weight'] - risk_weight)
    
    # Filter by exact matches for max_share and min_supplier
    filtered_df = scenarios_df[
        (scenarios_df['max_share'] == max_share) &
        (scenarios_df['min_supplier'] == min_supplier)
    ]
    
    if len(filtered_df) > 0:
        # Find closest match by volume and risk_weight
        closest_idx = filtered_df['volume_diff'].add(filtered_df['risk_diff']).idxmin()
        return scenarios_df.loc[closest_idx]
    
        return None

def get_detailed_result(detailed_results, volume, risk_weight, max_share, min_supplier):
    """Get detailed result for the selected parameters."""
    # First try exact match
    for result in detailed_results:
        params = result['parameters']
        if (params['volume'] == volume and 
            params['risk_weight'] == risk_weight and 
            params['max_share'] == max_share and 
            params['min_supplier'] == min_supplier):
            return result
    
    # If no exact match, find closest match
    best_result = None
    min_distance = float('inf')
    
    for result in detailed_results:
        params = result['parameters']
        if (params['max_share'] == max_share and 
            params['min_supplier'] == min_supplier):
            # Calculate distance based on volume and risk_weight
            volume_diff = abs(params['volume'] - volume)
            risk_diff = abs(params['risk_weight'] - risk_weight)
            total_distance = volume_diff + risk_diff * 1000  # Weight risk more heavily
            
            if total_distance < min_distance:
                min_distance = total_distance
                best_result = result
    
    return best_result

def create_cost_comparison_chart(scenario):
    """Create a cost comparison chart."""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Baseline',
        x=['Cost'],
        y=[scenario['baseline_cost']],
        marker_color='lightcoral',
        text=[f"{scenario['baseline_cost']:.0f}"],
        textposition='auto'
    ))
    
    fig.add_trace(go.Bar(
        name='Optimized',
        x=['Cost'],
        y=[scenario['optimized_cost']],
        marker_color='lightgreen',
        text=[f"{scenario['optimized_cost']:.0f}"],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Cost Comparison (per tonne)",
        xaxis_title="",
        yaxis_title="Cost ($)",
        barmode='group',
        height=400,
        showlegend=True,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig

def create_emissions_comparison_chart(scenario):
    """Create an emissions comparison chart."""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Baseline',
        x=['Emissions'],
        y=[scenario['baseline_emissions']],
        marker_color='lightcoral',
        text=[f"{scenario['baseline_emissions']:.3f}"],
        textposition='auto'
    ))
    
    fig.add_trace(go.Bar(
        name='Optimized',
        x=['Emissions'],
        y=[scenario['optimized_emissions']],
        marker_color='lightgreen',
        text=[f"{scenario['optimized_emissions']:.3f}"],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Emissions Comparison (KPI)",
        xaxis_title="",
        yaxis_title="Emissions KPI",
        barmode='group',
        height=400,
        showlegend=False,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig

def create_deforestation_comparison_chart(scenario):
    """Create a deforestation comparison chart."""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Baseline',
        x=['Deforestation'],
        y=[scenario['baseline_deforestation']],
        marker_color='lightcoral',
        text=[f"{scenario['baseline_deforestation']:.5f}"],
        textposition='auto'
    ))
    
    fig.add_trace(go.Bar(
        name='Optimized',
        x=['Deforestation'],
        y=[scenario['optimized_deforestation']],
        marker_color='lightgreen',
        text=[f"{scenario['optimized_deforestation']:.5f}"],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Deforestation Comparison (KPI)",
        xaxis_title="",
        yaxis_title="Deforestation KPI",
        barmode='group',
        height=400,
        showlegend=False,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig

def create_supplier_allocation_chart(detailed_result):
    """Create a chart showing supplier allocations."""
    if not detailed_result or detailed_result['status'] != 'completed':
        return None
    
    final_plan = pd.DataFrame(detailed_result['final_plan'])
    
    # Sort by volume sourced
    final_plan = final_plan.sort_values('Volume_Sourced', ascending=True)
    
    fig = px.bar(
        final_plan, 
        x='Volume_Sourced', 
        y='exporter_group',
        orientation='h',
        title="Supplier Allocations",
        labels={'Volume_Sourced': 'Volume Sourced (tonnes)', 'exporter_group': 'Supplier'}
    )
    
    fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
    return fig

def main():
    # Header
    st.markdown('<h1 class="main-header">🌿 Palm Oil Sourcing Optimization Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading precomputed data..."):
        scenarios_df, detailed_results, metadata, allocations_df = load_precomputed_data()
    
    if scenarios_df is None:
        st.error("Failed to load precomputed data. Please ensure the precomputed_results folder exists.")
        return
    
    # Sidebar for parameter selection
    st.sidebar.header("🎛️ Parameter Selection")
    
    # Get available parameters
    params = get_available_parameters(scenarios_df)
    
    # Create sliders and radio buttons
    st.sidebar.markdown("### 📊 Volume & Risk Settings")
    selected_volume = st.sidebar.slider(
        "Volume Required (tonnes)",
        min_value=min(params['volumes']),
        max_value=max(params['volumes']),
        value=200000,
        step=50000,
        help="Total volume of palm oil to source",
        format="%d"
    )
    
    selected_risk_weight = st.sidebar.slider(
        "Sustainability Weight",
        min_value=min(params['risk_weights']),
        max_value=max(params['risk_weights']),
        value=1.0,
        step=0.25,
        help="Weight given to risk factors (0 = no risk consideration, 1 = full risk consideration)",
        format="%.2f"
    )
    
    st.sidebar.markdown("### 🏢 Supplier Settings")
    selected_max_share = st.sidebar.select_slider(
        "Max Share per Supplier",
        options=params['max_shares'],
        value=0.5 if 0.5 in params['max_shares'] else params['max_shares'][0],
        help="Maximum percentage of total volume any single supplier can provide",
        format_func=lambda x: f"{x*100:.0f}%"
    )
    
    selected_min_suppliers = st.sidebar.select_slider(
        "Minimum Number of Suppliers",
        options=params['min_suppliers'],
        value=6 if 6 in params['min_suppliers'] else params['min_suppliers'][0],
        help="Minimum number of suppliers to include in the sourcing plan"
    )
    
    # Find matching scenario
    scenario = find_matching_scenario(
        scenarios_df, selected_volume, selected_risk_weight, 
        selected_max_share, selected_min_suppliers
    )
    
    if scenario is None:
        st.error("No precomputed results found for the selected parameters.")
        return
    
    # Check if we're using exact match or closest match
    exact_match = (
        scenario['volume'] == selected_volume and 
        scenario['risk_weight'] == selected_risk_weight
    )
    
    if not exact_match:
        st.info(f"📊 Showing results for closest match: Volume={scenario['volume']:,} tonnes, Risk Weight={scenario['risk_weight']}")
    
    if scenario['status'] != 'completed':
        st.error(f"Selected scenario has status: {scenario['status']}")
        if 'error' in scenario:
            st.error(f"Error: {scenario['error']}")
        return
    
    # Main content area
    st.header("📊 Optimization Results")
    
    # Key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        cost_change = scenario['optimized_cost'] - scenario['baseline_cost']
        cost_improvement = ((scenario['baseline_cost'] - scenario['optimized_cost']) / scenario['baseline_cost']) * 100
        st.markdown("**Cost Improvement**")
        if cost_change < 0:  # Cost went down (good)
            st.markdown(f"<h2 style='color: green;'>{cost_improvement:.1f}%</h2>", unsafe_allow_html=True)
            st.caption(f"↓ {scenario['baseline_cost']:.0f} → {scenario['optimized_cost']:.0f}")
        else:  # Cost went up (bad)
            st.markdown(f"<h2 style='color: red;'>+{abs(cost_improvement):.1f}%</h2>", unsafe_allow_html=True)
            st.caption(f"↑ {scenario['baseline_cost']:.0f} → {scenario['optimized_cost']:.0f}")
    
    with col2:
        emissions_change = scenario['optimized_emissions'] - scenario['baseline_emissions']
        emissions_improvement = ((scenario['baseline_emissions'] - scenario['optimized_emissions']) / scenario['baseline_emissions']) * 100
        st.markdown("**Emissions Reduction**")
        if emissions_change < 0:  # Emissions went down (good)
            st.markdown(f"<h2 style='color: green;'>{emissions_improvement:.1f}%</h2>", unsafe_allow_html=True)
            st.caption(f"↓ {scenario['baseline_emissions']:.3f} → {scenario['optimized_emissions']:.3f}")
        else:  # Emissions went up (bad)
            st.markdown(f"<h2 style='color: red;'>+{abs(emissions_improvement):.1f}%</h2>", unsafe_allow_html=True)
            st.caption(f"↑ {scenario['baseline_emissions']:.3f} → {scenario['optimized_emissions']:.3f}")
        
    with col3:
        deforestation_change = scenario['optimized_deforestation'] - scenario['baseline_deforestation']
        deforestation_improvement = ((scenario['baseline_deforestation'] - scenario['optimized_deforestation']) / scenario['baseline_deforestation']) * 100
        st.markdown("**Deforestation Reduction**")
        if deforestation_change < 0:  # Deforestation went down (good)
            st.markdown(f"<h2 style='color: green;'>{deforestation_improvement:.1f}%</h2>", unsafe_allow_html=True)
            st.caption(f"↓ {scenario['baseline_deforestation']:.5f} → {scenario['optimized_deforestation']:.5f}")
        else:  # Deforestation went up (bad)
            st.markdown(f"<h2 style='color: red;'>+{abs(deforestation_improvement):.1f}%</h2>", unsafe_allow_html=True)
            st.caption(f"↑ {scenario['baseline_deforestation']:.5f} → {scenario['optimized_deforestation']:.5f}")
    
    with col4:
        st.markdown("**Suppliers Used**")
        st.markdown(f"<h2 style='color: #1f77b4;'>{scenario['supplier_count']}</h2>", unsafe_allow_html=True)
        st.caption(f"Volume: {scenario['total_volume_sourced']:,.0f} tonnes")
    
    # Charts section
    st.header("📈 Performance Comparison")
    
    # Create three separate charts horizontally aligned
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig_cost = create_cost_comparison_chart(scenario)
        st.plotly_chart(fig_cost, use_container_width=True)
    
    with col2:
        fig_emissions = create_emissions_comparison_chart(scenario)
        st.plotly_chart(fig_emissions, use_container_width=True)
    
    with col3:
        fig_deforestation = create_deforestation_comparison_chart(scenario)
        st.plotly_chart(fig_deforestation, use_container_width=True)
    
    # Get detailed result for supplier allocations
    detailed_result = get_detailed_result(
        detailed_results, selected_volume, selected_risk_weight, 
        selected_max_share, selected_min_suppliers
    )
    
    if detailed_result and detailed_result['status'] == 'completed':
        st.header("🏢 Supplier Insights")
        tab_alloc, tab_details = st.tabs(["Supplier Allocations", "Detailed Supplier Information"]) 

        with tab_alloc:
            st.subheader("Supplier Allocations")
            # Supplier allocation chart
            fig_allocations = create_supplier_allocation_chart(detailed_result)
            if fig_allocations:
                st.plotly_chart(fig_allocations, use_container_width=True)

        with tab_details:
            st.subheader("Detailed Supplier Information")
            final_plan = pd.DataFrame(detailed_result['final_plan'])
            
            # Format the dataframe for display
            display_df = final_plan[['exporter_group', 'Volume_Sourced', 'final_score', 
                                    'avg_cost_per_tonne', 'avg_emissions_kpi', 'avg_deforestation_kpi']].copy()
            display_df.columns = ['Supplier', 'Volume Sourced (tonnes)', 'Final Score', 
                                 'Avg Cost per Tonne', 'Avg Emissions KPI', 'Avg Deforestation KPI']
            
            # Round numeric columns
            numeric_cols = ['Volume Sourced (tonnes)', 'Final Score', 'Avg Cost per Tonne', 
                           'Avg Emissions KPI', 'Avg Deforestation KPI']
            for col in numeric_cols:
                display_df[col] = display_df[col].round(4)
            
            st.dataframe(display_df, use_container_width=True)
            
            # Download button for results
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Supplier Allocations (CSV)",
                data=csv,
                file_name=f"supplier_allocations_{selected_volume}_{selected_risk_weight}_{selected_max_share}_{selected_min_suppliers}.csv",
                mime="text/csv"
            )
            
    # Summary statistics
    st.header("📋 Summary Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Selected Parameters")
        st.write(f"**Volume Required:** {selected_volume:,} tonnes")
        st.write(f"**Risk Weight:** {selected_risk_weight}")
        st.write(f"**Max Share per Supplier:** {selected_max_share*100:.0f}%")
        st.write(f"**Minimum Suppliers:** {selected_min_suppliers}")
    
    with col2:
        st.subheader("Optimization Results")
        st.write(f"**Total Volume Sourced:** {scenario['total_volume_sourced']:,.0f} tonnes")
        st.write(f"**Number of Suppliers:** {scenario['supplier_count']}")
        st.write(f"**Average Cost per Tonne:** {scenario['optimized_cost']:.2f}")
        st.write(f"**Average Emissions KPI:** {scenario['optimized_emissions']:.4f}")
        st.write(f"**Average Deforestation KPI:** {scenario['optimized_deforestation']:.6f}")
    

   
if __name__ == "__main__":
    main()
