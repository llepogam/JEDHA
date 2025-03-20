import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="Getaround Delay Analysis",
    page_icon="🚗",
    layout="wide"
)

# App title
st.title("🚗 Getaround Rental Delay Analysis")

# Function to load and preprocess data
@st.cache_data
def load_data():
    try:
        # URL for the data
        url = 'https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx'
        
        try:
            st.write(f"Trying to load data from URL: {url}")
            df = pd.read_excel(url)
            st.success(f"Successfully loaded data from URL")
        except Exception as e:
            st.error(f"Error loading data from URL: {e}")
            
        # Remove debugging messages after successful load
        st.success("Data loaded successfully!")
        
        # Fill NaN values in time_delta (assuming NaN means >12h)
        df['time_delta_with_previous_rental_in_minutes'] = df['time_delta_with_previous_rental_in_minutes'].fillna(721)
        
        # Create time categories for analysis
        bins = [-np.inf, 30, 60, 180, 720, np.inf]
        labels = ['1. <30 minutes', '2. 30-60 minutes', '3. 1-3 hours', '4. 3-12 hours', '5. >12 hours']
        df['time_vs_previous_rental_category'] = pd.cut(
            df['time_delta_with_previous_rental_in_minutes'],
            bins=bins,
            labels=labels,
            right=False
        )
        
        # Add checkout status
        df.loc[df['delay_at_checkout_in_minutes'] < 0, 'checkout_status'] = 'Late'
        df.loc[df['delay_at_checkout_in_minutes'] >= 0, 'checkout_status'] = 'On time'
        df.loc[df['delay_at_checkout_in_minutes'].isna(), 'checkout_status'] = 'On time' # Let's assume that the nan is meaning that there are no delays
        
        # Add checkout delay categories
        bins_checkout = [-np.inf, -720, -120, -60, -30, 0, 30, 60, np.inf]
        labels_checkout = ['1. >12h late', '2. 2-12h late', '3. 1-2h late', '4. 30-60min late',
                        '5. <30min late', '6. <30min early', '7. 30-60min early', '8. >1h early']
        df['checkout_delay_category'] = pd.cut(
            df['delay_at_checkout_in_minutes'],
            bins=bins_checkout,
            labels=labels_checkout,
            right=False
        )
        
        # Add car rental frequency category
        car_rental_counts = df['car_id'].value_counts().reset_index()
        car_rental_counts.columns = ['car_id', 'rental_count']
        
        # Define rental frequency categories
        def categorize_frequency(count):
            if count == 1:
                return '1 rental'
            elif 2 <= count <= 3:
                return '2-3 rentals'
            elif 4 <= count <= 5:
                return '4-5 rentals'
            elif 6 <= count <= 10:
                return '6-10 rentals'
            else:
                return '>10 rentals'
        
        car_rental_counts['rental_frequency_category'] = car_rental_counts['rental_count'].apply(categorize_frequency)
        
        # Merge the frequency category back to the main dataframe
        df = df.merge(car_rental_counts[['car_id', 'rental_frequency_category']], on='car_id', how='left')
        

        df = df.merge(
            df[['rental_id', 'delay_at_checkout_in_minutes']],
            left_on='previous_ended_rental_id',
            right_on='rental_id',
            how='left',
            suffixes=('', '_previous')
        ).rename(columns={'delay_at_checkout_in_minutes_previous': 'delay_previous_rental'})
        
        df['gap_between_checkin_chekout']=df['time_delta_with_previous_rental_in_minutes']-df['delay_previous_rental']
        df['late_checkin'] = ''
        bins = [-np.inf, 0, np.inf]

        labels = ['Late', 'Not Late']

        df['late_checkin'] = pd.cut(
            df['gap_between_checkin_chekout'],
            bins=bins,
            labels=labels,
            right=False  
        )

        return df
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load data
df = load_data()

if df is not None:
    # Create tabs - adding "Key Insights" as the first tab
    tab0, tab1, tab2, tab3 = st.tabs(["Key Insights", "General Analysis", "Late Checkout Impact", "Threshold Analysis"])
    
    # Tab 0: Key Insights
    with tab0:
        st.header("Key Insights")
        
        # Calculate key metrics for insights
        total_rentals = len(df)
        connect_rentals = len(df[df['checkin_type'] == 'connect'])
        mobile_rentals = len(df[df['checkin_type'] == 'mobile'])
        connect_pct = connect_rentals / total_rentals * 100
        mobile_pct = mobile_rentals / total_rentals * 100
        
        late_checkouts = len(df[df['checkout_status'] == 'Late'])
        late_checkout_pct = late_checkouts / total_rentals * 100
        
        canceled_rentals = len(df[df['state'] == 'canceled'])
        canceled_pct = canceled_rentals / total_rentals * 100
        
        late_checkins = len(df[df['late_checkin'] == 'Late'])
        
        # Display metrics in columns
        st.subheader("Rental Overview")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Rentals", f"{total_rentals:,}")
        with col2:
            st.metric("Connect Rentals", f"{connect_rentals:,} ({connect_pct:.1f}%)")
        with col3:
            st.metric("Mobile Rentals", f"{mobile_rentals:,} ({mobile_pct:.1f}%)")
            
        st.subheader("Delay Impact")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Late Checkouts", f"{late_checkouts:,} ({late_checkout_pct:.1f}%)")
        with col2:
            st.metric("Canceled Rentals", f"{canceled_rentals:,} ({canceled_pct:.1f}%)")
        with col3:
            st.metric("Late Check-ins due to Previous Rental", f"{late_checkins:,}")
        
        # Summary text
        st.markdown("""
        ### Key Findings

        1. **Short time gaps between reservations represent a minor portion of business operations**: 
            - Out of 21k rentals, only 8% have a time gap below 12 hours between consecutive rentals
            - On average, each car is rented fewer than 3 times, indicating moderate utilization
            - Less than 400 rentals (approximately 2%) have a time gap below 1 hour from the previous rental

        2. **Late checkouts have limited impact on overall business operations**: 
            - Only 218 rentals were affected by late checkouts, where the car was not available at the scheduled time
            - The cancellation rate for affected rentals is around 17%, which is comparable to the average cancellation rate of 15%
            - Most delays were under 30 minutes, likely due to minor traffic issues, which wouldn't typically justify a cancellation

        3. **A buffer of 30-60 minutes between rentals appears sufficient to minimize scheduling conflicts**: 
            - Given the current rental frequency, aggressive time optimization does not appear necessary
            - Most delays are less than 1 hour, and this buffer would prevent most potential issues
            - Approximately 4% of reservations would be affected by implementing this threshold
        """)
            
    # Tab 1: General Analysis
    with tab1:
        st.header("General Analysis")
        
        # Key figures
        st.subheader("Key Figures")
        
        total_rentals = len(df)
        close_rentals = len(df[df['time_delta_with_previous_rental_in_minutes'] < 720])  # Less than 12 hours
        avg_rentals_per_car = df['car_id'].value_counts().mean()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Rentals", f"{total_rentals:,}")
        with col2:
            st.metric("% Rentals with <12h Gap between 2 rentals", f"{close_rentals/total_rentals:.1%}")
        with col3:
            st.metric("Avg. Rentals per Car", f"{avg_rentals_per_car:.1f}")
        
        # Histogram for distribution of selected columns
        st.subheader("Column Distribution")
        allowed_columns = [
            'checkin_type', 
            'state', 
            'time_vs_previous_rental_category', 
            'checkout_status', 
            'checkout_delay_category', 
            'rental_frequency_category'
        ]
        selected_column = st.selectbox("Select column to visualize", allowed_columns)
        
        # Create histogram for selected column
        if pd.api.types.is_numeric_dtype(df[selected_column]):
            fig = px.histogram(
                df, 
                x=selected_column,
                title=f"Distribution of {selected_column}"
            )
        else:
            # For categorical columns, show a bar chart instead
            value_counts = df[selected_column].value_counts().reset_index()
            value_counts.columns = ['Value', 'Count']
            fig = px.bar(
                value_counts,
                x='Value',
                y='Count',
                title=f"Distribution of {selected_column}"
            )
        
        st.plotly_chart(fig, use_container_width=True)

        # Graph showing distribution of reservations by time before previous rental
        st.subheader("Time Between Consecutive Rentals by State")
        
        # Filter out '>12 hours' category
        filtered_df = df
        
        # Group by time category and state
        time_state_dist = filtered_df.groupby(['time_vs_previous_rental_category', 'state']).size().reset_index()
        time_state_dist.columns = ['Time Category', 'State', 'Count']
        
        # Calculate total for each time category for percentage
        time_totals = filtered_df.groupby('time_vs_previous_rental_category').size().reset_index()
        time_totals.columns = ['Time Category', 'Total']
        
        # Merge to get the percentage
        time_state_dist = time_state_dist.merge(time_totals, on='Time Category')
        time_state_dist['Percentage'] = time_state_dist['Count'] / time_state_dist['Total'] * 100
        
        # Create the graph
        fig = px.bar(
            time_state_dist,
            x='Time Category',
            y='Percentage',
            color='State',
            barmode='stack',
            text=time_state_dist['Percentage'].round(1),
            title="Distribution of Time Between Consecutive Rentals by State",
            labels={'Percentage': 'Percentage (%)'}
        )
        fig.update_traces(texttemplate='%{text}%', textposition='inside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        st.plotly_chart(fig, use_container_width=True)
        
        # Graph showing distribution of reservations by time before previous rental
        st.subheader("Time Between Consecutive Rentals by Type")
        
        # Filter out '>12 hours' category
        filtered_df = df
        
        # Group by time category and state
        time_state_dist = filtered_df.groupby(['time_vs_previous_rental_category', 'checkin_type']).size().reset_index()
        time_state_dist.columns = ['Time Category', 'Type', 'Count']
        
        # Calculate total for each time category for percentage
        time_totals = filtered_df.groupby('time_vs_previous_rental_category').size().reset_index()
        time_totals.columns = ['Time Category', 'Total']
        
        # Merge to get the percentage
        time_state_dist = time_state_dist.merge(time_totals, on='Time Category')
        time_state_dist['Percentage'] = time_state_dist['Count'] / time_state_dist['Total'] * 100
        
        # Create the graph
        fig = px.bar(
            time_state_dist,
            x='Time Category',
            y='Percentage',
            color='Type',
            barmode='stack',
            text=time_state_dist['Percentage'].round(1),
            title="Distribution of Time Between Consecutive Rentals by Type",
            labels={'Percentage': 'Percentage (%)'}
        )
        fig.update_traces(texttemplate='%{text}%', textposition='inside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        st.plotly_chart(fig, use_container_width=True)
        
    with tab2:    
        # Late Checkouts Analysis
        st.subheader("Late Checkouts and Cancellations")

        # Get rentals with previous rental information
        rentals_with_prev = df.dropna(subset=['previous_ended_rental_id'])
        total_with_prev = len(rentals_with_prev)

        # Count late checkouts among rentals with previous rental info
        late_checkouts = rentals_with_prev[rentals_with_prev['checkout_status'] == 'Late']
        num_late_checkouts = len(late_checkouts)

        # Count the percentage of info from previous rental
        pct_rental_with_infom_previous_rental = total_with_prev / total_rentals * 100

        # Count canceled rentals after a late checkout
        canceled_after_late = rentals_with_prev[(rentals_with_prev['checkout_status'] == 'Late') & 
                                                (rentals_with_prev['state'] == 'canceled')]
        pct_canceled_after_late = len(canceled_after_late) / num_late_checkouts * 100 if num_late_checkouts > 0 else 0

        # Count the number of rental where the checking was late due to the previous rental
        number_late_checking = df[df['late_checkin'] == "Late"]  # Keep this as a DataFrame, not len()

        # Key figures
        st.markdown("### Key Figures")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rentals with Previous Rental Info", f"{total_with_prev:,}")
        with col2:
            st.metric("Percentage of Rental with Previous Rental", f"{pct_rental_with_infom_previous_rental:.1f}%")
        with col3:
            st.metric("Number of Rental with Late Checkin due to Previous Rental", f"{len(number_late_checking):,}")

        st.markdown("### Rental State depending on Late Checkout")  

        # Step 1: Group by and count rental_id - Fixed observed parameter
        grouped = df.groupby(['late_checkin', 'state'], observed=True)['rental_id'].count().reset_index()
        grouped.rename(columns={'rental_id': 'count'}, inplace=True)

        # Step 2: Group by late_checkin only and calculate the sum - Fixed observed parameter
        sum_grouped = df.groupby(['late_checkin'], observed=True)['rental_id'].count().reset_index()
        sum_grouped.rename(columns={'rental_id': 'sum'}, inplace=True)

        # Correctly merge the dataframes - only using 'late_checkin' as the key
        result = pd.merge(grouped, sum_grouped, on='late_checkin')

        # Calculate percentage
        result['percentage'] = result['count']/result['sum']*100

        # Create the graph showing counts with state color
        fig = px.bar(
            result,
            x='late_checkin',
            y='count',
            color='state',
            barmode='stack',
            text=result['count'],
            title="Distribution of State by Type of Delay",
            labels={'count': 'Number of Rentals', 'late_checkin': 'Checkout Status', 'state': 'Rental State'}
        )
        fig.update_traces(texttemplate='%{text}', textposition='inside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        st.plotly_chart(fig, use_container_width=True)

        # Create a percentage graph
        fig = px.bar(
            result,
            x='late_checkin',
            y='percentage',
            color='state',
            barmode='stack',
            text=result['percentage'].round(1),
            title="Percentage Distribution of State by Type of Delay",
            labels={'percentage': 'Percentage (%)', 'late_checkin': 'Checkout Status', 'state': 'Rental State'}
        )
        fig.update_traces(texttemplate='%{text}%', textposition='inside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        st.plotly_chart(fig, use_container_width=True) 

        st.markdown("### Split of Rentals with Late Checkin by Checkout Delay Category")

        # Filter for late checkouts only
        df_late = df[df['checkout_status'] == 'Late']

        # Group by checkout delay category - Fixed observed parameter
        checkout_delay_counts = df_late.groupby('checkout_delay_category', observed=True)['rental_id'].count().reset_index()
        checkout_delay_counts.columns = ['Checkout Delay Category', 'Count']

        # Calculate total and percentages
        total = checkout_delay_counts['Count'].sum()
        checkout_delay_counts['Percentage'] = checkout_delay_counts['Count'] / total * 100

        # Sort the data to ensure consistent display order (assuming delay categories have numeric prefixes)
        checkout_delay_counts = checkout_delay_counts.sort_values('Checkout Delay Category')

        # Create the count graph with improved styling
        fig1 = px.bar(
            checkout_delay_counts,
            x='Checkout Delay Category',
            y='Count',
            text='Count',
            title="Number of Late Rentals by Checkout Delay Category",
            labels={
                'Checkout Delay Category': 'Checkout Delay Category',
                'Count': 'Number of Rentals'
            },
            color='Count',
            color_continuous_scale='Blues'
        )
        fig1.update_traces(texttemplate='%{text}', textposition='inside')
        fig1.update_layout(
            uniformtext_minsize=8, 
            uniformtext_mode='hide',
            xaxis_title="Checkout Delay Category",
            yaxis_title="Number of Rentals",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig1, use_container_width=True)

        # Create the percentage graph
        fig2 = px.bar(
            checkout_delay_counts,
            x='Checkout Delay Category',
            y='Percentage',
            text=checkout_delay_counts['Percentage'].round(1),
            title="Percentage of Late Rentals by Checkout Delay Category",
            labels={
                'Checkout Delay Category': 'Checkout Delay Category',
                'Percentage': 'Percentage (%)'
            },
            color='Percentage',
            color_continuous_scale='Blues'
        )
        fig2.update_traces(texttemplate='%{text}%', textposition='inside')
        fig2.update_layout(
            uniformtext_minsize=8, 
            uniformtext_mode='hide',
            xaxis_title="Checkout Delay Category",
            yaxis_title="Percentage of Rentals (%)",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig2, use_container_width=True)


    # Tab 3: Threshold Analysis
    with tab3:
        st.header("Threshold Analysis")
        
        # Threshold selection
        threshold_options = [15, 30, 60, 90, 120, 180, 240, 300, 360]
        threshold = st.select_slider(
            "Select minimum delay threshold (minutes)",
            options=threshold_options,
            value=60
        )
        
        st.markdown(f"### Impact of {threshold}-minute Minimum Delay")
        
        # Create a range of thresholds to analyze
        thresholds = list(range(0, 361, 30))
        if threshold not in thresholds:
            thresholds.append(threshold)
            thresholds.sort()
        
        # Calculate affected rentals for each threshold
        threshold_impact = []
        for t in thresholds:
            all_affected = len(df[df['time_delta_with_previous_rental_in_minutes'] < t])
            connect_affected = len(df[(df['checkin_type'] == 'connect') & 
                                    (df['time_delta_with_previous_rental_in_minutes'] < t)])
            mobile_affected = len(df[(df['checkin_type'] == 'mobile') & 
                                (df['time_delta_with_previous_rental_in_minutes'] < t)])
            
            threshold_impact.append({
                'threshold': t,
                'all_affected': all_affected,
                'connect_affected': connect_affected,
                'mobile_affected': mobile_affected,
                'all_pct': all_affected / len(df) * 100 if len(df) > 0 else 0,
                'connect_pct': connect_affected / len(df[df['checkin_type'] == 'connect']) * 100 
                            if len(df[df['checkin_type'] == 'connect']) > 0 else 0,
                'mobile_pct': mobile_affected / len(df[df['checkin_type'] == 'mobile']) * 100
                            if len(df[df['checkin_type'] == 'mobile']) > 0 else 0
            })
        
        threshold_df = pd.DataFrame(threshold_impact)
        
        # Plot absolute numbers
        fig = px.line(
            threshold_df,
            x='threshold',
            y=['all_affected', 'connect_affected', 'mobile_affected'],
            labels={
                'threshold': 'Minimum Delay Threshold (minutes)',
                'value': 'Number of Affected Rentals',
                'variable': 'Car Type'
            },
            title="Number of Affected Rentals by Threshold"
        )
        
        # Update legend names
        newnames = {'all_affected': 'All Cars', 'connect_affected': 'Connect Cars', 'mobile_affected': 'Mobile Cars'}
        fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))
        
        fig.update_layout(hovermode="x unified")
        
        # Add vertical line for selected threshold
        fig.add_vline(x=threshold, line_dash="dash", line_color="red")
        fig.add_annotation(x=threshold, y=max(threshold_df['all_affected']), 
                        text=f"Selected: {threshold} min",
                        showarrow=True, arrowhead=1, ax=30, ay=-30)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Plot percentage
        fig = px.line(
            threshold_df,
            x='threshold',
            y=['all_pct', 'connect_pct', 'mobile_pct'],
            labels={
                'threshold': 'Minimum Delay Threshold (minutes)',
                'value': 'Percentage of Affected Rentals (%)',
                'variable': 'Car Type'
            },
            title="Percentage of Affected Rentals by Threshold"
        )
        
        # Update legend names
        newnames = {'all_pct': 'All Cars', 'connect_pct': 'Connect Cars', 'mobile_pct': 'Mobile Cars'}
        fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))
        
        fig.update_layout(hovermode="x unified")
        
        # Add vertical line for selected threshold
        fig.add_vline(x=threshold, line_dash="dash", line_color="red")
        fig.add_annotation(x=threshold, y=max(threshold_df['all_pct']), 
                        text=f"Selected: {threshold} min",
                        showarrow=True, arrowhead=1, ax=30, ay=-30)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display data table for the selected threshold
        st.subheader(f"Impact at Selected Threshold: {threshold} minutes")
        
        selected_row = threshold_df[threshold_df['threshold'] == threshold].iloc[0] if len(threshold_df[threshold_df['threshold'] == threshold]) > 0 else None
        
        if selected_row is not None:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("All Cars Affected", f"{int(selected_row['all_affected']):,}")
            with col2:
                st.metric("Connect Cars Affected", f"{int(selected_row['connect_affected']):,}")
            with col3:
                st.metric("Mobile Cars Affected", f"{int(selected_row['mobile_affected']):,}")
        
        # Display detailed breakdown for the selected threshold
        affected_rentals = df[df['time_delta_with_previous_rental_in_minutes'] < threshold]
        
        if not affected_rentals.empty:
            st.subheader("Breakdown of Affected Rentals")
            
            # By check-in type
            checkin_breakdown = affected_rentals['checkin_type'].value_counts().reset_index()
            checkin_breakdown.columns = ['Check-in Type', 'Count']
            checkin_breakdown['Percentage'] = checkin_breakdown['Count'] / len(affected_rentals) * 100
            
            fig = px.pie(
                checkin_breakdown,
                values='Count',
                names='Check-in Type',
                title=f"Distribution of Affected Rentals by Check-in Type ({threshold} min threshold)",
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # By state
            state_breakdown = affected_rentals['state'].value_counts().reset_index()
            state_breakdown.columns = ['State', 'Count']
            state_breakdown['Percentage'] = state_breakdown['Count'] / len(affected_rentals) * 100
            
            fig = px.bar(
                state_breakdown,
                x='State',
                y='Count',
                color='State',
                text_auto='.0f',
                title=f"State Distribution of Affected Rentals ({threshold} min threshold)"
            )
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)

else:
    st.error("Failed to load data. The app tried loading from the URL (https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx) and local paths without success. Please check your internet connection or upload the file manually.")

# Footer
st.markdown("---")
st.markdown("Getaround Rental Delay Analysis Dashboard - Developed by Louis Le Pogam")