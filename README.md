# 📊 SPC Analysis - Cp & Cpk Calculator

A comprehensive **Statistical Process Control (SPC)** application that calculates Process Capability (Cp) and Process Capability Index (Cpk) from Excel data and provides interactive visualizations for quality control analysis.

## 🌟 Features

### 📈 Statistical Analysis
- **Process Capability (Cp)** - Measures potential process capability
- **Process Capability Index (Cpk)** - Measures actual process capability considering centering
- **Process Performance Index (Ppk)** - Long-term process performance
- **CPU & CPL** - Upper and Lower capability indices
- **Basic Statistics** - Mean, standard deviation, range, quartiles

### 📊 Interactive Visualizations
- **Control Charts** - X-bar charts with control limits and out-of-control point detection
- **Histograms** - Distribution analysis with normal curve overlay
- **Process Distribution** - Capability visualization with specification limits
- **Defect Rate Analysis** - Theoretical vs actual defect rates
- **Yield Calculations** - Process yield metrics

### 🎯 Quality Features
- **Specification Limits** - Support for Upper (USL) and Lower (LSL) specification limits
- **Normality Testing** - Shapiro-Wilk test for data distribution
- **Out-of-Control Detection** - Automatic identification of special causes
- **Capability Interpretation** - Color-coded capability assessment
- **Export Functionality** - Download analysis reports in CSV format

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd <repository-name>
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
streamlit run spc_app.py
```

4. **Open your browser:**
Navigate to `http://localhost:8501` to access the application.

## 📋 Usage Instructions

### 1. Data Preparation
Your Excel/CSV file should contain:
- A column with numerical measurement values
- At least 30 data points for reliable analysis (recommended: 50+ points)
- No missing values in the measurement column
- Proper column headers

**Sample data format:**
| Sample_ID | Measurement | Date       | Operator |
|-----------|-------------|------------|----------|
| 1         | 10.2        | 2024-01-01 | A        |
| 2         | 10.1        | 2024-01-02 | B        |
| 3         | 9.9         | 2024-01-03 | A        |

### 2. Application Workflow

1. **Upload Data**: Use the file uploader in the sidebar to upload your Excel (.xlsx, .xls) or CSV file
2. **Select Column**: Choose the column containing your measurement data
3. **Set Limits**: Enter your Upper Specification Limit (USL) and/or Lower Specification Limit (LSL)
4. **Optional Target**: Enter a target/nominal value if applicable
5. **View Results**: The app automatically calculates and displays:
   - Process capability indices
   - Interactive charts
   - Statistical analysis
   - Quality assessment

### 3. Interpretation Guidelines

#### Capability Index (Cpk) Interpretation:
- **Cpk ≥ 1.67**: 🎯 Excellent capability
- **1.33 ≤ Cpk < 1.67**: ✅ Good capability  
- **1.0 ≤ Cpk < 1.33**: ⚠️ Marginal capability
- **Cpk < 1.0**: ❌ Poor capability

#### Key Formulas:
- **Cp = (USL - LSL) / (6σ)**
- **Cpk = min(CPU, CPL)**
- **CPU = (USL - μ) / (3σ)**
- **CPL = (μ - LSL) / (3σ)**

Where:
- μ = Process mean
- σ = Process standard deviation
- USL = Upper Specification Limit
- LSL = Lower Specification Limit

## 📁 Sample Data

The repository includes several sample datasets for testing:

### Main Dataset (`sample_spc_data.xlsx/csv`)
- 100 measurement points
- Includes outliers and process shifts
- Good for comprehensive testing

### Additional Test Datasets:
1. **`sample_good_capability.xlsx`** - Process with excellent capability
2. **`sample_poor_capability.xlsx`** - Process with poor capability  
3. **`sample_off_center.xlsx`** - Well-controlled but off-center process

You can generate new sample data by running:
```bash
python3 sample_data.py
```

## 🔧 Technical Details

### Dependencies
- **Streamlit** - Web application framework
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **Plotly** - Interactive visualizations
- **SciPy** - Statistical functions
- **Matplotlib & Seaborn** - Additional plotting capabilities
- **OpenPyXL & xlrd** - Excel file support

### File Structure
```
├── spc_app.py              # Main Streamlit application
├── sample_data.py          # Sample data generation script
├── requirements.txt        # Python dependencies
├── README.md              # This documentation
├── sample_spc_data.xlsx   # Main sample dataset
├── sample_spc_data.csv    # Main sample dataset (CSV)
└── sample_*.xlsx/csv      # Additional test datasets
```

### Key Classes and Functions

#### `SPCAnalyzer` Class
- `load_data()` - Load Excel/CSV files
- `calculate_cp()` - Calculate process capability
- `calculate_cpk()` - Calculate capability index
- `calculate_ppk()` - Calculate performance index
- `create_control_chart()` - Generate control charts
- `create_histogram()` - Generate distribution plots

## 📊 Chart Types

### 1. Control Chart
- Plots measurement values over time
- Shows control limits (±3σ)
- Highlights specification limits
- Identifies out-of-control points

### 2. Histogram with Normal Distribution
- Shows data distribution
- Overlays theoretical normal curve
- Displays specification limits
- Includes normality test results

### 3. Process Distribution Analysis
- Compares theoretical vs actual defect rates
- Shows process yield calculations
- Visualizes capability relative to specifications

## 🎯 SPC Best Practices

### Data Collection
- Collect data systematically and consistently
- Ensure measurement system accuracy
- Use rational subgroups when possible
- Maintain adequate sample sizes (n ≥ 30)

### Analysis Guidelines
- Verify data normality before capability analysis
- Consider both short-term (Cp, Cpk) and long-term (Pp, Ppk) capability
- Monitor process stability before capability assessment
- Update capability studies regularly

### Action Thresholds
- **Cpk < 1.0**: Immediate corrective action required
- **1.0 ≤ Cpk < 1.33**: Process improvement needed
- **Cpk ≥ 1.33**: Maintain current process
- **Cpk ≥ 1.67**: Excellent process, consider tightening specifications

## 🛠️ Troubleshooting

### Common Issues:

1. **"No module named 'streamlit'" Error**
   ```bash
   pip install -r requirements.txt
   ```

2. **File Upload Issues**
   - Ensure file format is .xlsx, .xls, or .csv
   - Check for proper column headers
   - Verify numerical data in measurement column

3. **Capability Calculation Errors**
   - Enter at least one specification limit (USL or LSL)
   - Ensure measurement data is numerical
   - Check for sufficient data points (minimum 5, recommended 30+)

4. **Visualization Problems**
   - Refresh the browser page
   - Check data for extreme outliers
   - Ensure proper data format

## 📈 Future Enhancements

- [ ] Support for subgroup analysis (X-bar & R charts)
- [ ] Additional control chart types (p, np, c, u charts)
- [ ] Process capability trend analysis
- [ ] Multi-variate capability analysis
- [ ] Integration with quality management systems
- [ ] Advanced statistical tests (Anderson-Darling, etc.)

## 📧 Contact

For questions, suggestions, or support, please contact the development team or create an issue in the repository.

## 📄 License

This project is open source and available under the MIT License.

---

**Happy Quality Analyzing! 📊✨**
