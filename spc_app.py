import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from scipy import stats
import io

# Set page configuration
st.set_page_config(
    page_title="SPC Analysis - Cp & Cpk Calculator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class SPCAnalyzer:
    """Statistical Process Control analyzer for Cp and Cpk calculations"""
    
    def __init__(self):
        self.data = None
        self.measurement_column = None
        self.usl = None  # Upper Specification Limit
        self.lsl = None  # Lower Specification Limit
        self.target = None  # Target value
    
    def load_data(self, uploaded_file):
        """Load data from uploaded Excel file"""
        try:
            if uploaded_file.name.endswith('.csv'):
                self.data = pd.read_csv(uploaded_file)
            else:
                self.data = pd.read_excel(uploaded_file)
            return True
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            return False
    
    def calculate_basic_stats(self, measurements):
        """Calculate basic statistical measures"""
        stats_dict = {
            'count': len(measurements),
            'mean': np.mean(measurements),
            'std': np.std(measurements, ddof=1),  # Sample standard deviation
            'min': np.min(measurements),
            'max': np.max(measurements),
            'median': np.median(measurements),
            'q25': np.percentile(measurements, 25),
            'q75': np.percentile(measurements, 75),
            'range': np.max(measurements) - np.min(measurements)
        }
        return stats_dict
    
    def calculate_cp(self, measurements, usl, lsl):
        """Calculate Process Capability (Cp)"""
        if usl is None or lsl is None:
            return None
        
        std = np.std(measurements, ddof=1)
        if std == 0:
            return float('inf')
        
        cp = (usl - lsl) / (6 * std)
        return cp
    
    def calculate_cpk(self, measurements, usl, lsl, target=None):
        """Calculate Process Capability Index (Cpk)"""
        mean = np.mean(measurements)
        std = np.std(measurements, ddof=1)
        
        if std == 0:
            return float('inf'), float('inf'), float('inf')
        
        # Calculate CPU and CPL
        cpu = (usl - mean) / (3 * std) if usl is not None else None
        cpl = (mean - lsl) / (3 * std) if lsl is not None else None
        
        # Cpk is the minimum of CPU and CPL
        if cpu is not None and cpl is not None:
            cpk = min(cpu, cpl)
        elif cpu is not None:
            cpk = cpu
        elif cpl is not None:
            cpk = cpl
        else:
            cpk = None
        
        return cpk, cpu, cpl
    
    def calculate_ppk(self, measurements, usl, lsl):
        """Calculate Process Performance Index (Ppk)"""
        mean = np.mean(measurements)
        std = np.std(measurements, ddof=0)  # Population standard deviation for Ppk
        
        if std == 0:
            return float('inf'), float('inf'), float('inf')
        
        ppu = (usl - mean) / (3 * std) if usl is not None else None
        ppl = (mean - lsl) / (3 * std) if lsl is not None else None
        
        if ppu is not None and ppl is not None:
            ppk = min(ppu, ppl)
        elif ppu is not None:
            ppk = ppu
        elif ppl is not None:
            ppk = ppl
        else:
            ppk = None
        
        return ppk, ppu, ppl
    
    def create_control_chart(self, measurements, title="Control Chart"):
        """Create an X-bar control chart"""
        fig = go.Figure()
        
        mean = np.mean(measurements)
        std = np.std(measurements, ddof=1)
        
        # Control limits (assuming individual measurements)
        ucl = mean + 3 * std
        lcl = mean - 3 * std
        
        # Add measurement points
        fig.add_trace(go.Scatter(
            x=list(range(1, len(measurements) + 1)),
            y=measurements,
            mode='lines+markers',
            name='Measurements',
            line=dict(color='blue'),
            marker=dict(size=6)
        ))
        
        # Add center line
        fig.add_hline(y=mean, line_dash="dash", line_color="green", 
                     annotation_text=f"Mean = {mean:.3f}")
        
        # Add control limits
        fig.add_hline(y=ucl, line_dash="dash", line_color="red", 
                     annotation_text=f"UCL = {ucl:.3f}")
        fig.add_hline(y=lcl, line_dash="dash", line_color="red", 
                     annotation_text=f"LCL = {lcl:.3f}")
        
        # Add specification limits if available
        if self.usl is not None:
            fig.add_hline(y=self.usl, line_dash="dot", line_color="orange", 
                         annotation_text=f"USL = {self.usl:.3f}")
        if self.lsl is not None:
            fig.add_hline(y=self.lsl, line_dash="dot", line_color="orange", 
                         annotation_text=f"LSL = {self.lsl:.3f}")
        
        fig.update_layout(
            title=title,
            xaxis_title="Sample Number",
            yaxis_title="Measurement Value",
            showlegend=True,
            height=500
        )
        
        return fig
    
    def create_histogram(self, measurements, title="Histogram with Normal Distribution"):
        """Create histogram with normal distribution overlay"""
        fig = go.Figure()
        
        # Histogram
        fig.add_trace(go.Histogram(
            x=measurements,
            nbinsx=30,
            name='Data',
            opacity=0.7,
            yaxis='y',
            histnorm='probability density'
        ))
        
        # Normal distribution overlay
        mean = np.mean(measurements)
        std = np.std(measurements, ddof=1)
        x_norm = np.linspace(min(measurements), max(measurements), 100)
        y_norm = stats.norm.pdf(x_norm, mean, std)
        
        fig.add_trace(go.Scatter(
            x=x_norm,
            y=y_norm,
            mode='lines',
            name='Normal Distribution',
            line=dict(color='red', width=2)
        ))
        
        # Add specification limits
        if self.usl is not None:
            fig.add_vline(x=self.usl, line_dash="dash", line_color="orange", 
                         annotation_text=f"USL = {self.usl:.3f}")
        if self.lsl is not None:
            fig.add_vline(x=self.lsl, line_dash="dash", line_color="orange", 
                         annotation_text=f"LSL = {self.lsl:.3f}")
        
        # Add mean line
        fig.add_vline(x=mean, line_dash="dot", line_color="green", 
                     annotation_text=f"Mean = {mean:.3f}")
        
        fig.update_layout(
            title=title,
            xaxis_title="Measurement Value",
            yaxis_title="Density",
            showlegend=True,
            height=500
        )
        
        return fig
    
    def create_capability_plot(self, measurements):
        """Create process capability visualization"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Process Distribution', 'Capability Indices', 
                          'Process Performance', 'Control Chart'),
            specs=[[{"type": "xy"}, {"type": "indicator"}],
                   [{"type": "xy"}, {"type": "xy"}]]
        )
        
        mean = np.mean(measurements)
        std = np.std(measurements, ddof=1)
        
        # Process distribution
        x_range = np.linspace(min(measurements) - 2*std, max(measurements) + 2*std, 100)
        y_norm = stats.norm.pdf(x_range, mean, std)
        
        fig.add_trace(go.Scatter(x=x_range, y=y_norm, mode='lines', name='Process'),
                     row=1, col=1)
        
        if self.usl is not None and self.lsl is not None:
            # Shade areas outside specification limits
            x_fill_left = x_range[x_range <= self.lsl]
            y_fill_left = stats.norm.pdf(x_fill_left, mean, std)
            
            x_fill_right = x_range[x_range >= self.usl]
            y_fill_right = stats.norm.pdf(x_fill_right, mean, std)
            
            fig.add_trace(go.Scatter(x=x_fill_left, y=y_fill_left, 
                                   fill='tonexty', fillcolor='rgba(255,0,0,0.3)',
                                   mode='lines', name='Out of Spec (Lower)'),
                         row=1, col=1)
            fig.add_trace(go.Scatter(x=x_fill_right, y=y_fill_right,
                                   fill='tonexty', fillcolor='rgba(255,0,0,0.3)',
                                   mode='lines', name='Out of Spec (Upper)'),
                         row=1, col=1)
        
        # Add specification limits
        if self.usl is not None:
            fig.add_vline(x=self.usl, line_dash="dash", line_color="red", row=1, col=1)
        if self.lsl is not None:
            fig.add_vline(x=self.lsl, line_dash="dash", line_color="red", row=1, col=1)
        
        fig.update_layout(height=800, showlegend=True)
        
        return fig

# Main Streamlit App
def main():
    # Header
    st.markdown('<div class="main-header">📊 SPC Analysis - Cp & Cpk Calculator</div>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    This application calculates Process Capability (Cp) and Process Capability Index (Cpk) 
    from your Excel data and provides comprehensive SPC visualizations.
    """)
    
    # Initialize session state
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = SPCAnalyzer()
    
    analyzer = st.session_state.analyzer
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("📁 Data Input")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload your Excel/CSV file",
            type=['xlsx', 'xls', 'csv'],
            help="Upload an Excel or CSV file containing your measurement data"
        )
        
        if uploaded_file is not None:
            if analyzer.load_data(uploaded_file):
                st.success("File loaded successfully!")
                
                # Column selection
                st.header("📊 Data Configuration")
                
                measurement_column = st.selectbox(
                    "Select measurement column",
                    analyzer.data.columns,
                    help="Choose the column containing your measurement values"
                )
                analyzer.measurement_column = measurement_column
                
                # Specification limits
                st.header("📏 Specification Limits")
                
                col1, col2 = st.columns(2)
                with col1:
                    usl = st.number_input(
                        "Upper Spec Limit (USL)",
                        value=None,
                        placeholder="Enter USL",
                        help="Upper specification limit for your process"
                    )
                    analyzer.usl = usl
                
                with col2:
                    lsl = st.number_input(
                        "Lower Spec Limit (LSL)",
                        value=None,
                        placeholder="Enter LSL",
                        help="Lower specification limit for your process"
                    )
                    analyzer.lsl = lsl
                
                # Target value (optional)
                target = st.number_input(
                    "Target Value (optional)",
                    value=None,
                    placeholder="Enter target",
                    help="Nominal or target value for your process"
                )
                analyzer.target = target
    
    # Main content area
    if uploaded_file is not None and analyzer.data is not None and analyzer.measurement_column:
        
        # Get measurement data
        measurements = analyzer.data[analyzer.measurement_column].dropna()
        
        if len(measurements) == 0:
            st.error("No valid measurement data found in the selected column.")
            return
        
        # Data preview
        st.header("📋 Data Preview")
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.dataframe(analyzer.data.head(10), use_container_width=True)
        
        with col2:
            st.metric("Total Records", len(analyzer.data))
            st.metric("Valid Measurements", len(measurements))
        
        with col3:
            if analyzer.data[analyzer.measurement_column].isnull().sum() > 0:
                st.warning(f"{analyzer.data[analyzer.measurement_column].isnull().sum()} missing values found")
        
        # Basic statistics
        st.header("📊 Basic Statistics")
        stats_dict = analyzer.calculate_basic_stats(measurements)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Mean", f"{stats_dict['mean']:.4f}")
            st.metric("Std Dev", f"{stats_dict['std']:.4f}")
        with col2:
            st.metric("Minimum", f"{stats_dict['min']:.4f}")
            st.metric("Maximum", f"{stats_dict['max']:.4f}")
        with col3:
            st.metric("Median", f"{stats_dict['median']:.4f}")
            st.metric("Range", f"{stats_dict['range']:.4f}")
        with col4:
            st.metric("Q1 (25%)", f"{stats_dict['q25']:.4f}")
            st.metric("Q3 (75%)", f"{stats_dict['q75']:.4f}")
        
        # Process Capability Analysis
        st.header("🎯 Process Capability Analysis")
        
        if analyzer.usl is not None or analyzer.lsl is not None:
            
            # Calculate Cp and Cpk
            cp = analyzer.calculate_cp(measurements, analyzer.usl, analyzer.lsl)
            cpk, cpu, cpl = analyzer.calculate_cpk(measurements, analyzer.usl, analyzer.lsl)
            ppk, ppu, ppl = analyzer.calculate_ppk(measurements, analyzer.usl, analyzer.lsl)
            
            # Display capability indices
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if cp is not None:
                    cp_color = "green" if cp >= 1.33 else "orange" if cp >= 1.0 else "red"
                    st.markdown(f'<div class="metric-card"><h3 style="color:{cp_color}">Cp</h3><h2>{cp:.3f}</h2></div>', 
                               unsafe_allow_html=True)
                else:
                    st.info("Cp: Need both USL and LSL")
            
            with col2:
                if cpk is not None:
                    cpk_color = "green" if cpk >= 1.33 else "orange" if cpk >= 1.0 else "red"
                    st.markdown(f'<div class="metric-card"><h3 style="color:{cpk_color}">Cpk</h3><h2>{cpk:.3f}</h2></div>', 
                               unsafe_allow_html=True)
                else:
                    st.info("Cpk: Need USL or LSL")
            
            with col3:
                if cpu is not None:
                    st.markdown(f'<div class="metric-card"><h3>CPU</h3><h2>{cpu:.3f}</h2></div>', 
                               unsafe_allow_html=True)
                else:
                    st.info("CPU: Need USL")
            
            with col4:
                if cpl is not None:
                    st.markdown(f'<div class="metric-card"><h3>CPL</h3><h2>{cpl:.3f}</h2></div>', 
                               unsafe_allow_html=True)
                else:
                    st.info("CPL: Need LSL")
            
            # Process Performance Indices
            st.subheader("Process Performance Indices")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if ppk is not None:
                    st.metric("Ppk", f"{ppk:.3f}")
            with col2:
                if ppu is not None:
                    st.metric("PPU", f"{ppu:.3f}")
            with col3:
                if ppl is not None:
                    st.metric("PPL", f"{ppl:.3f}")
            
            # Capability interpretation
            st.subheader("📋 Capability Interpretation")
            
            if cpk is not None:
                if cpk >= 1.67:
                    st.success("🎯 Excellent capability (Cpk ≥ 1.67)")
                elif cpk >= 1.33:
                    st.success("✅ Good capability (1.33 ≤ Cpk < 1.67)")
                elif cpk >= 1.0:
                    st.warning("⚠️ Marginal capability (1.0 ≤ Cpk < 1.33)")
                else:
                    st.error("❌ Poor capability (Cpk < 1.0)")
            
        else:
            st.warning("⚠️ Please enter at least one specification limit (USL or LSL) to calculate capability indices.")
        
        # Visualizations
        st.header("📈 SPC Charts")
        
        # Tabs for different charts
        tab1, tab2, tab3 = st.tabs(["Control Chart", "Histogram", "Process Distribution"])
        
        with tab1:
            st.subheader("Control Chart")
            control_chart = analyzer.create_control_chart(measurements)
            st.plotly_chart(control_chart, use_container_width=True)
            
            # Out-of-control points analysis
            mean = np.mean(measurements)
            std = np.std(measurements, ddof=1)
            ucl = mean + 3 * std
            lcl = mean - 3 * std
            
            out_of_control = []
            for i, value in enumerate(measurements):
                if value > ucl or value < lcl:
                    out_of_control.append((i+1, value))
            
            if out_of_control:
                st.warning(f"⚠️ {len(out_of_control)} out-of-control points detected:")
                for point, value in out_of_control:
                    st.write(f"• Point {point}: {value:.4f}")
            else:
                st.success("✅ All points are within control limits")
        
        with tab2:
            st.subheader("Histogram with Normal Distribution")
            histogram = analyzer.create_histogram(measurements)
            st.plotly_chart(histogram, use_container_width=True)
            
            # Normality test
            shapiro_stat, shapiro_p = stats.shapiro(measurements)
            st.write(f"**Shapiro-Wilk Normality Test:**")
            st.write(f"Statistic: {shapiro_stat:.4f}, p-value: {shapiro_p:.4f}")
            
            if shapiro_p > 0.05:
                st.success("✅ Data appears to be normally distributed (p > 0.05)")
            else:
                st.warning("⚠️ Data may not be normally distributed (p ≤ 0.05)")
        
        with tab3:
            st.subheader("Process Distribution Analysis")
            if analyzer.usl is not None and analyzer.lsl is not None:
                # Calculate defect rates
                mean = np.mean(measurements)
                std = np.std(measurements, ddof=1)
                
                # Theoretical defect rates based on normal distribution
                lower_defects = stats.norm.cdf(analyzer.lsl, mean, std) * 100
                upper_defects = (1 - stats.norm.cdf(analyzer.usl, mean, std)) * 100
                total_defects = lower_defects + upper_defects
                
                # Actual defect rates from data
                actual_lower = (measurements < analyzer.lsl).sum() / len(measurements) * 100
                actual_upper = (measurements > analyzer.usl).sum() / len(measurements) * 100
                actual_total = actual_lower + actual_upper
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Theoretical Defect Rate", f"{total_defects:.2f}%")
                    st.write(f"• Lower: {lower_defects:.2f}%")
                    st.write(f"• Upper: {upper_defects:.2f}%")
                
                with col2:
                    st.metric("Actual Defect Rate", f"{actual_total:.2f}%")
                    st.write(f"• Lower: {actual_lower:.2f}%")
                    st.write(f"• Upper: {actual_upper:.2f}%")
                
                # Yield calculation
                theoretical_yield = 100 - total_defects
                actual_yield = 100 - actual_total
                
                st.write("**Process Yield:**")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Theoretical Yield", f"{theoretical_yield:.2f}%")
                with col2:
                    st.metric("Actual Yield", f"{actual_yield:.2f}%")
            
            else:
                st.info("Enter both USL and LSL to see defect rate analysis")
        
        # Export results
        st.header("💾 Export Results")
        
        if st.button("Generate Report"):
            # Create summary report
            report_data = {
                'Metric': ['Count', 'Mean', 'Std Dev', 'Min', 'Max', 'Range'],
                'Value': [len(measurements), stats_dict['mean'], stats_dict['std'], 
                         stats_dict['min'], stats_dict['max'], stats_dict['range']]
            }
            
            if cp is not None:
                report_data['Metric'].append('Cp')
                report_data['Value'].append(cp)
            
            if cpk is not None:
                report_data['Metric'].append('Cpk')
                report_data['Value'].append(cpk)
            
            report_df = pd.DataFrame(report_data)
            
            # Convert to CSV for download
            csv = report_df.to_csv(index=False)
            st.download_button(
                label="📁 Download Summary Report (CSV)",
                data=csv,
                file_name=f"spc_analysis_report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    else:
        # Welcome message
        st.info("👆 Please upload an Excel or CSV file to begin the SPC analysis.")
        
        # Sample data format
        st.subheader("📋 Expected Data Format")
        st.write("Your Excel/CSV file should contain:")
        st.write("• A column with measurement values")
        st.write("• Numeric data (no text in measurement column)")
        st.write("• At least 30 data points for reliable analysis")
        
        sample_data = pd.DataFrame({
            'Sample_ID': range(1, 11),
            'Measurement': [10.2, 10.1, 9.9, 10.3, 10.0, 9.8, 10.4, 10.1, 9.9, 10.2],
            'Date': pd.date_range('2024-01-01', periods=10)
        })
        
        st.write("**Sample data format:**")
        st.dataframe(sample_data)

if __name__ == "__main__":
    main()