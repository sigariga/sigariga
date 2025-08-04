# 🎯 SPC Analysis Application - Demo Guide

## Quick Demo Steps

### 1. Start the Application
```bash
# Option 1: Use the startup script
./run_app.sh

# Option 2: Direct Streamlit command
streamlit run spc_app.py
```

### 2. Load Sample Data
Upload one of the provided sample files:
- `sample_spc_data.xlsx` - Main dataset with 100 points
- `sample_good_capability.xlsx` - Excellent process capability
- `sample_poor_capability.xlsx` - Poor process capability
- `sample_off_center.xlsx` - Off-center process

### 3. Configure Analysis
1. Select "Measurement" column
2. Set specification limits:
   - **USL**: 10.5 (Upper Specification Limit)
   - **LSL**: 9.5 (Lower Specification Limit)
   - **Target**: 10.0 (optional)

### 4. Review Results

#### Expected Results for Main Dataset:
- **Cp**: ~0.85 (Marginal capability)
- **Cpk**: ~0.76 (Poor capability)
- **Mean**: ~10.05
- **Std Dev**: ~0.19

#### Charts to Explore:
1. **Control Chart**: Shows out-of-control points
2. **Histogram**: Distribution with normal overlay
3. **Process Distribution**: Defect rate analysis

### 5. Key Features to Test

#### Statistical Analysis:
- ✅ Automatic Cp/Cpk calculation
- ✅ Process performance indices (Ppk)
- ✅ Basic statistics display
- ✅ Normality testing

#### Interactive Charts:
- ✅ Zoom and pan on all charts
- ✅ Hover for detailed values
- ✅ Export charts as images

#### Quality Assessment:
- ✅ Color-coded capability indicators
- ✅ Out-of-control point detection
- ✅ Defect rate calculations
- ✅ Process yield metrics

#### Data Export:
- ✅ Download summary report
- ✅ CSV format with key metrics

## 📊 Sample Analysis Results

### Good Capability Process:
- **Cpk**: 2.0+ (Excellent)
- **Color**: Green indicators
- **Interpretation**: Process meets specifications

### Poor Capability Process:
- **Cpk**: 0.5-0.7 (Poor)
- **Color**: Red indicators
- **Interpretation**: Process needs improvement

### Off-Center Process:
- **Cp**: Good (>1.0)
- **Cpk**: Poor (<1.0)
- **Interpretation**: Process capable but needs centering

## 🎯 Demo Scenarios

### Scenario 1: Quality Manager Review
1. Upload main dataset
2. Set tight specifications (USL: 10.3, LSL: 9.7)
3. Observe poor capability
4. Export report for management

### Scenario 2: Process Improvement
1. Compare good vs poor capability datasets
2. Analyze histogram differences
3. Review defect rate impacts
4. Identify improvement opportunities

### Scenario 3: Process Monitoring
1. Load dataset with out-of-control points
2. Review control chart for special causes
3. Identify points requiring investigation
4. Plan corrective actions

## 📈 Expected Performance

- **Load Time**: < 2 seconds for 100 data points
- **Chart Rendering**: Near-instantaneous
- **File Support**: Excel (.xlsx, .xls) and CSV
- **Data Size**: Tested up to 1000+ points

## 💡 Tips for Best Demo Experience

1. **Start with good capability data** to show ideal results
2. **Compare different datasets** to show capability differences
3. **Interact with charts** to demonstrate responsiveness
4. **Export reports** to show practical utility
5. **Test edge cases** like missing specification limits

---

**Ready to explore SPC analysis? Start with `./run_app.sh` and dive in! 🚀**