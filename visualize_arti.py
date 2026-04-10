#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

COLS = ["CorsikaId","px","py","pz","xprime","yprime","t",
        "shower_id","prm_id","prm_energy","prm_theta","prm_phi"]

def load_sec(path):
    df = pd.read_csv(
        path,
        comment="#",
        sep=' ',# separation is space,
        header=None,
        names=COLS,
        engine="python"
    )

    # Count unique showers BEFORE subsetting
    total_unique_showers = df["shower_id"].nunique()
    
    for c in ["CorsikaId","px","py","pz"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    
    df = df.dropna(subset=["CorsikaId","px","py","pz"])

    # Filter: Only Muons
    df_muons = df[df["CorsikaId"].isin([5, 6])].copy()
    
    # Zenith angle calculation
    df_muons['p'] = np.sqrt(df_muons['px']**2 + df_muons['py']**2 + df_muons['pz']**2)
    df_muons = df_muons[df_muons['p'] > 0]
    df_muons['theta_rad'] = np.arccos(np.clip(df_muons['pz'] / df_muons['p'], -1.0, 1.0)) 
    df_muons['theta'] = np.rad2deg(df_muons['theta_rad'])

    return df_muons, total_unique_showers

def main():
    ap = argparse.ArgumentParser(description="Muon Analysis with Embedded Metadata")
    ap.add_argument("-i","--input", required=True, help="Path to .sec file")
    ap.add_argument("-o","--outdir", default="arti_plots", help="Output directory")
    ap.add_argument("--dpi", type=int, default=220, help="Figure DPI")
    args = ap.parse_args()

    # --- Collect Metadata ---
    print("\n--- Simulation Metadata ---")
    loc_name = input("Enter Location Name: ").strip().title() or "Unknown_Loc"
    altitude = input("Enter Altitude (meters): ").strip() or "0m"
    atmo_model = input("Enter Atmospheric Model (E1 or E2): ").strip() or "Standard"
    
    try:
        t_input = input("Simulation time (seconds) [Default 1.0]: ")
        sim_time = float(t_input) if t_input.strip() else 1.0
    except ValueError:
        sim_time = 1.0

    os.makedirs(args.outdir, exist_ok=True)

    # Load and process
    df, unique_showers = load_sec(args.input)
    total_muons = len(df)

    # Histogram & Math
    bins = np.arange(0, 91, 10)
    counts, bin_edges = np.histogram(df['theta'], bins=bins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0
    bin_edges_rad = np.deg2rad(bin_edges) 
    solid_angles = 2 * np.pi * (np.cos(bin_edges_rad[:-1]) - np.cos(bin_edges_rad[1:]))
    flux_intensity = counts / sim_time / solid_angles

    def cos_squared_model(theta_deg, I0):
       return I0 * np.cos(np.deg2rad(theta_deg))**2
    
    try:
        popt, _ = curve_fit(cos_squared_model, bin_centers, flux_intensity, p0=[max(flux_intensity)])
        I0_fit = popt[0]
    except:
        I0_fit = 0

    # --- Plotting ---
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.scatter(bin_centers, flux_intensity, color='blue', s=40, label='Simulated Muons', zorder=3)

    if I0_fit > 0:
        theta_range = np.linspace(0, 90, 100)
        ax.plot(theta_range, cos_squared_model(theta_range, I0_fit), 'r-', linewidth=2,
                 label=r'Fit: $I(\theta) = ' + f'{I0_fit:.2f}' + r' \cos^2\theta$', zorder=4)

    # Create the metadata string for the on-image box
    info_text = (
        f"Location: {loc_name}\n"
        f"Altitude: {altitude}\n"
        f"Atmosphere: {atmo_model}\n"
        f"Total Showers: {unique_showers}\n"
        f"Total Muons: {total_muons}\n"
        f"Sim Time: {sim_time}s"
    )

    # Add text box to the plot (top right)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.95, 0.95, info_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right', bbox=props)

    ax.set_title(f'Muon Flux Intensity: {loc_name}', fontsize=16, pad=20)
    ax.set_xlabel('Zenith Angle $\\theta$ (degrees)', fontsize=12)
    ax.set_ylabel(r'Intensity $I(\theta)$ [particles / (s $\cdot$ sr)]', fontsize=12)
    ax.legend(loc='upper left')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Save Image
    safe_loc = loc_name.replace(" ", "_")
    base_name = f"{safe_loc}_{altitude}_{atmo_model}_T{sim_time}"
    img_path = os.path.join(args.outdir, f"{base_name}.png")

    plt.tight_layout()
    plt.savefig(img_path, dpi=args.dpi)
    plt.close()
    
    
    print(f"\n[DONE]")
    print(f"Image: {img_path}")

if __name__ == "__main__":
    main()