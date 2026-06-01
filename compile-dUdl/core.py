import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

# Constant conversion factor (1 kJ/mol = 120 K)
kJ_mol_Kelvin = 120.0

def integrate_spline(x, y, a=0.0, b=1.0):
    """Fits a cubic spline to the data and integrates it between limits a and b."""
    spline = UnivariateSpline(x, y, s=0)
    integral_value = spline.integral(a, b) 
    return integral_value, spline(x)

def compile_data(root_folder="./"):
    """
    Traverses subdirectories to parse 'dU_dlambda.out' files,
    converting raw Kelvin data into kJ/mol.
    """
    dUdl_list = []
    
    for item in os.listdir(root_folder):
        item_path = os.path.join(root_folder, item)
        if os.path.isdir(item_path):
            target_file = os.path.join(item_path, "OUTPUT", "CFC", "dU_dlambda.out")
            
            if os.path.exists(target_file):
                try:
                    a = np.loadtxt(target_file, comments='#')
                    # Handle single-row files gracefully by making them 2D
                    if a.ndim == 1:
                        a = np.atleast_2d(a)
                        
                    for i in range(len(a[:, 0])):
                        if not np.isnan(a[i, 1]):
                            # Convert Kelvin values to kJ/mol
                            dUdl_list.append([
                                a[i, 0], 
                                a[i, 1] / kJ_mol_Kelvin, 
                                a[i, 2] / kJ_mol_Kelvin
                            ])
                except Exception as e:
                    print(f"Warning: Could not parse file {target_file}. Error: {e}")
                    
    if not dUdl_list:
        raise ValueError("No valid 'dU_dlambda.out' data was found in the subfolders.")

    dUdl_list_sorted = sorted(dUdl_list)
    return np.array(dUdl_list_sorted)

def plot_results(data_array, spline_fit, output_basename='dUdl_with_CubicFit'):
    """Generates and saves the analytical dU/dlambda cubic fit plot."""
    fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(6, 4.2))
    
    axs.plot(data_array[:, 0], data_array[:, 1], color='blue', linestyle='solid', 
             linewidth=2, marker='s', markersize=4, label=r'NO$_{3}^{-}$ + H$_{3}$O$^{+}$')
    axs.plot(data_array[:, 0], spline_fit, linestyle='solid', color='darkorange', 
             linewidth=2, label='Cubic fit')
    
    axs.grid(True, which='both')
    axs.grid(which='minor', alpha=0.1)
    axs.grid(which='major', alpha=0.5)
    
    axs.set_ylabel(r'$\langle \frac{\partial U}{\partial \lambda} \rangle$ / [kJ/mol]', fontsize=14)
    axs.set_xlabel(r'$\lambda$', fontsize=14)
    axs.legend(loc='lower left', shadow=False, fontsize=10, frameon=False)
    
    fig.tight_layout()
    fig.savefig(f'{output_basename}.pdf')
    fig.savefig(f'{output_basename}.svg')
    plt.close(fig)