import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

def load_tga_dsc_data(file_path):
    return pd.read_csv(file_path, skiprows=9)

def downsample_data(data, factor=10):
    return data.iloc[::factor]

def plot_dsc_data_with_peaks_troughs(ax, data, label, color, show_lines):
    ax.plot(data["°C"], data["W/g"], label=label, color=color)
    
    if show_lines:
        # Finding peaks and troughs
        peaks, _ = find_peaks(data["W/g"])
        troughs, _ = find_peaks(-data["W/g"])
        
        # Marking peaks with vertical lines
        for peak in peaks:
            ax.axvline(x=data.iloc[peak]["°C"], color=color, linestyle='--', alpha=0.7)
        
        # Marking troughs with vertical lines
        for trough in troughs:
            ax.axvline(x=data.iloc[trough]["°C"], color=color, linestyle='--', alpha=0.7)
    
    
    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Heat Flow (W/g)")
    ax.legend()

def plot_tga_data_with_inflections(ax, data, label, color, show_lines, mass_percent=None):
    ax.plot(data["°C"], data["%"], label=label, color=color)
    
    if show_lines:
        # Calculating the derivative of weight percentage with respect to temperature
        derivative = np.gradient(data["%"], data["°C"])
        
        # Finding inflection points (where the derivative changes sign)
        inflections = np.where(np.diff(np.sign(derivative)))[0]
        
        # Marking inflection points with vertical lines
        for inflection in inflections:
            ax.axvline(x=data.iloc[inflection]["°C"], color=color, linestyle='--', alpha=0.7)
    
    if mass_percent is not None:
        ax.axhline(y=mass_percent, color=color, linestyle='--', alpha=0.7)
    
    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Weight (%)")
    ax.legend()

def plot_tga_dsc_data(directory, show_dsc_lines=False, show_tga_lines=False,
                      m_laser_paper_percent=None, m_oven_paper_percent=None):
    files = os.listdir(directory)
    colors = {
        "uncoated": "#b0c4b1",
        "coated-laser": "#3a5a40",
        "coated-oven": "#f77f00"
    }

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    for file in files:
        if file.endswith(".csv"):
            label = file.replace(".csv", "").replace("-", " ").capitalize()
            color = colors.get(file.replace(".csv", ""), "black")
            data = load_tga_dsc_data(os.path.join(directory, file))
            data_downsampled = downsample_data(data)
            
            plot_dsc_data_with_peaks_troughs(ax1, data_downsampled, label, color, show_dsc_lines)
            if "laser" in file:
                plot_tga_data_with_inflections(ax2, data_downsampled, label, color, show_tga_lines, m_laser_paper_percent)
            elif "oven" in file:
                plot_tga_data_with_inflections(ax2, data_downsampled, label, color, show_tga_lines, m_oven_paper_percent)
            else:
                plot_tga_data_with_inflections(ax2, data_downsampled, label, color, show_tga_lines)

    ax1.set_title("DSC Data")
    ax2.set_title("TGA Data")
    plt.tight_layout()
    plt.show()

# measured mass in grams
m_laser_paper = 0.0247
m_laser_total = 0.0515
m_laser_paper_percent = m_laser_paper / m_laser_total * 100

m_oven_paper = 0.0279
m_oven_total = 0.0603
m_oven_paper_percent = m_oven_paper / m_oven_total * 100

# Specify the directory containing the CSV files
directory = r"C:\Users\antho\Desktop\Desktop_tmp\sandra_MCL_data"
plot_tga_dsc_data(directory, m_laser_paper_percent=m_laser_paper_percent, m_oven_paper_percent=m_oven_paper_percent)