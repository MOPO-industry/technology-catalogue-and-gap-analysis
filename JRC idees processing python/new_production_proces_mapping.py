alumina_new_production_proces_mapping = {
    'Low-enthalpy heat': ['Low-enthalpy heat', 'electricity'],  # HEAT PUMP!
    'Alumina production: High-enthalpy heat': ['Alumina production: High-enthalpy heat', 'natural_gas'], # Temperatures around 1000 °C
    'Alumina production: Refining': ['Alumina production: Refining', 'electricity']
}
aluminium_primary_new_production_proces_mapping = {
    'Low-enthalpy heat': ['Low-enthalpy heat', 'electricity'],  # HEAT PUMP!
    'Aluminium electrolysis (smelting)': ['Aluminium electrolysis (smelting)', 'electricity'],
    'Aluminium processing  (metallurgy e.g. cast house, reheating)': ['Aluminium processing  (metallurgy e.g. cast house, reheating)', 'electricity'],
    'Aluminium finishing': ['Aluminium finishing', 'electricity']
}
aluminium_secondary_new_production_proces_mapping = {
    'Low-enthalpy heat': ['Low-enthalpy heat', 'electricity'], # HEAT PUMP!
    'Secondary aluminium (incl. pre-treatment, remelting)': ['Secondary aluminium (incl. pre-treatment, remelting)', 'electricity'],
    'Aluminium processing  (metallurgy e.g. cast house, reheating)': ['Aluminium processing  (metallurgy e.g. cast house, reheating)', 'electricity'],
    'Aluminium finishing': ['Aluminium finishing', 'electricity'],
}
other_non_ferrous_metals_new_production_proces_mapping = {
    'Low-enthalpy heat': ['Low-enthalpy heat', 'electricity'],  # HEAT PUMP!
    'Metal processing  (metallurgy e.g. cast house, reheating)': ['Metal processing  (metallurgy e.g. cast house, reheating)', 'electricity'],
    'Other Metals: production': ['Other Metals: production', 'electricity'],
    'Metal finishing': ['Metal finishing', 'electricity']
}
food_beverages_and_tobacco_new_production_proces_mapping = {
    'Low-enthalpy heat': ['Low-enthalpy heat', 'electricity'], # HEAT PUMP!
    'Food: Oven (direct heat)': ['Food: Oven (direct heat)', 'electricity', 'Food: Direct Heat - Electric'],
    'Food: Specific process heat': ['Food: Specific process heat', 'electricity', 'Food: Process Heat - Electric'], # HEAT PUMP!
    'Food: Steam processing': ['Food: Specific process heat', 'electricity', 'Food: Process Heat - Electric'], # efficiency of specific process heat is used!
    'Food: Drying': ['Food: Drying', 'electricity', 'Food: Electric drying'], # HEAT PUMP!
    'Food: Process cooling and refrigeration': ['Food: Process cooling and refrigeration', 'electricity', 'Food: Electric cooling'], # HEAT PUMP!
    'Food: Electric machinery': ['Food: Electric machinery', 'electricity'] # MECHANICAL PROCESS
}
pulp_new_production_proces_mapping = {
    'Low-enthalpy heat': ['Low-enthalpy heat', 'electricity'],  # HEAT PUMP!
    'Pulp: Wood preparation, grinding': ['Pulp: Wood preparation, grinding', 'electricity'], # MECHANICAL PROCESS
    'Pulp: Pulping': ['Pulp: Pulping', 'electricity'],
    'Pulp: Cleaning': ['Pulp: Cleaning', 'electricity'] # MECHANICAL PROCESS
}
paper_new_production_proces_mapping = {
    'Low-enthalpy heat': ['Low-enthalpy heat', 'electricity'],  # HEAT PUMP!
    'Paper: Stock preparation': ['Paper: Stock preparation', 'electricity'], # HEAT PUMP!
    'Paper: Paper machine': ['Paper: Paper machine', 'electricity'], # HEAT PUMP!
    'Paper: Product finishing': ['Paper: Product finishing', 'electricity'] # HEAT PUMP!
}
printing_new_production_proces_mapping = {
    'Low-enthalpy heat': ['Low-enthalpy heat', 'electricity'], # HEAT PUMP!
    'Printing and publishing': ['Printing and publishing', 'electricity'] # MECHANICAL PROCESS
}
textile_and_leather_new_production_process_mapping = {
    'Low-enthalpy heat': ['Low-enthalpy heat', 'electricity'], # HEAT PUMP!
    'Textiles: Pretreatment with steam': ['Textiles: Pretreatment with steam', 'renew_bio'], # HEAT PUMP!
    'Textiles: Wet processing with steam': ['Textiles: Wet processing with steam', 'renew_bio'], # HEAT PUMP!
    'Textiles: Electric general machinery': ['Textiles: Electric general machinery', 'electricity'], # MECHANICAL PROCESS
    'Textiles: Drying': ['Textiles: Drying', 'electricity', 'Textiles: Electric drying'], # HEAT PUMP!
    'Textiles: Finishing Electric': ['Textiles: Finishing Electric', 'electricity'] # CONSIDERED AT LEAST PARTLY A MECHANICAL PROCESS
}
ceramics_and_other_non_metalic_minerals_new_production_process_mapping = {
    'Low-enthalpy heat': ['Low-enthalpy heat', 'electricity'], # HEAT PUMP!
    'Ceramics: Mixing of raw material': ['Ceramics: Mixing of raw material', 'electricity'], # MECHANICAL PROCESS
    'Ceramics: Drying and sintering of raw material': ['Ceramics: Drying and sintering of raw material', 'electricity'],
    'Ceramics: Primary production process': ['Ceramics: Primary production process', 'electricity'],
    'Ceramics: Product finishing': ['Ceramics: Product finishing', 'electricity'] # HEAT PUMP!
}
primary_steel_new_finishing_and_rolling = {
    'Steel: Furnaces, refining and rolling': ['Steel: Furnaces, refining and rolling', 'electricity'],
    'Steel: Product finishing': ['Steel: Product finishing', 'electricity']
}
secondary_steel_new_finishing_and_rolling = {
    'Steel: Furnaces, refining and rolling': ['Steel: Furnaces, refining and rolling', 'electricity'],
    'Steel: Product finishing': ['Steel: Product finishing', 'electricity']
}
other_chemicals_new = {
    'Low-enthalpy heat': ['Low-enthalpy heat', 'electricity'], # HEAT PUMP!
    'Chemicals: High-enthalpy heat processing': ['Chemicals: High-enthalpy heat processing', 'natural_gas'], # CAN HAVE VERY HIGH TEMPERATURE
    'Chemicals: Furnaces':['Chemicals: Furnaces', 'natural_gas'], # CAN HAVE VERY HIGH TEMPERATURE
    'Chemicals: Process cooling':['Chemicals: Process cooling', 'electricity'] # HEAT PUMP!
}
pharmaceuticals_new = {
    'Low-enthalpy heat': ['Low-enthalpy heat', 'electricity'], # HEAT PUMP!
    'Chemicals: High-enthalpy heat processing': ['Chemicals: High-enthalpy heat processing', 'natural_gas'], # CAN HAVE VERY HIGH TEMPERATURE
    'Chemicals: Furnaces':['Chemicals: Furnaces', 'natural_gas'], # CAN HAVE VERY HIGH TEMPERATURE
    'Chemicals: Process cooling':['Chemicals: Process cooling', 'electricity'] # HEAT PUMP!
}
transport_equipment_new = {
    'Low-enthalpy heat': ['Low-enthalpy heat', 'electricity'], # HEAT PUMP!
    'Trans. Eq.: Foundries': ['Trans. Eq.: Foundries', 'natural_gas'], # CAN HAVE VERY HIGH TEMPERATURE
    'Trans. Eq.: Connection techniques': ['Trans. Eq.: Connection techniques', 'electricity'],
    'Trans. Eq.: Heat treatment': [ 'Trans. Eq.: Heat treatment', 'electricity'],
    'Trans. Eq.: Steam processing': ['Trans. Eq.: Steam processing', 'electricity'], # HEAT PUMP!
    'Trans. Eq.: General machinery': ['Trans. Eq.: General machinery', 'electricity'], # MECHANICAL PROCESS
    'Trans. Eq.: Product finishing': ['Trans. Eq.: Product finishing', 'electricity'] # AT LEAST PARTLY MECHANICAL PROCESS
}
machinery_equipment_new = {
    'Low-enthalpy heat': ['Low-enthalpy heat', 'electricity'], # HEAT PUMP!
    'Mach. Eq.: Foundries': ['Mach. Eq.: Foundries', 'natural_gas'], # CAN HAVE VERY HIGH TEMPERATURE
    'Mach. Eq.: Connection techniques': ['Mach. Eq.: Connection techniques', 'electricity'],
    'Mach. Eq.: Heat treatment': ['Mach. Eq.: Heat treatment', 'electricity'],
    'Mach. Eq.: Steam processing': ['Mach. Eq.: Heat treatment', 'electricity'], # HEAT PUMP!
    'Mach. Eq.: General machinery': ['Mach. Eq.: General machinery', 'electricity'], # MECHANICAL PROCESS
    'Mach. Eq.: Product finishing': ['Mach. Eq.: Product finishing', 'electricity'] # AT LEAST PARTLY MECHANICAL PROCESS
}
wood_and_wood_products_new = {
    'Low-enthalpy heat': ['Low-enthalpy heat', 'electricity'], # HEAT PUMP!
    'Wood: Specific processes with steam': ['Wood: Specific processes with steam', 'electricity'], # HEAT PUMP! (mostly low temperature steam)
    'Wood: Electric mechanical processes': ['Wood: Electric mechanical processes', 'electricity'], # MECHANICAL PROCESS
    'Wood: Drying': ['Wood: Drying', 'electricity', 'Wood: Electric drying'], # HEAT PUMP!
    'Wood: Finishing Electric': ['Wood: Finishing Electric', 'electricity'] # MECHANICAL PROCESS
}
other_industrial_sectors_new = {
    'Low-enthalpy heat': ['Low-enthalpy heat', 'electricity'], # HEAT PUMP!
    'Other Industrial sectors: Steam processing': ['Other Industrial sectors: Process heating', 'electricity'], # efficiency of process heating!
    'Other Industrial sectors: Process heating': ['Other Industrial sectors: Process heating', 'electricity'],
    'Other Industrial sectors: Drying': ['Other Industrial sectors: Drying', 'electricity'],  # HEAT PUMP!
    'Other Industrial sectors: Process Cooling': ['Other Industrial sectors: Process Cooling', 'electricity'],  # HEAT PUMP!
    'Other Industrial sectors: Diesel motors (incl. biofuels)': ['Other Industrial sectors: Electric machinery', 'electricity'], # MECHANICAL PROCESS # efficiency of other industrial sectors: electric machinery
    'Other Industrial sectors: Electric machinery': ['Other Industrial sectors: Electric machinery', 'electricity'] # MECHANICAL PROCESS
}


new_production_proces_mapping = {
    'Alumina': alumina_new_production_proces_mapping,
    'Aluminium_primary': aluminium_primary_new_production_proces_mapping,
    'Aluminium_secondary': aluminium_secondary_new_production_proces_mapping,
    'Other_non_ferrous': other_non_ferrous_metals_new_production_proces_mapping,
    'Food_beverages_and_tobacco': food_beverages_and_tobacco_new_production_proces_mapping,
    'Pulp': pulp_new_production_proces_mapping,
    'Paper': paper_new_production_proces_mapping,
    'Printing_and_media': printing_new_production_proces_mapping,
    'Textile_and_leather': textile_and_leather_new_production_process_mapping,
    'Ceramics_and_other_non_metalic_minerals': ceramics_and_other_non_metalic_minerals_new_production_process_mapping,
    "Integrated_steelworks": primary_steel_new_finishing_and_rolling,
    "Electric_arc": secondary_steel_new_finishing_and_rolling,
    "transport_equipment": transport_equipment_new,
    "machinery_equipment": machinery_equipment_new,
    "wood_and_wood_products": wood_and_wood_products_new,
    "other_industrial_sectors": other_industrial_sectors_new,
    "Other_chemicals": other_chemicals_new,
    "Pharmaceutical_products": pharmaceuticals_new,
}



heat_pump_processes = {
    'Food: Specific process heat': ['Food: Specific process heat', 'electricity', 'Food: Process Heat - Electric'], # HEAT PUMP!
    'Food: Drying': ['Food: Drying', 'electricity', 'Food: Electric drying'], # HEAT PUMP!
    'Food: Process cooling and refrigeration': ['Food: Process cooling and refrigeration', 'electricity', 'Food: Electric cooling'], # HEAT PUMP!
    'Paper: Stock preparation': ['Paper: Stock preparation', 'electricity'], # HEAT PUMP!
    'Paper: Paper machine': ['Paper: Paper machine', 'electricity'], # HEAT PUMP!
    'Paper: Product finishing': ['Paper: Product finishing', 'electricity'], # HEAT PUMP!
    'Textiles: Pretreatment with steam': ['Textiles: Pretreatment with steam', 'renew_bio'], # HEAT PUMP!
    'Textiles: Wet processing with steam': ['Textiles: Wet processing with steam', 'renew_bio'], # HEAT PUMP!
    'Textiles: Drying': ['Textiles: Drying', 'electricity', 'Textiles: Electric drying'], # HEAT PUMP!
    'Ceramics: Product finishing': ['Ceramics: Product finishing', 'electricity'], # HEAT PUMP!
    'Chemicals: Process cooling':['Chemicals: Process cooling', 'electricity'], # HEAT PUMP!
    'Trans. Eq.: Steam processing': ['Trans. Eq.: Steam processing', 'electricity'], # HEAT PUMP!
    'Mach. Eq.: Steam processing': ['Mach. Eq.: Heat treatment', 'electricity'], # HEAT PUMP!
    'Wood: Drying': ['Wood: Drying', 'electricity', 'Wood: Electric drying'], # HEAT PUMP!
    'Low-enthalpy heat': ['Low-enthalpy heat', 'electricity'], # HEAT PUMP!
    'Other Industrial sectors: Drying': ['Other Industrial sectors: Drying', 'electricity'],  # HEAT PUMP!
    'Other Industrial sectors: Process Cooling': ['Other Industrial sectors: Process Cooling', 'electricity'],  # HEAT PUMP!
    'Wood: Specific processes with steam': ['Wood: Specific processes with steam', 'electricity'] # HEAT PUMP! (mostly low temperature steam)
}



alumina_original_production_proces_mapping = {
    'Alumina production: High-enthalpy heat': ['steam', 'natural_gas'],
    'Low-enthalpy heat': ['heat', 'electricity'],
}
aluminium_primary_original_production_proces_mapping = {
    'Aluminium finishing': ['steam', 'natural_gas', 'Aluminium finishing - Steam'],
    'Low-enthalpy heat': ['heat', 'electricity']
}
aluminium_secondary_original_production_proces_mapping = {
    'Aluminium finishing': ['steam', 'natural_gas', 'Aluminium finishing - Steam'],
    'Low-enthalpy heat': ['heat', 'electricity']
}
other_non_ferrous_metals_original_production_proces_mapping = {
    'Metal finishing': ['steam', 'natural_gas', 'Metal finishing - Steam'],
    'Low-enthalpy heat': ['heat', 'electricity']
}
ceramics_and_other_non_metalic_minerals_original_production_process_mapping = {
    'Low-enthalpy heat': ['heat', 'electricity'],
    'Ceramics: Drying and sintering of raw material': ['steam', 'natural_gas', 'Ceramics: Steam drying and sintering']
}
pulp_original_production_proces_mapping = {
    'Pulp: Pulping': ['heat', 'natural_gas'],
    'Low-enthalpy heat': ['heat', 'electricity'],
}
paper_original_production_proces_mapping = {
    'Low-enthalpy heat': ['heat', 'electricity'],
    'Paper: Stock preparation': ['steam', 'natural_gas'],
    'Paper: Paper machine': ['steam', 'natural_gas'],
    'Paper: Product finishing': ['steam', 'natural_gas']
}
printing_original_production_proces_mapping = {
    'Low-enthalpy heat': ['heat', 'electricity'],
}
food_beverages_and_tobacco_original_production_proces_mapping = {
    'Low-enthalpy heat': ['heat', 'electricity'],
    'Food: Drying': ['steam', 'natural_gas', 'Food: Steam drying'],
    'Food: Steam processing': ['steam', 'natural_gas'],
    'Food: Process cooling and refrigeration': ['steam', 'natural_gas', 'Food: Steam cooling']
}
textile_and_leather_original_production_process_mapping = {
    'Low-enthalpy heat': ['heat', 'electricity'],
    'Textiles: Pretreatment with steam': ['steam', 'natural_gas'],
    'Textiles: Wet processing with steam': ['steam', 'natural_gas'],
    'Textiles: Drying': ['steam', 'natural_gas', 'Textiles: Steam drying'],
}
primary_steel_original_finishing_and_rolling = {
    'Steel: Product finishing': ['steam', 'natural_gas', 'Steel: Product finishing - Steam']
}
secondary_steel_original_finishing_and_rolling = {
    'Steel: Product finishing': ['steam', 'natural_gas', 'Steel: Product finishing - Steam']
}
other_chemicals_original = {
    'Low-enthalpy heat': ['heat', 'electricity'],
    'Chemicals: High-enthalpy heat processing': ['steam', 'natural_gas'],
    'Chemicals: Process cooling': ['steam', 'electricity']
}
pharmaceuticals_original = {
    'Low-enthalpy heat': ['heat', 'electricity'],
    'Chemicals: High-enthalpy heat processing': ['steam', 'natural_gas'],
    'Chemicals: Process cooling': ['steam', 'electricity']
}
transport_equipment_original = {
    'Low-enthalpy heat': ['heat', 'electricity'],
    'Trans. Eq.: Steam processing': ['steam', 'natural_gas']
}
machinery_equipment_original = {
    'Low-enthalpy heat': ['heat', 'electricity'],
    'Mach. Eq.: Steam processing': ['steam', 'natural_gas']
}
wood_and_wood_products_original = {
    'Low-enthalpy heat': ['heat', 'electricity'],
    'Wood: Specific processes with steam': ['steam', 'natural_gas'],
    'Wood: Drying': ['steam', 'natural_gas', 'Wood: Steam drying']
}
other_industrial_sectors_original = {
    'Low-enthalpy heat': ['heat', 'electricity'],
    'Other Industrial sectors: Steam processing': ['steam', 'natural_gas'],
    'Other Industrial sectors: Drying': ['steam', 'natural_gas', 'Other Industries: Steam drying']
}

original_production_proces_mapping = {
    'Alumina': alumina_original_production_proces_mapping,
    'Aluminium_primary': aluminium_primary_original_production_proces_mapping,
    'Aluminium_secondary': aluminium_secondary_original_production_proces_mapping,
    'Other_non_ferrous': other_non_ferrous_metals_original_production_proces_mapping,
    'Food_beverages_and_tobacco': food_beverages_and_tobacco_original_production_proces_mapping,
    'Pulp': pulp_original_production_proces_mapping,
    'Paper': paper_original_production_proces_mapping,
    'Printing_and_media': printing_original_production_proces_mapping,
    'Textile_and_leather': textile_and_leather_original_production_process_mapping,
    'Ceramics_and_other_non_metalic_minerals': ceramics_and_other_non_metalic_minerals_original_production_process_mapping,
    "Integrated_steelworks": primary_steel_original_finishing_and_rolling,
    "Electric_arc": secondary_steel_original_finishing_and_rolling,
    "transport_equipment": transport_equipment_original,
    "machinery_equipment": machinery_equipment_original,
    "wood_and_wood_products": wood_and_wood_products_original,
    "other_industrial_sectors": other_industrial_sectors_original,
    "Pharmaceutical_products": pharmaceuticals_original,
    "Other_chemicals": other_chemicals_original
}
