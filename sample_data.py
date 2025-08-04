import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_spc_data():
    """Generate sample SPC data for testing the application"""
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Parameters for the process
    target_value = 10.0
    process_std = 0.15
    sample_size = 100
    
    # Generate measurement data with some variation
    measurements = np.random.normal(target_value, process_std, sample_size)
    
    # Add some trend and special causes
    # Add slight upward trend
    trend = np.linspace(0, 0.1, sample_size)
    measurements += trend
    
    # Add some out-of-control points
    measurements[25] += 0.8  # Outlier
    measurements[60] -= 0.7  # Outlier
    measurements[80:85] += 0.3  # Shift
    
    # Create sample data
    sample_data = {
        'Sample_ID': range(1, sample_size + 1),
        'Measurement': measurements,
        'Date': pd.date_range(start='2024-01-01', periods=sample_size, freq='D'),
        'Operator': np.random.choice(['A', 'B', 'C'], sample_size),
        'Shift': np.random.choice(['Day', 'Night'], sample_size),
        'Machine': np.random.choice(['M1', 'M2', 'M3'], sample_size)
    }
    
    df = pd.DataFrame(sample_data)
    
    # Round measurements to 4 decimal places
    df['Measurement'] = df['Measurement'].round(4)
    
    return df

def generate_multiple_datasets():
    """Generate multiple sample datasets with different characteristics"""
    
    datasets = {}
    
    # Dataset 1: Good process capability
    np.random.seed(42)
    good_process = np.random.normal(10.0, 0.05, 50)
    datasets['good_capability'] = pd.DataFrame({
        'Sample_ID': range(1, 51),
        'Measurement': good_process.round(4),
        'Date': pd.date_range('2024-01-01', periods=50, freq='D')
    })
    
    # Dataset 2: Poor process capability
    np.random.seed(123)
    poor_process = np.random.normal(10.0, 0.25, 50)
    datasets['poor_capability'] = pd.DataFrame({
        'Sample_ID': range(1, 51),
        'Measurement': poor_process.round(4),
        'Date': pd.date_range('2024-01-01', periods=50, freq='D')
    })
    
    # Dataset 3: Off-center process
    np.random.seed(456)
    off_center = np.random.normal(10.3, 0.1, 50)
    datasets['off_center'] = pd.DataFrame({
        'Sample_ID': range(1, 51),
        'Measurement': off_center.round(4),
        'Date': pd.date_range('2024-01-01', periods=50, freq='D')
    })
    
    return datasets

if __name__ == "__main__":
    # Generate main sample data
    main_data = generate_sample_spc_data()
    main_data.to_excel('sample_spc_data.xlsx', index=False)
    main_data.to_csv('sample_spc_data.csv', index=False)
    
    # Generate additional datasets
    datasets = generate_multiple_datasets()
    
    for name, data in datasets.items():
        data.to_excel(f'sample_{name}.xlsx', index=False)
        data.to_csv(f'sample_{name}.csv', index=False)
    
    print("Sample data files generated:")
    print("- sample_spc_data.xlsx (main dataset)")
    print("- sample_spc_data.csv (main dataset)")
    for name in datasets.keys():
        print(f"- sample_{name}.xlsx")
        print(f"- sample_{name}.csv")
    
    # Display summary statistics
    print("\nMain dataset summary:")
    print(f"Sample size: {len(main_data)}")
    print(f"Mean: {main_data['Measurement'].mean():.4f}")
    print(f"Std Dev: {main_data['Measurement'].std():.4f}")
    print(f"Min: {main_data['Measurement'].min():.4f}")
    print(f"Max: {main_data['Measurement'].max():.4f}")
    print(f"Range: {main_data['Measurement'].max() - main_data['Measurement'].min():.4f}")