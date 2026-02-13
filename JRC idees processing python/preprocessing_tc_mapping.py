import pandas as pd

sector_mapping_tc = {
    "ISI": "steel",
    "CHI": "chemical",
    "NFM": 'non-ferrous-metals',
    "NMM": 'ceramics-and-other-non-metallic-mineral-products-excluding-cement-and-glass',
    "PPA": 'pulp-and-paper',
    "FBT": 'food-beverages-and-tobacco',
    "TEL": 'textiles-and-leather',
    "TRE": "transport-equipment",
    "MAE": "machinery-equipment",
    "WWP": "wood-and-wood-products",
    "OIS": "other-industrial-sectors"
}

product_mapping_tc = {
    "Basic_chemicals": "basic-chemicals",
    "Other_chemicals": "other-chemicals",
    "Pharmaceutical_products": "pharmaceuticals",
    "Food_beverages_and_tobacco": "food-beverages-tobacco",
    "Electric_arc": "electric-arc-steel",
    "Integrated_steelworks": "integrated-steelworks-steel",
    "Alumina": "alumina",
    "Aluminium_primary": "aluminium-primary",
    "Aluminium_secondary": "aluminium-secondary",
    "Other_non_ferrous": "other-non-ferrous-metals",
    "Cement": "cement",
    "Ceramics_and_other_non_metalic_minerals": "ceramics-and-other-non-metalic-minerals",
    "Glass": "glass",
    "Paper": "paper",
    "Printing_and_media": "printing-and-media",
    "Pulp": "pulp",
    "Textile_and_leather": "leather-and-textile",
    "transport_equipment": "transport-equipment",
    "machinery_equipment": "machinery-equipment",
    "wood_and_wood_products": "wood-and-wood-products",
    "other_industrial_sectors": "other-industrial-sectors"
}


industry_mapping_tc = {
    "Basic_chemicals": "basic-chemicals-production",
    "Other_chemicals": "other-chemicals-production",
    "Pharmaceutical_products": "pharmaceuticals-production",
    "Food_beverages_and_tobacco": "food-beverages-tobacco-production",
    "Electric_arc": "electric-arc-steel-production",
    "Integrated_steelworks": "integrated-steelworks-steel-production",
    "Alumina": "alumina-production",
    "Aluminium_primary": "aluminium-primary-production",
    "Aluminium_secondary": "aluminium-secondary-production",
    "Other_non_ferrous": "other-non-ferrous-metals-production",
    "Cement": "cement-production",
    "Ceramics_and_other_non_metalic_minerals": "ceramics-and-other-non-metalic-minerals-production",
    "Glass": "glass-production",
    "Paper": "paper-production",
    "Printing_and_media": "printing-and-media-production",
    "Pulp": "pulp-production",
    "Textile_and_leather": "leather-and-textile-production",
    "transport_equipment": "transport-equipment-production",
    "machinery_equipment": "machinery-equipment-production",
    "wood_and_wood_products": "wood-and-wood-products_production",
    "other_industrial_sectors": "other-industrial-sectors_production"
}

energy_carrier_mapping_tc = {
    'electricity-heat-pump': "elec",
    "electricity": "elec",
    "heat": "heat",
    "steam": "steam",
    "natural_gas": "CH4",
    'oil_petro_products': "HC",
    "renew_bio": "bio",
    "solid_fossil_fuels": "coal"
}

mapping_energy_tc = pd.DataFrame(
    [
        ['TJ/kt ethylene eq.', 0.27778, 'mwh_t_ethylene_eq'],
        ['TJ/TJ', 1, 'mwh_mwh'],
        ['TJ/kt', 0.27778, 'mwh_t'],
        ['TJ/kt lead eq.', 0.27778, 'mwh_t_lead_eq'],
        ['TJ/kt bricks eq.', 0.27778, 'mwh_t_bricks_eq'],
        ['TJ/kt paper eq.', 0.27778, 'mwh_t_paper_eq']
    ],
    columns=["unit_energy_use", "conversion", "unit_energy_use_converted"])

mapping_production_tc = pd.DataFrame(
    [
        ['kt', 1,  'kt_yr'],
        ['kt lead eq.', 1, 'kt_lead_eq_yr'],
        ['kt ethylene eq.', 1, 'kt_ethylene_eq_yr'],
        ['kt bricks eq.', 1, 'kt_bricks_eq_yr'],
        ['kt paper eq.', 1, 'kt_paper_eq_yr'],
        ['TJ', 277.78, 'mwh_yr']
    ],
    columns=["unit_capacity", "conversion_production", "production_unit_converted"])

mapping_CO2_tc = pd.DataFrame(
    [
        ['ktco2/kt ethylene eq.', 1, 'tco2_t_ethylene_eq'],
        ['ktco2/TJ', 3.6, 'tco2_mwh'],
        ['ktco2/kt', 1, 'tco2_t'],
        ['ktco2/kt lead eq.', 1, 'tco2_t_lead_eq'],
        ['ktco2/kt bricks eq.', 1, 'tco2_t_bricks_eq'],
        ['ktco2/kt paper eq.', 1, 'tco2_t_paper_eq']
    ],
    columns=["unit_CO2_emissions_per_capacity", "conversion_co2_emissions", "co2_emissions_per_capacity_unit_converted"])
