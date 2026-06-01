import sys
from .core import compile_data, integrate_spline, plot_results

__version__ = "0.1.0"

def main():
    """
    The main entry point execution script mimicking the original behavior.
    """
    print("Processing directories and compiling data...")
    try:
        data = compile_data()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
        
    # Save the text compilation output
    import numpy as np
    np.savetxt("Compiled_dU_dl.txt", data, fmt=['%1.3f', ' %.4e', ' %.4e'], 
               header='#Lambda dU/d\\lambda[kJ/mol] Std.Err_dU/d\\lambda [kJ/mol]')
    
    # Calculate integration and fit
    integral_val, spline_fit = integrate_spline(data[:, 0], data[:, 1], 0.0, 1.0)
    print(f"Integrated answer is {integral_val:.3f} kJ/mol")
    
    # Generate charts
    plot_results(data, spline_fit)
    print("Plot generated successfully.")

if __name__ == "__main__":
    main()