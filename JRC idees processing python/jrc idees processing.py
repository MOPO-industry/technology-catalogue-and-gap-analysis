import pandas as pd
import os
from pathlib import Path

from row_mapping import detailed_line_mapping
from row_mapping import energy_use_header_mapping
from row_mapping import useful_energy_header_mapping
from row_mapping import products_with_proces_emissions
from row_mapping import production_mapping
from row_mapping import production_header_mapping
from row_mapping import CO2_header_mapping

from unit_mapping import energy_use_unit_mapping
from unit_mapping import production_unit_mapping
from unit_mapping import CO2_unit_mapping

from energy_carrier_mapping import energy_carrier_mapping_jrc_idees_to_EB
from energy_carrier_mapping import classification_1_mapping
from energy_carrier_mapping import classification_2_mapping
from energy_carrier_mapping import jrc_products_of_interest

from new_production_proces_mapping import new_production_proces_mapping
from new_production_proces_mapping import original_production_proces_mapping
from new_production_proces_mapping import heat_pump_processes

from preprocessing_tc_mapping import sector_mapping_tc
from preprocessing_tc_mapping import product_mapping_tc
from preprocessing_tc_mapping import industry_mapping_tc
from preprocessing_tc_mapping import energy_carrier_mapping_tc
from preprocessing_tc_mapping import mapping_energy_tc
from preprocessing_tc_mapping import mapping_production_tc
from preprocessing_tc_mapping import mapping_CO2_tc

from utility import filter_jrc_idees_detailed
from utility import filter_jrc_idees
from utility import fill_energy_carrier_EB_column
from utility import build_tc_energy_use_tables
from utility import build_tc_production_co2_and_lifetime_tables
from utility import create_new_production_proces
from utility import replace_production_by_energy_use
from utility import build_steel_finishing_outputs
from utility import update_original_production_proces
from utility import useful_energy_per_capacity

Path("additional_data").mkdir(exist_ok=True)
Path(r"../input_data/processed_jrc_idees_data").mkdir(exist_ok=True)

year_of_interest = 2021
ktoe_to_TJ = 41.868


# CAPEX and OPEX from Danish technology catalogue:
# - High-temperature heat pumps up to 150 °C
# - Electric boiler, 10 kV, steam, 1-12 bar
# - Boiler, gas and oil
capex_heat_pump_2025 = 1.55 / 365 / 24 * 1000000  # yr.€/MWh
capex_heat_pump_2030 = 1.5 / 365 / 24 * 1000000  # yr.€/MWh
capex_heat_pump_2040 = 1.4 / 365 / 24 * 1000000  # yr.€/MWh
capex_heat_pump_2050 = 1.35 / 365 / 24 * 1000000  # yr.€/MWh
capex_electric_steam_boiler_2025 = 0.11 / 365 / 24 * 1000000  # yr.€/MWh
capex_electric_steam_boiler_2030_2040_2050 = 0.1 / 365 / 24 * 1000000  # yr.€/MWh
capex_gas_boiler = 0.09 / 365 / 24 * 1000000  # yr.€/MWh

opex_cst_heat_pump_2025 = 2494 / 365 / 24 # €/MWh
opex_cst_heat_pump_2030 = 2456 / 365 / 24 # €/MWh
opex_cst_heat_pump_2040 = 2382 / 365 / 24 # €/MWh
opex_cst_heat_pump_2050 = 2345 / 365 / 24 # €/MWh
opex_cst_electric_steam_boiler_2025 = 1298 / 365 / 24 # €/MWh
opex_cst_electric_steam_boiler_2030 = 1237 / 365 / 24 # €/MWh
opex_cst_electric_steam_boiler_2040 = 1177 / 365 / 24 # €/MWh
opex_cst_electric_steam_boiler_2050 = 1116 / 365 / 24 # €/MWh
opex_cst_gas_boiler = 2000 / 365 / 24 # €/MWh


product_mapping = {"Integrated_steelworks": "ISI",
                   "Electric_arc": "ISI",
                   "Alumina": "NFM",
                   "Aluminium_primary": "NFM",
                   "Aluminium_secondary": "NFM",
                   "Other_non_ferrous": "NFM",
                   "Basic_chemicals": "CHI",
                   "Other_chemicals": "CHI",
                   "Pharmaceutical_products": "CHI",
                   "Cement": "NMM",
                   "Ceramics_and_other_non_metalic_minerals": "NMM",
                   "Glass": "NMM",
                   "Pulp": "PPA",
                   "Paper": "PPA",
                   "Printing_and_media": "PPA",
                   "Food_beverages_and_tobacco": "FBT",
                   "Textile_and_leather": "TEL",
                   "transport_equipment": "TRE",
                   "machinery_equipment": "MAE",
                   "wood_and_wood_products": "WWP",
                   "other_industrial_sectors": "OIS"
                   }

# GET ENERGY USE DATA FROM JRC IDEES
jrc_energy_use_per_carrier = filter_jrc_idees_detailed(
    "../input_data/jrc_idees_2021/industry/",
    detailed_line_mapping,
    product_mapping,
    energy_use_header_mapping,
    year_of_interest,
    jrc_products_of_interest,
    energy_use_unit_mapping,
    'fec',
    products_with_proces_emissions,
    ktoe_to_TJ
)


# GET USEFUL ENERGY DATA FROM JRC IDEES
jrc_useful_energy_per_carrier = filter_jrc_idees_detailed(
    "../input_data/jrc_idees_2021/industry/",
    detailed_line_mapping,
    product_mapping,
    useful_energy_header_mapping,
    year_of_interest,
    jrc_products_of_interest,
    energy_use_unit_mapping,
    'ued',
    products_with_proces_emissions,
    ktoe_to_TJ
)


# GET CO2 EMISSION DATA FROM JRC IDEES
jrc_CO2_emission_per_carrier = filter_jrc_idees_detailed(
    "../input_data/jrc_idees_2021/industry/",
    detailed_line_mapping,
    product_mapping,
    CO2_header_mapping,
    year_of_interest,
    jrc_products_of_interest,
    CO2_unit_mapping,
    'emi',
    products_with_proces_emissions,
    ktoe_to_TJ
)


# COMBINE ENERGY USE, USEFUL ENERGY AND CO2 EMISSIONS DATAFRAMES
jrc_original_and_new_energy_use = pd.merge(jrc_CO2_emission_per_carrier.drop(columns = ['unit']),
                                           jrc_energy_use_per_carrier.drop(columns = ['unit']),
                                           on=['country_code', 'sector', 'product',
                                               'year', 'classification_1', 'classification_2',
                                               'energy_carrier_jrc_idees'],
                                           how='left')


jrc_original_and_new_energy_use = pd.merge(jrc_original_and_new_energy_use,
                                           jrc_useful_energy_per_carrier.drop(columns = ['unit']),
                                           on=['country_code', 'sector', 'product',
                                               'year', 'classification_1', 'classification_2',
                                               'energy_carrier_jrc_idees'],
                                           how='left')


# CALCULATE ENERGY EFFICIENCY AND CO2 INTENSITY
jrc_original_and_new_energy_use['efficiency_(%)'] = jrc_original_and_new_energy_use['useful_energy_(TJ)']/jrc_original_and_new_energy_use['energy_use_(TJ)']
jrc_original_and_new_energy_use['CO2_intensity_(kt/TJ)'] = jrc_original_and_new_energy_use['CO2_emissions_(kt)']/jrc_original_and_new_energy_use['useful_energy_(TJ)']


# ADD ENERGY BALANCE CARRIER NAMES
jrc_original_and_new_energy_use = fill_energy_carrier_EB_column(jrc_original_and_new_energy_use,
                                                           energy_carrier_mapping_jrc_idees_to_EB,
                                                           classification_1_mapping,
                                                           classification_2_mapping)


# REPLACE STEAM AND HEAT ENERGY CARRIERS
jrc_original_and_new_energy_use = update_original_production_proces(jrc_original_and_new_energy_use, original_production_proces_mapping)

# ADJUST ENERGY USE FOR FUTURE ROUTE AND MAKE COPY WITH ORIGINAL AND NEW ENERGY USE AND CO2 EMISSIONS
jrc_original_and_new_energy_use = create_new_production_proces(jrc_original_and_new_energy_use, new_production_proces_mapping, heat_pump_processes)

jrc_original_energy_and_feedstock_use_and_CO2_per_carrier_simplified = jrc_original_and_new_energy_use.copy().groupby([
    'country_code', 'sector', 'product', 'year', 'energy_carrier_EB'])[
    ['energy_use_(TJ)', 'CO2_emissions_(kt)', 'useful_energy_(TJ)']].sum().reset_index()

jrc_original_energy_and_feedstock_use_and_CO2_total = jrc_original_and_new_energy_use.copy().groupby([
    'country_code', 'sector', 'product', 'year'])[
    ['energy_use_(TJ)', 'CO2_emissions_(kt)', 'useful_energy_(TJ)']].sum().reset_index()

jrc_new_energy_and_feedstock_use_and_CO2_per_carrier_simplified = jrc_original_and_new_energy_use.copy().groupby([
    'country_code', 'sector', 'product', 'year', 'new_energy_carrier_EB'])[
    ['new_energy_use_(TJ)', 'new_CO2_emissions_(kt)', 'useful_energy_(TJ)']].sum().reset_index()

jrc_new_energy_and_feedstock_use_and_CO2_total = jrc_original_and_new_energy_use.copy().groupby([
    'country_code', 'sector', 'product', 'year'])[
    ['new_energy_use_(TJ)', 'new_CO2_emissions_(kt)', 'useful_energy_(TJ)']].sum().reset_index()


# GET PRODUCTION DATA FROM JRC IDEES AND MAKE SEPARATE COPY (NEW AND ORIGINAL)
jrc_production = filter_jrc_idees(
    "../input_data/jrc_idees_2021/industry",
    production_mapping,
    product_mapping,
    production_header_mapping,
    year_of_interest,
    jrc_products_of_interest,
    production_unit_mapping
)[['sector', 'country_code', 'product', 'year', 'unit', 'actual_capacity']]
jrc_production_new = jrc_production.copy()
jrc_production_original = jrc_production.copy()

useful_energy_per_capacity_df, useful_energy_per_capacity_df_sum = useful_energy_per_capacity(
    ['Food_beverages_and_tobacco',
     'Textile_and_leather',
     'transport_equipment',
     'machinery_equipment',
     'wood_and_wood_products',
     'other_industrial_sectors'],
    jrc_production_original,
    jrc_original_energy_and_feedstock_use_and_CO2_total,
    'useful_energy_(TJ)')

useful_energy_per_capacity_df_sum.to_csv(r"../input_data/processed_jrc_idees_data/useful_energy_per_production_index.csv", index=False)

# REPLACE PRODUCTION BY ENERGY USE FOR FBT AND TEL (ORIGINAL PROCES)
jrc_production_original = replace_production_by_energy_use(
    ['Food_beverages_and_tobacco',
     'Textile_and_leather',
     'transport_equipment',
     'machinery_equipment',
     'wood_and_wood_products',
     'other_industrial_sectors'],
    jrc_production_original,
    jrc_original_energy_and_feedstock_use_and_CO2_total,
    'useful_energy_(TJ)')


# REPLACE PRODUCTION BY ENERGY USE FOR FBT AND TEL (NEW PROCES)
jrc_production_new = replace_production_by_energy_use(
    ['Food_beverages_and_tobacco',
     'Textile_and_leather',
     'transport_equipment',
     'machinery_equipment',
     'wood_and_wood_products',
     'other_industrial_sectors'],
    jrc_production_new,
    jrc_new_energy_and_feedstock_use_and_CO2_total,
    'useful_energy_(TJ)')


filter_jrc_sectors = ["food-beverages-tobacco-production", "alumina-production",
                      "aluminium-primary-production", "aluminium-secondary-production",
                      "other-non-ferrous-metals-production", "ceramics-and-other-non-metalic-minerals-production",
                      "paper-production", "printing-and-media-production", "pulp-production",
                      "leather-and-textile-production", "transport-equipment-production",
                      "machinery-equipment-production", "wood-and-wood-products_production",
                      "other-industrial-sectors_production", "other-chemicals-production",
                      "pharmaceuticals-production"]


jrc_original_energy_and_feedstock_use_and_CO2_per_carrier_simplified = jrc_original_energy_and_feedstock_use_and_CO2_per_carrier_simplified[
    ['country_code', 'sector', 'product', 'year', 'energy_carrier_EB',
    'energy_use_(TJ)', 'CO2_emissions_(kt)', 'useful_energy_(TJ)']
]

jrc_original_energy_and_feedstock_use_and_CO2_total = jrc_original_energy_and_feedstock_use_and_CO2_total[
    ['country_code', 'sector', 'product', 'year',
    'energy_use_(TJ)', 'CO2_emissions_(kt)', 'useful_energy_(TJ)']
]

jrc_new_energy_and_feedstock_use_and_CO2_per_carrier_simplified = jrc_new_energy_and_feedstock_use_and_CO2_per_carrier_simplified[
    ['country_code', 'sector', 'product', 'year', 'new_energy_carrier_EB',
     'new_energy_use_(TJ)', 'new_CO2_emissions_(kt)', 'useful_energy_(TJ)']
]

jrc_new_energy_and_feedstock_use_and_CO2_total = jrc_new_energy_and_feedstock_use_and_CO2_total[
    ['country_code', 'sector', 'product', 'year',
     'new_energy_use_(TJ)', 'new_CO2_emissions_(kt)', 'useful_energy_(TJ)']
]


####################################################
#### GET ENERGY USE DATA FOR NON-AIDRES SECTORS ####
####################################################

orig_out, orig_sum, proces_energy_original_out_simplified, original_capex_opex = build_tc_energy_use_tables(
    energy_df=jrc_original_energy_and_feedstock_use_and_CO2_per_carrier_simplified,
    production_df=jrc_production_original,
    energy_col='energy_use_(TJ)',
    carrier_col='energy_carrier_EB',
    scenario_suffix='-reference',
    final_year_map={'2025': 'mean', '2030': 'copy', '2040': 'copy', '2050': 'copy'},
    sector_mapping_tc=sector_mapping_tc,
    product_mapping_tc=product_mapping_tc,
    industry_mapping_tc=industry_mapping_tc,
    filter_jrc_sectors=filter_jrc_sectors,
    mapping_energy_tc=mapping_energy_tc,
    energy_carrier_mapping_tc=energy_carrier_mapping_tc)

new_out, new_sum, proces_energy_new_out_simplified, new_capex_opex = build_tc_energy_use_tables(
    energy_df=jrc_new_energy_and_feedstock_use_and_CO2_per_carrier_simplified,
    production_df=jrc_production_new,
    energy_col='new_energy_use_(TJ)',
    carrier_col='new_energy_carrier_EB',
    scenario_suffix='-alternative',
    final_year_map={'2025': 'mean', '2030': 'copy', '2040': 'copy', '2050': 'copy'},
    sector_mapping_tc=sector_mapping_tc,
    product_mapping_tc=product_mapping_tc,
    industry_mapping_tc=industry_mapping_tc,
    filter_jrc_sectors=filter_jrc_sectors,
    mapping_energy_tc=mapping_energy_tc,
    energy_carrier_mapping_tc=energy_carrier_mapping_tc)

df_capex_heat_pump = pd.DataFrame({
    "energy_carrier_EB": ["electricity-heat-pump", "electricity", "natural_gas"],
    "2025": [capex_heat_pump_2025, capex_electric_steam_boiler_2025, capex_gas_boiler],
    "2030": [capex_heat_pump_2030, capex_electric_steam_boiler_2030_2040_2050, capex_gas_boiler],
    "2040": [capex_heat_pump_2040, capex_electric_steam_boiler_2030_2040_2050, capex_gas_boiler],
    "2050": [capex_heat_pump_2050, capex_electric_steam_boiler_2030_2040_2050, capex_gas_boiler]
})

df_opex_heat_pump = pd.DataFrame({
    "energy_carrier_EB": ["electricity-heat-pump", "electricity", "natural_gas"],
    "2025": [opex_cst_heat_pump_2025, opex_cst_electric_steam_boiler_2025, opex_cst_gas_boiler],
    "2030": [opex_cst_heat_pump_2030, opex_cst_electric_steam_boiler_2030, opex_cst_gas_boiler],
    "2040": [opex_cst_heat_pump_2040, opex_cst_electric_steam_boiler_2040, opex_cst_gas_boiler],
    "2050": [opex_cst_heat_pump_2050, opex_cst_electric_steam_boiler_2050, opex_cst_gas_boiler]
})
new_capex = new_capex_opex.copy().merge(df_capex_heat_pump, on='energy_carrier_EB', how='left')
new_opex = new_capex_opex.copy().merge(df_opex_heat_pump, on='energy_carrier_EB', how='left')


def construct_capex_opex(df, ext, cost):
    years = ['2025', '2030', '2040', '2050']

    for year in years:
        df[year] = df[year] * df['energy_use_converted']
    df['unit'] = ext+df['unit_energy_use_converted'].str[3:]
    df = df[['country_code', 'sector_id', 'to_node', 'Industry', 'energy_carrier_tc', 'unit', '2025', '2030', '2040', '2050']]
    df = df.groupby(['country_code', 'sector_id', 'to_node', 'unit', 'Industry'])[['2025', '2030', '2040', '2050']].sum().reset_index()
    df = df[~(df[years] == 0).all(axis=1)]
    df_mean = df.copy().groupby(['sector_id', 'to_node', 'Industry', 'unit'])[['2025', '2030', '2040', '2050']].mean().reset_index()
    df_sd = df.copy().groupby(['sector_id', 'to_node', 'Industry', 'unit'])[['2025', '2030', '2040', '2050']].std().reset_index()
    df_sd = df_sd.rename(columns={c: f"{c}_sd" for c in years})
    df = pd.merge(df_mean, df_sd, on = ['sector_id', 'to_node', 'Industry', 'unit'], how = 'left')
    df['costs'] = cost

    return df

new_capex = construct_capex_opex(new_capex, 'eur-yr', 'capex')
new_opex = construct_capex_opex(new_opex, 'eur', 'fom')


###############################################################################
#### GET PRODUCTION, CO2 EMISSION AND LIFETIME DATA FOR NON-AIDRES SECTORS ####
###############################################################################

production_original_out, CO2_emissions_original_out_simplified, lifetime_original_out = build_tc_production_co2_and_lifetime_tables(
    energy_co2_df=jrc_original_energy_and_feedstock_use_and_CO2_total,
    production_df=jrc_production_original,
    co2_col='CO2_emissions_(kt)',
    industry_suffix='-reference',
    sector_mapping_tc=sector_mapping_tc,
    product_mapping_tc=product_mapping_tc,
    industry_mapping_tc=industry_mapping_tc,
    filter_jrc_sectors=filter_jrc_sectors,
    mapping_production_tc=mapping_production_tc,
    mapping_CO2_tc=mapping_CO2_tc,
    prod_year_base='2018',            # <- matches your original code
    prod_year_copy_to=[],
    emis_year_base='2025',            # <- matches your original code
    emis_year_copy_to=['2030','2040','2050']
)

# --- NEW (alternative)
production_new_out, CO2_emissions_new_out_simplified, lifetime_new_out = build_tc_production_co2_and_lifetime_tables(
    energy_co2_df=jrc_new_energy_and_feedstock_use_and_CO2_total,
    production_df=jrc_production_new,
    co2_col='new_CO2_emissions_(kt)',
    industry_suffix='-alternative',
    sector_mapping_tc=sector_mapping_tc,
    product_mapping_tc=product_mapping_tc,
    industry_mapping_tc=industry_mapping_tc,
    filter_jrc_sectors=filter_jrc_sectors,
    mapping_production_tc=mapping_production_tc,
    mapping_CO2_tc=mapping_CO2_tc,
    prod_year_base='2030',            # <- your new flow
    prod_year_copy_to=['2050'],       # <- copy 2030 into 2050
    emis_year_base='2025',            # <- your new flow
    emis_year_copy_to=['2030','2040','2050']
)


##################################################
#### GET STEEL DATA FOR FINISHING AND ROLLING ####
##################################################

outputs_new_steel = build_steel_finishing_outputs(
    energy_use_df=jrc_original_and_new_energy_use,
    production_df=jrc_production_new,
    energy_use_tj_col='new_energy_use_(TJ)',
    co2_emissions_kt_col='new_CO2_emissions_(kt)',
    energy_carrier_eb_col='new_energy_carrier_EB',
    sector_mapping_tc=sector_mapping_tc,
    product_mapping_tc=product_mapping_tc,
    energy_carrier_mapping_tc=energy_carrier_mapping_tc,
    mapping_energy_tc=mapping_energy_tc,
    mapping_production_tc=mapping_production_tc,
    mapping_CO2_tc=mapping_CO2_tc,
    energy_years=['2025','2030','2040','2050'],
    energy_base_year='2025',
    co2_years=['2025','2030','2040','2050'],
    co2_base_year='2025',
    ref_or_alt='alternative'
)

steel_finishing_new_out                   = outputs_new_steel['steel_finishing_out']
steel_finishing_new_out_energy_simplified = outputs_new_steel['energy_simplified']
steel_finishing_new_out_CO2_simplified    = outputs_new_steel['co2_simplified']
lifetime_steel_finishing_new_out          = outputs_new_steel['lifetime_out']

steel_capex_opex = steel_finishing_new_out.copy()
steel_capex_opex = steel_capex_opex[['country_code', 'sector_id', 'to_node', 'Industry',
                                     'energy_carrier_tc', 'new_energy_carrier_EB',
                                     'energy_use_converted', 'unit_energy_use_converted']]
steel_capex_opex = steel_capex_opex.rename(columns={'new_energy_carrier_EB': 'energy_carrier_EB'})
new_steel_capex = steel_capex_opex.copy().merge(df_capex_heat_pump, on='energy_carrier_EB', how='left')
new_steel_opex = steel_capex_opex.copy().merge(df_opex_heat_pump, on='energy_carrier_EB', how='left')

new_steel_capex = construct_capex_opex(new_steel_capex, 'eur-yr', 'capex')
new_steel_opex = construct_capex_opex(new_steel_opex, 'eur', 'fom')

outputs_original_steel = build_steel_finishing_outputs(
    energy_use_df=jrc_original_and_new_energy_use,
    production_df=jrc_production_original,
    energy_use_tj_col='energy_use_(TJ)',
    co2_emissions_kt_col='CO2_emissions_(kt)',
    energy_carrier_eb_col='energy_carrier_EB',
    sector_mapping_tc=sector_mapping_tc,
    product_mapping_tc=product_mapping_tc,
    energy_carrier_mapping_tc=energy_carrier_mapping_tc,
    mapping_energy_tc=mapping_energy_tc,
    mapping_production_tc=mapping_production_tc,
    mapping_CO2_tc=mapping_CO2_tc,
    energy_years=['2025','2030','2040','2050'],
    energy_base_year='2025',
    co2_years=['2025','2030','2040','2050'],
    co2_base_year='2025',
    ref_or_alt='reference'
)

steel_finishing_original_out                   = outputs_original_steel['steel_finishing_out']
steel_finishing_original_out_energy_simplified = outputs_original_steel['energy_simplified']
steel_finishing_original_out_CO2_simplified    = outputs_original_steel['co2_simplified']
lifetime_steel_finishing_original_out          = outputs_original_steel['lifetime_out']

# Export data for all processes not in AIDRES
proces_energy_new_out_simplified.to_csv(r"../input_data/processed_jrc_idees_data/proces_energy_new.csv", index=False)
proces_energy_original_out_simplified.to_csv("../input_data/processed_jrc_idees_data/proces_energy_original.csv", index=False)
CO2_emissions_new_out_simplified.to_csv("../input_data/processed_jrc_idees_data/CO2_emissions_new.csv", index=False)
production_new_out.to_csv("../input_data/processed_jrc_idees_data/production_new.csv", index=False)
CO2_emissions_original_out_simplified.to_csv("../input_data/processed_jrc_idees_data/CO2_emissions_original.csv", index=False)
production_original_out.to_csv("../input_data/processed_jrc_idees_data/production_original.csv", index=False)
lifetime_original_out.to_csv("../input_data/processed_jrc_idees_data/lifetime_original.csv", index=False)
lifetime_new_out.to_csv("../input_data/processed_jrc_idees_data/lifetime_new.csv", index=False)
new_capex.to_csv("../input_data/processed_jrc_idees_data/capex_new.csv", index=False)
new_opex.to_csv("../input_data/processed_jrc_idees_data/opex_new.csv", index=False)

# Export steel finishing and rolling data
steel_finishing_original_out_energy_simplified.to_csv("../input_data/processed_jrc_idees_data/steel_finishing_original_energy_out.csv", index=False)
steel_finishing_new_out_energy_simplified.to_csv("../input_data/processed_jrc_idees_data/steel_finishing_new_energy_out.csv", index=False)
steel_finishing_original_out_CO2_simplified.to_csv("../input_data/processed_jrc_idees_data/steel_finishing_original_CO2_out.csv", index=False)
steel_finishing_new_out_CO2_simplified.to_csv("../input_data/processed_jrc_idees_data/steel_finishing_new_CO2_out.csv", index=False)
lifetime_steel_finishing_original_out.to_csv("../input_data/processed_jrc_idees_data/lifetime_steel_finishing_original.csv", index=False)
lifetime_steel_finishing_new_out.to_csv("../input_data/processed_jrc_idees_data/lifetime_steel_finishing_new.csv", index=False)
new_steel_opex.to_csv("../input_data/processed_jrc_idees_data/opex_steel_new.csv", index=False)
new_steel_capex.to_csv("../input_data/processed_jrc_idees_data/capex_steel_new.csv", index=False)