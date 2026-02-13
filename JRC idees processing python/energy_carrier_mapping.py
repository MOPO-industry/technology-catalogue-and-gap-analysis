energy_carrier_mapping_jrc_idees_to_EB = {
    'Solar and geothermal': 'heat',
    'Electricity': 'electricity',
    'LPG': 'oil_petro_products',
    'Diesel oil and liquid biofuels': 'oil_petro_products',
    'Diesel oil': 'oil_petro_products',
    'Naphtha': 'oil_petro_products',
    'Natural gas and biogas': 'natural_gas',
    'Natural gas': 'natural_gas',
    'Solids': 'solid_fossil_fuels',
    'Refinery gas': 'oil_petro_products',
    'Fuel oil': 'oil_petro_products',
    'Other liquids': 'oil_petro_products',
    'Derived gases': 'solid_fossil_fuels',
    'Biomass and waste': 'renew_bio',
    'Distributed steam': 'steam',
    'Ambient heat': 'heat',
    'Coke': 'solid_fossil_fuels'
}

classification_1_mapping = {
    'Lighting': 'electricity',
    'Air compressors': 'electricity',
    'Motor drives': 'electricity',
    'Fans and pumps': 'electricity',
    'Steel: Electric arc': 'electricity',
    #'Steel: Blast /Basic oxygen furnace': 'electricity', # Not sure
    'Electricity': 'electricity',
    'Aluminium electrolysis (smelting)': 'electricity',
    'Chemicals: Generic electric process': 'electricity',
    'Cement: Grinding, milling of raw material': 'electricity',
    'Distributed steam': 'steam',
    'Ceramics: Mixing of raw material': 'electricity',
    'Glass: Forming': 'electricity', # Not sure
    'Glass: Finishing processes': 'electricity', # Not sure
    'Pulp: Wood preparation, grinding': 'electricity',
    'Pulp: Cleaning': 'electricity', # Not sure
    'Printing and publishing': 'electricity', # Not sure
    'Food: Electric machinery': 'electricity',
    'Textiles: Electric general machinery': 'electricity',
    'Textiles: Finishing Electric': 'electricity',
    'Trans. Eq.: General machinery': 'electricity', # Not sure
    'Trans. Eq.: Product finishing': 'electricity', # Not sure
    'Mach. Eq.: General machinery': 'electricity', # Not sure
    'Mach. Eq.: Product finishing': 'electricity', # Not sure
    'Wood: Electric mechanical processes': 'electricity',
    'Wood: Finishing Electric': 'electricity',
    'Other Industrial sectors: Diesel motors (incl. biofuels)': 'oil_petro_products',
    'Other Industrial sectors: Electric machinery': 'electricity'
}

classification_2_mapping = {
    'Steel: Product finishing - Electric': 'electricity',
    'Aluminium finishing - Electric': 'electricity',
    'Metal finishing - Electric': 'electricity',
    'Ceramics: Electric furnace': 'electricity',
    'Paper: Product finishing - Electricity': 'electricity',
    'Steel: Furnaces, refining and rolling - Electric': 'electricity',
    'Aluminium processing - Electric': 'electricity',
    'Secondary aluminium - Electric': 'electricity',
    'Metal production - Electric': 'electricity',
    'Metal processing - Electric': 'electricity',
    'Chemicals: Furnaces - Electric': 'electricity',
    'Chemicals: Process cooling - Natural gas and biogas': 'natural_gas',
    'Chemicals: Process cooling - Electric': 'electricity',
    'High-enthalpy heat processing - Electric (microwave)': 'electricity',
    'Cement: Grinding, packaging and precasting (electricity)': 'electricity',
    'Ceramics: Microwave drying and sintering': 'electricity',
    'Ceramics: Electric kiln': 'electricity',
    'Glass: Electric melting tank': 'electricity',
    'Glass: Annealing - electric': 'electricity',
    'Pulp: Pulping electric': 'electricity',
    'Paper: Stock preparation - Mechanical': 'electricity',
    'Paper: Paper machine - Electricity': 'electricity',
    'Food: Direct Heat - Electric': 'electricity',
    'Food: Direct Heat - Microwave': 'electricity',
    'Food: Process Heat - Electric': 'electricity',
    'Food: Process Heat - Microwave': 'electricity',
    'Food: Electric drying': 'electricity',
    'Food: Freeze drying': 'electricity',
    'Food: Microwave drying': 'electricity',
    'Food: Thermal cooling': 'heat',
    'Food: Electric cooling': 'electricity',
    'Textiles: Electric drying': 'electricity',
    'Textiles: Microwave drying': 'electricity',
    'Trans. Eq.: Electric Foundries': 'electricity',
    'Trans. Eq.: Thermal connection': 'heat',
    'Trans. Eq.: Electric connection': 'electricity',
    'Trans. Eq.: Heat treatment - Electric': 'electricity',
    'Mach. Eq.: Electric Foundries': 'electricity',
    'Mach. Eq.: Thermal connection': 'heat',
    'Mach. Eq.: Electric connection': 'electricity',
    'Mach. Eq.: Heat treatment - Electric': 'electricity',
    'Wood: Electric drying': 'electricity',
    'Wood: Microwave drying': 'electricity',
    'Other Industrial sectors: Electric processing': 'electricity',
    'Other Industries: Electric drying': 'electricity',
    'Other Industries: Thermal cooling': 'heat',
    'Other Industries: Electric cooling': 'electricity'
}

jrc_products_of_interest = (
    "Integrated_steelworks",
    "Electric_arc",
    "Alumina",
    "Aluminium_primary",
    "Aluminium_secondary",
    "Other_non_ferrous",
    "Basic_chemicals",
    "Other_chemicals",
    "Pharmaceutical_products",
    "Cement",
    "Ceramics_and_other_non_metalic_minerals",
    "Glass",
    "Pulp",
    "Paper",
    "Printing_and_media",
    "Food_beverages_and_tobacco",
    "Textile_and_leather",
    "transport_equipment",
    "machinery_equipment",
    "wood_and_wood_products",
    "other_industrial_sectors"
)
