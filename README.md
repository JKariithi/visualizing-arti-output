# Visualizing ARTI Output

A Python-based analysis tool designed to process **CORSIKA/ARTI** simulation data. This script calculates muon flux intensity, fits the data to the theoretical $I_0 \cos^2\theta$ model, and generates high-resolution visualizations with embedded simulation metadata.

## 🚀 Features
* **Metadata Persistence:** Automatically embeds location name, altitude, atmospheric model, and particle counts directly into the plot image.
* **Physics Modeling:** Performs non-linear least-squares fitting to find the vertical muon intensity ($I_0$).
* **Data Cleaning:** Automatically handles unique shower counts and filters for muon species (IDs 5 & 6) from `.sec` or `.shw` files.
* **Professional Plots:** Generates publication-ready figures with LaTeX-formatted labels.

## 📋 Prerequisites

Ensure you have Python 3.8+ installed. You will need the following libraries:
* `numpy`
* `pandas`
* `matplotlib`
* `scipy`

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone 
   cd visualizing-arti-output
   ```

2. Create the Virtual Environment**
Open your terminal in the folder where your script is located and run:
```bash
python3 -m venv muon_env
```

**2. Activate the Environment**
* **On Linux/macOS:**
    ```bash
    source muon_env/bin/activate
    ```
* **On Windows:**
    ```bash
    .\muon_env\Scripts\activate
    ```

3. Install Requirements**
Once activated, your terminal should show `(muon_env)`. Now, install the necessary libraries:
```bash
pip install -r requirements.txt
```


## 📖 Usage

Run the script by providing the path to your simulation file and the desired output directory:

```bash
python3 visualize_arti.py -i your_data.shw -o arti_plots
```

### Interactive Prompts
Upon running, the script will prompt you for:
1. **Location Name** (e.g., Chyulu Hills)
2. **Altitude** (e.g., 2500m)
3. **Atmospheric Model** (e.g., E1)
4. **Simulation Time** (The duration in seconds the simulation was set to represent)

## 📊 Output
The script generates a `.png` file named according to your metadata (e.g., `Muon_Dist_Chyulu_Hills_2500m_E1.png`). 

**The final plot includes:**
* A scatter plot of simulated muon flux.
* A red trend line representing the $I_0 \cos^2\theta$ fit.
* An information box in the top-right corner containing all simulation parameters for easy retrieval.

