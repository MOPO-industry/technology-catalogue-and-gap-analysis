The main script performs the following operations:
1. Load raw JRC IDEES data from: input_data/jrc_idees_2021/industry
2. Extract key datasets
 - Production data
 - Energy use
 - Useful energy
 - Emissions
3. Compute metrics for the products of interest not in AIDRES:
 - Production (where the consumption index is replaced by energy use for 'food, beverages and tobacco' and 'textile and leather') 
 - Average energy use per unit of production (calculated for every energy carrier used in the technology catalogue)
 - Average emissions per unit of production
4. For steel‑specific detailed calculations for primary and secondary steel, the script additionally computes:
 - Energy use per unit of production (for every energy carrier in the technology catalogue) for:
	- rolling
	- finishing
 - Average emissions per unit of production for:
	- rolling
	- finishing
5. Calculates alternative future production routes using natural gas in case of high-enthalpy heat, and heat, electricity and biomass and waste in case of low-enthalpy heat or other processes
6. Save processed datasets to: input_data/processed_jrc_idees_data/

Clone repository:
git clone https://github.com/<your-org>/<your-repo>.git
cd <your-repo>

Install requirements:
pip install -r requirements.txt
