import pandas as pd
from pathlib import Path
import os
import numpy as np
from typing import Dict, List, Tuple, Optional

def filter_jrc_idees(
        folder: str,
        line_map: dict,
        product_map: dict,
        parameter_map: dict,
        year: int | str,
        products: tuple,
        unit_map: dict
) -> pd.DataFrame:

    records: list[dict] = []

    for file in Path(folder).glob("*.xlsx"):
        with pd.ExcelFile(file, engine="openpyxl") as xls:
            for product in products:
                sheet = product_map[product]
                df = xls.parse(sheet_name=sheet, header=0)

                record = {
                    "sector": product_map[product],
                    "country_code": file.stem[-2:],
                    "product": product,
                    "year": year,
                    "unit": unit_map[product]
                }

                for row_idx in line_map[product]:
                    value = df.iat[row_idx, df.columns.get_loc(year)]
                    record[parameter_map[line_map[product].index(row_idx) + 1]] = value

                records.append(record)

    return pd.DataFrame.from_records(
        records)

def filter_jrc_idees_detailed(
        folder: str,
        energy_map: dict,
        product_map: dict,
        parameter_map: dict,
        year: int | str,
        products: tuple,
        unit_map: dict,
        tab_extension: str,
        products_with_proces_emissions_list:list,
        ktoe_to_TJ_conv: float
) -> pd.DataFrame:

    rows = []
    header = parameter_map[1]

    # There is an extra row for emissions compared to energy use (proces emissions)
    if tab_extension == 'emi':
        for k, v in energy_map.items():
            if k in products_with_proces_emissions_list:
                new_key = max(v.keys()) + 1
                v[new_key] = 3

    for file in Path(folder).glob("*.xlsx"):

        with pd.ExcelFile(file, engine="openpyxl") as xls:
            for product in products:
                sheet = product_map[product] + "_" + tab_extension
                df = xls.parse(sheet_name=sheet, header=0)
                df['level'] = 0

                s = pd.Series(energy_map[product])
                df['level'] = df.index.map(s)

                df = df[~df['level'].isna()]
                df = df.set_index(df.columns[0])
                df = df[[year, 'level']]
                df = df.reset_index()
                pre_level_2 = None
                pre_level_3 = None

                for i in range(len(df)):
                    current = df.iloc[i]
                    current_level = int(current["level"])
                    next_level = int(df.iloc[i + 1]["level"]) if i + 1 < len(df) else None

                    if tab_extension == 'fec' or tab_extension == 'ued':
                        value = df.iat[i, df.columns.get_loc(year)] * ktoe_to_TJ_conv
                    else:
                        value = df.iat[i, df.columns.get_loc(year)]

                    new_data_row = {
                        "country_code": file.stem[-2:],
                        "sector": product_map[product],
                        "product": product,
                        header: value,
                        "year": year,
                        "unit": unit_map[product]
                    }

                    if current_level == 3:
                        if next_level == 1:
                            pre_level_3 = current.iloc[0]
                            pre_level_2 = None
                        elif next_level == 2:
                            pre_level_3 = current.iloc[0]
                        elif next_level == 3 or next_level is None:
                            new_data_row["classification_1"] = current.iloc[0]
                            new_data_row["classification_2"] = None
                            new_data_row["energy_carrier_jrc_idees"] = None

                            rows.append(new_data_row)

                    elif current_level == 2:
                        if next_level == 1:
                            pre_level_2 = current.iloc[0]
                        elif next_level in (2, 3) or next_level is None:
                            new_data_row["classification_1"] = pre_level_3
                            new_data_row["classification_2"] = current.iloc[0]
                            new_data_row["energy_carrier_jrc_idees"] = None

                            rows.append(new_data_row)

                    elif current_level == 1:
                        new_data_row["classification_1"] = pre_level_3
                        new_data_row["classification_2"] = pre_level_2
                        new_data_row["energy_carrier_jrc_idees"] = current.iloc[0]

                        rows.append(new_data_row)

    out_df = pd.DataFrame(rows)

    return out_df

def fill_energy_carrier_EB_column(df, jrc_energy_carrier_map, classification_1_map, classification_2_map):
    df["energy_carrier_EB"] = df["energy_carrier_jrc_idees"].map(
        jrc_energy_carrier_map)

    df["energy_carrier_EB"] = df["energy_carrier_EB"].fillna(
        df["classification_2"].map(classification_2_map)
    )

    df["energy_carrier_EB"] = df["energy_carrier_EB"].fillna(
        df["classification_1"].map(classification_1_map)
    )


    return df


def create_new_production_proces(df, mapping_new_processes, heat_pump_list):
    for i in df['country_code'].drop_duplicates().tolist():
        for k1, v1 in mapping_new_processes.items():
            for k2, v2 in v1.items():

                if k2 in heat_pump_list:
                    new_efficiency = 2.85 # average of technology catalogue
                    new_CO2_intensity = 0
                    new_energy_carrier_EB = 'electricity-heat-pump'
                else:
                    row_filter = ((df['classification_1'] == v2[0]) &
                                  (df['energy_carrier_EB'] == v2[1]) &
                                  (df['country_code'] == i) &
                                  (df['product'] == k1))
                    if len(v2) == 3:
                        row_filter = row_filter & (df['classification_2'] == v2[2])

                    new_efficiency = df.loc[row_filter, 'efficiency_(%)'].iloc[0]
                    new_CO2_intensity = df.loc[row_filter, 'CO2_intensity_(kt/TJ)'].iloc[0]
                    new_energy_carrier_EB = df.loc[row_filter, 'energy_carrier_EB'].iloc[0]

                if k2 == 'Ceramics: Drying and sintering of raw material':
                    new_efficiency = 11.6/26
                    new_CO2_intensity = 0

                if k2 in heat_pump_list:
                    data_to_replace_filter = ((df['classification_1'] == k2) &
                                              (df['country_code'] == i) &
                                              (df['product'] == k1))
                else:
                    data_to_replace_filter = ((df['classification_1'] == k2) &
                                              ~((df['energy_carrier_EB'] == v2[1]) | (df['energy_carrier_EB'] == 'electricity')) &
                                              (df['country_code'] == i) &
                                              (df['product'] == k1))

                df.loc[data_to_replace_filter, 'new_efficiency_(%)'] = new_efficiency
                df.loc[data_to_replace_filter, 'new_CO2_intensity_(kt/TJ)'] = new_CO2_intensity
                df.loc[data_to_replace_filter, 'new_energy_carrier_EB'] = new_energy_carrier_EB

                if k2 in heat_pump_list:
                    df.loc[data_to_replace_filter, 'new proces'] = 'yes, heat pump'
                else:
                    df.loc[data_to_replace_filter, 'new proces'] = 'yes'


                df.loc[df['new_efficiency_(%)'].isna(), 'new_efficiency_(%)'] = df['efficiency_(%)']
                df.loc[df['new_CO2_intensity_(kt/TJ)'].isna(), 'new_CO2_intensity_(kt/TJ)'] = df['CO2_intensity_(kt/TJ)']
                df.loc[df['new_energy_carrier_EB'].isna(), 'new_energy_carrier_EB'] = df['energy_carrier_EB']
                df.loc[df['new proces'].isna(), 'new proces'] = 'no'

                df['new_CO2_emissions_(kt)'] = df['useful_energy_(TJ)'] * df['new_CO2_intensity_(kt/TJ)']
                df.loc[df['new_CO2_emissions_(kt)'].isna(), 'new_CO2_emissions_(kt)'] = df['CO2_emissions_(kt)'] # Needed for proces emissions!

                df['new_energy_use_(TJ)'] = df['useful_energy_(TJ)'] / df['new_efficiency_(%)']

    return df


def replace_production_by_energy_use(product_list: list,
                                     production_df,
                                     energy_use_df,
                                     energy_column_title: str):

    for cc in production_df['country_code'].drop_duplicates():
        for product in product_list:
            production_df.loc[
                (production_df['product'] == product) & (production_df['country_code'] == cc), 'unit'] = 'TJ'

            production_df.loc[
                (production_df['product'] == product) & (production_df['country_code'] == cc), 'actual_capacity'] = (
                energy_use_df.loc[(energy_use_df['product'] == product) & (
                            energy_use_df['country_code'] == cc), energy_column_title].iloc[0])

    return production_df


def useful_energy_per_capacity(product_list: list,
                                     production_df,
                                     energy_use_df,
                                     energy_column_title: str):
    energy_per_capacity = production_df.copy()

    for cc in production_df['country_code'].drop_duplicates():
        for product in product_list:
           energy_per_capacity.loc[
                (energy_per_capacity['product'] == product) & (energy_per_capacity['country_code'] == cc), 'unit'] = 'TJ/production_index'

           energy_per_capacity.loc[
               (energy_per_capacity['product'] == product) & (energy_per_capacity['country_code'] == cc), 'useful_energy'] = (
               energy_use_df.loc[(energy_use_df['product'] == product) & (
                       energy_use_df['country_code'] == cc), energy_column_title].iloc[0])

    energy_per_capacity = energy_per_capacity.dropna(subset=['useful_energy'])
    energy_per_capacity['useful_energy_per_capacity'] = energy_per_capacity['useful_energy']/energy_per_capacity['actual_capacity']

    energy_per_capacity_sum = energy_per_capacity.groupby(
            ['sector', 'product', 'year', 'unit'], as_index=False
        )['useful_energy_per_capacity'].mean()

    return energy_per_capacity, energy_per_capacity_sum


def update_original_production_proces(df, mapping_original_processes):
    for i in df['country_code'].drop_duplicates().tolist():
        for k1, v1 in mapping_original_processes.items():
            for k2, v2 in v1.items():
                row_filter = ((df['classification_1'] == k2) &
                              (df['energy_carrier_EB'] == v2[1]) &
                              (df['country_code'] == i) &
                              (df['product'] == k1))
                if len(v2) == 3:
                    row_filter = row_filter & (df['classification_2'] == v2[2])

                new_efficiency = df.loc[row_filter, 'efficiency_(%)'].iloc[0]
                new_CO2_intensity = df.loc[row_filter, 'CO2_intensity_(kt/TJ)'].iloc[0]
                new_energy_carrier_jrc = df.loc[row_filter, 'energy_carrier_EB'].iloc[0]

                data_to_replace_filter = ((df['classification_1'] == k2) &
                                          (df['energy_carrier_EB'] == v2[0]) &
                                          (df['country_code'] == i) &
                                          (df['product'] == k1))

                df.loc[data_to_replace_filter, 'efficiency_(%)'] = new_efficiency
                df.loc[data_to_replace_filter, 'CO2_intensity_(kt/TJ)'] = new_CO2_intensity
                df.loc[data_to_replace_filter, 'energy_carrier_EB'] = new_energy_carrier_jrc

                df.loc[data_to_replace_filter, 'CO2_emissions_(kt)'] = (
                        df.loc[data_to_replace_filter, 'useful_energy_(TJ)'] *
                        df.loc[data_to_replace_filter, 'CO2_intensity_(kt/TJ)'])

                df.loc[data_to_replace_filter, 'energy_use_(TJ)'] = (
                        df.loc[data_to_replace_filter, 'useful_energy_(TJ)'] /
                        df.loc[data_to_replace_filter, 'efficiency_(%)'])

    return df



def build_tc_energy_use_tables(
    energy_df,
    production_df,
    energy_col,                 # 'energy_use_(TJ)' or 'new_energy_use_(TJ)'
    carrier_col,                # 'energy_carrier_EB' or 'new_energy_carrier_EB'
    scenario_suffix,            # '-reference' or '-alternative'
    final_year_map,             # e.g., {'2018': 'mean'} or {'2025': 'mean', '2030': 'copy', '2040': 'copy', '2050': 'copy'}
    sector_mapping_tc=None,
    product_mapping_tc=None,
    industry_mapping_tc=None,
    filter_jrc_sectors=None,
    mapping_energy_tc=None,
    energy_carrier_mapping_tc=None
):
    import pandas as pd

    df = energy_df.merge(
        production_df,
        on=['sector', 'country_code', 'product', 'year'],
        how='left'
    ).copy()

    # normalize energy use per capacity
    df['energy_use'] = df[energy_col] / df['actual_capacity']
    df['unit_energy_use'] = 'TJ/' + df['unit']

    df = df[['country_code', 'sector', 'product', 'year', carrier_col, 'energy_use', 'unit_energy_use', 'actual_capacity']]

    df['sector_id'] = df['sector'].replace(sector_mapping_tc)
    df['to_node'] = df['product'].replace(product_mapping_tc)
    df['Industry'] = df['product'].replace(industry_mapping_tc)

    df = df[df['Industry'].isin(filter_jrc_sectors)]

    df = df.merge(mapping_energy_tc, on="unit_energy_use", how="left")
    df['energy_use_converted'] = df['energy_use'] * df['conversion']

    df['energy_carrier_tc'] = df[carrier_col].replace(energy_carrier_mapping_tc)

    df['Industry'] = df['Industry'] + scenario_suffix

    df_capex_opex_cst = df.copy()
    df_capex_opex_cst = df_capex_opex_cst.rename(columns={'new_energy_carrier_EB':'energy_carrier_EB'})
    df_capex_opex_cst = df_capex_opex_cst[['country_code', 'sector_id', 'to_node', 'Industry',
                                           'unit_energy_use_converted', 'energy_use_converted',
                                           'energy_carrier_tc', 'energy_carrier_EB']]

    # Keep a verbose “out” view if needed
    df_out = df[['country_code', 'sector_id', 'to_node', 'Industry',
                 'energy_carrier_tc', carrier_col, 'energy_use', 'unit_energy_use',
                 'energy_use_converted', 'unit_energy_use_converted', 'conversion']].copy()

    # country-level sums per (sector/to_node/industry/carrier/unit)
    out_sum = df_out.groupby(
        ['country_code', 'sector_id', 'to_node', 'Industry', 'energy_carrier_tc', 'unit_energy_use_converted'],
        as_index=False
    )['energy_use_converted'].sum()

    # total per country (to drop all-zero country-Industry (= production process) combinations)
    country_totals = (out_sum.groupby(['country_code', 'Industry'], as_index=False)['energy_use_converted']
                      .sum()
                      .rename(columns={'energy_use_converted': 'energy_use_converted_sum'}))

    out_sum = out_sum.merge(country_totals, on=['country_code', 'Industry'], how='left')

    out_sum = out_sum[out_sum['energy_use_converted_sum'] != 0]

    # mean/std across countries to get a single row per country
    simplified_mean = out_sum.groupby(
        ['sector_id', 'to_node', 'Industry', 'energy_carrier_tc', 'unit_energy_use_converted'],
        as_index=False
    )['energy_use_converted'].mean()

    simplified_std = out_sum.groupby(
        ['sector_id', 'to_node', 'Industry', 'energy_carrier_tc', 'unit_energy_use_converted'],
        as_index=False
    )['energy_use_converted'].std().rename(columns={'energy_use_converted': 'std'})

    simplified = simplified_mean.merge(
        simplified_std,
        on=['sector_id', 'to_node', 'Industry', 'energy_carrier_tc', 'unit_energy_use_converted'],
        how='left'
    ).rename(columns={
        'unit_energy_use_converted': 'unit',
        'energy_carrier_tc': 'from_node'
    })

    # Year column assignment
    # The ‘mean’ key in final_year_map means compute from energy_use_converted;
    # The ‘copy’ key means duplicate from the first provided ‘mean’ year.
    # Find the first year that requests 'mean' (source column)
    mean_years = [y for y, mode in final_year_map.items() if mode == 'mean']

    if not mean_years:
        raise ValueError("final_year_map must include at least one 'mean' target year")
    source_year = mean_years[0]

    simplified = simplified.rename(columns={'energy_use_converted': source_year})

    # Copy to other years as requested
    for y, mode in final_year_map.items():
        if y == source_year:
            continue
        if mode == 'copy':
            simplified[y] = simplified[source_year]
        elif mode == 'mean':
            # already assigned above; ignore
            pass
        else:
            raise ValueError(f"Unknown mode '{mode}' for year '{y}'")

    return df_out, out_sum, simplified, df_capex_opex_cst


def build_tc_production_co2_and_lifetime_tables(
    energy_co2_df: pd.DataFrame,
    production_df: pd.DataFrame,
    *,
    # required differences between "original" vs "new"
    co2_col: str,                      # e.g., 'CO2_emissions_(kt)' or 'new_CO2_emissions_(kt)'
    industry_suffix: str,              # e.g., '-reference' or '-alternative'

    # mappings & filters
    sector_mapping_tc: Dict,
    product_mapping_tc: Dict,
    industry_mapping_tc: Dict,
    filter_jrc_sectors: List[str],
    mapping_production_tc: pd.DataFrame,   # expects: ['unit_capacity','conversion_production','production_unit_converted']
    mapping_CO2_tc: pd.DataFrame,          # expects: ['unit_CO2_emissions_per_capacity','conversion_co2_emissions','co2_emissions_per_capacity_unit_converted']

    # how to label/copy year columns in outputs
    prod_year_base: str,               # e.g., '2018' or '2030'
    prod_year_copy_to: Optional[List[str]] = None,   # e.g., ['2050']
    emis_year_base: str = '2018',      # e.g., '2018' or '2025'
    emis_year_copy_to: Optional[List[str]] = None,   # e.g., ['2030','2040','2050']

    # merge keys
    merge_keys: Tuple[str, ...] = ('sector', 'country_code', 'product', 'year'),

) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Build technology-catalogue-ready tables for production capacity and CO₂ emissions per capacity.

    Returns:
        production_out, emissions_simplified_out, lifetime_out

    Expects:
        - energy_co2_df has columns: merge_keys + ['unit', co2_col]
        - production_df has columns: merge_keys + ['actual_capacity']
        - mapping_production_tc has: ['unit_capacity','conversion_production','production_unit_converted']
        - mapping_CO2_tc has: ['unit_CO2_emissions_per_capacity','conversion_co2_emissions',
                               'co2_emissions_per_capacity_unit_converted']
    """

    df = energy_co2_df.merge(production_df, on=list(merge_keys), how='left').copy()

    # ---- computations and mappings
    # Avoid division by zero
    denom = df['actual_capacity'].replace({0: pd.NA})
    df['CO2_emissions_per_capacity'] = df[co2_col] / denom
    df['unit_CO2_emissions_per_capacity'] = 'ktco2/' + df['unit'].astype(str)

    df['sector_id'] = df['sector'].replace(sector_mapping_tc)
    df['to_node'] = df['product'].replace(product_mapping_tc)
    df['Industry'] = df['product'].replace(industry_mapping_tc)

    # Filter to selected industries
    df = df[df['Industry'].isin(filter_jrc_sectors)].copy()

    # Convert units for production
    df = df.rename(columns={'unit': 'unit_capacity'})
    df = df.merge(mapping_production_tc, on='unit_capacity', how='left')
    df['actual_capacity_converted'] = df['actual_capacity'] * df['conversion_production']

    # Convert units for CO2 per capacity
    df = df.merge(mapping_CO2_tc, on='unit_CO2_emissions_per_capacity', how='left')
    df['CO2_emissions_per_capacity_converted'] = (
        df['CO2_emissions_per_capacity'] * df['conversion_co2_emissions']
    )

    # Tag scenario & emission field
    df['Industry'] = df['Industry'] + industry_suffix
    df['emission'] = 'co2_emission'

    # ---- PRODUCTION OUTPUT
    production_out = df[
        ['country_code', 'sector_id', 'to_node', 'Industry',
         'actual_capacity', 'unit_capacity', 'conversion_production',
         'actual_capacity_converted', 'production_unit_converted']
    ].copy()

    # Rename for final shape & add year columns
    production_out = production_out.rename(columns={'production_unit_converted': 'unit'})
    production_out[prod_year_base] = production_out['actual_capacity_converted']
    for y in prod_year_copy_to:
        production_out[y] = production_out[prod_year_base]

    # ---- EMISSIONS OUTPUT (sum by country → mean & std by sector)
    emissions_out = df[
        ['country_code', 'sector_id', 'to_node', 'Industry',
         'CO2_emissions_per_capacity', 'unit_CO2_emissions_per_capacity',
         'conversion_co2_emissions', 'CO2_emissions_per_capacity_converted',
         'co2_emissions_per_capacity_unit_converted', 'emission']
    ].copy()

    lifetime_out = emissions_out.copy()

    emissions_sum = (
        df.copy().groupby(
            ['country_code', 'sector_id', 'to_node', 'Industry'],
            as_index=False
        )['actual_capacity'].sum()
    )

    emissions_out = emissions_out.merge(emissions_sum,
                                        on = ['country_code', 'sector_id', 'to_node', 'Industry'])

    # Drop zero totals
    emissions_out = emissions_out[
        emissions_out['actual_capacity'] != 0
    ].copy()

    emissions_mean = (
        emissions_out.groupby(
            ['sector_id', 'to_node', 'Industry',
             'co2_emissions_per_capacity_unit_converted', 'emission'],
            as_index=False
        )['CO2_emissions_per_capacity_converted'].mean()
    )

    emissions_std = (
        emissions_out.groupby(
            ['sector_id', 'to_node', 'Industry',
             'co2_emissions_per_capacity_unit_converted', 'emission'],
            as_index=False
        )['CO2_emissions_per_capacity_converted'].std()
        .rename(columns={'CO2_emissions_per_capacity_converted': 'std'})
    )

    emissions_simplified_out = pd.merge(
        emissions_mean, emissions_std,
        on=['sector_id', 'to_node', 'Industry',
            'co2_emissions_per_capacity_unit_converted', 'emission'],
        how='left'
    )

    emissions_simplified_out = emissions_simplified_out.rename(
        columns={
            'co2_emissions_per_capacity_unit_converted': 'unit',
            'CO2_emissions_per_capacity_converted': emis_year_base
        }
    )

    # Replicate into additional catalogue years if requested
    for y in emis_year_copy_to:
        emissions_simplified_out[y] = emissions_simplified_out[emis_year_base]

    # ---- LIFETIME OUTPUT (consistent with simplified groups)

    lifetime_out = lifetime_out.groupby(['sector_id', 'to_node', 'Industry'])['CO2_emissions_per_capacity_converted'].sum().reset_index()
    lifetime_out = lifetime_out[['sector_id','to_node', 'Industry']].drop_duplicates()

    lifetime_out['unit'] = 'yr'
    lifetime_out['life'] = 30

    # Housekeeping
    production_out = production_out.reset_index(drop=True)
    emissions_simplified_out = emissions_simplified_out.reset_index(drop=True)
    lifetime_out = lifetime_out.reset_index(drop=True)

    return production_out, emissions_simplified_out, lifetime_out

def build_steel_finishing_outputs(
    *,
    # Core inputs
    energy_use_df: pd.DataFrame,
    production_df: pd.DataFrame,

    # Column names that differ between NEW vs ORIGINAL
    energy_use_tj_col: str,          # e.g., 'new_energy_use_(TJ)' or 'energy_use_(TJ)'
    co2_emissions_kt_col: str,       # e.g., 'new_CO2_emissions_(kt)' or 'CO2_emissions_(kt)'
    energy_carrier_eb_col: str,      # e.g., 'new_energy_carrier_EB' or 'energy_carrier_EB'

    # Shared keys / columns (override if needed)
    sector_col: str = 'sector',
    country_code_col: str = 'country_code',
    product_col: str = 'product',
    year_col: str = 'year',
    unit_col: str = 'unit',
    actual_capacity_col: str = 'actual_capacity',
    classification_col: str = 'classification_1',

    # Mappings: dicts & tables (must match your existing schemas)
    sector_mapping_tc: dict = None,
    product_mapping_tc: dict = None,
    energy_carrier_mapping_tc: dict = None,
    mapping_energy_tc: pd.DataFrame = None,        # expects 'unit_energy_use'→'conversion','unit_energy_use_converted'
    mapping_production_tc: pd.DataFrame = None,    # expects 'unit_capacity'→'conversion_production'
    mapping_CO2_tc: pd.DataFrame = None,           # expects 'unit_CO2_emissions_per_capacity'→'conversion_co2_emissions','co2_emissions_per_capacity_unit_converted'

    # Energy output years
    energy_years: list,                     # e.g., ['2025', '2030', '2040', '2050'] or ['2018']
    energy_base_year: str,

    # CO2 output years (first entry treated as base; others get the same value, if provided)
    co2_years: list,                        # e.g., ['2025','2030','2040','2050'] or ['2018']
    co2_base_year: str,  # e.g., ['2025','2030','2040','2050'] or ['2018']

    ref_or_alt: str,

    lifetime_value: int = 40,
    lifetime_unit: str = 'yr'
):
    """
    Returns a dict with:
      - 'steel_finishing_out': filtered intermediate table (per country/product/classification)
      - 'energy_simplified'  : mean+std by (sector,to_node,Industry,classification,from_node,unit) + years
      - 'co2_simplified'     : mean+std by (sector,to_node,Industry,classification,unit) + years
      - 'lifetime_out'       : (sector_id,to_node,Industry,unit,life)
    """

    # Merge base data
    df = energy_use_df.merge(
        production_df,
        on=[sector_col, country_code_col, product_col, year_col],
        how='left'
    )

    # Derived metrics (safe divide to avoid inf/-inf)
    cap = df[actual_capacity_col].replace(0, np.nan)
    df['energy_use'] = df[energy_use_tj_col] / cap
    df['CO2_emissions_per_capacity'] = df[co2_emissions_kt_col] / cap

    # Units
    df['unit_energy_use'] = 'TJ/' + df[unit_col]
    df['unit_CO2_emissions_per_capacity'] = 'ktco2/' + df[unit_col]

    # Mappings: sector & product
    df['sector_id'] = df[sector_col].replace(sector_mapping_tc)
    df['to_node'] = df[product_col].replace(product_mapping_tc)

    # Energy conversion
    df = df.merge(mapping_energy_tc, on="unit_energy_use", how="left")
    df['energy_use_converted'] = df['energy_use'] * df['conversion']

    # Energy carrier mapping
    df['energy_carrier_tc'] = df[energy_carrier_eb_col].replace(energy_carrier_mapping_tc)

    # Production unit conversion
    df = df.rename(columns={unit_col: 'unit_capacity'})
    df = df.merge(mapping_production_tc, on='unit_capacity', how='left')
    df['actual_capacity_converted'] = df[actual_capacity_col] * df['conversion_production']

    # CO2 unit conversion
    df = df.merge(mapping_CO2_tc, on='unit_CO2_emissions_per_capacity', how='left')
    df['CO2_emissions_per_capacity_converted'] = df['CO2_emissions_per_capacity'] * df['conversion_co2_emissions']

    # Intermediate output (keep the source EB column that was provided)
    out_cols = [
        country_code_col, 'sector_id', 'to_node', 'energy_carrier_tc', energy_carrier_eb_col, classification_col,
        'energy_use', 'unit_energy_use', 'conversion', 'energy_use_converted', 'unit_energy_use_converted',
        'CO2_emissions_per_capacity', 'unit_CO2_emissions_per_capacity', 'conversion_co2_emissions',
        'CO2_emissions_per_capacity_converted', 'co2_emissions_per_capacity_unit_converted',
        'new_efficiency_(%)', 'efficiency_(%)'
    ]
    steel_finishing_out = df[out_cols].copy()

    # Filter relevant classifications
    steel_finishing_out = steel_finishing_out[
        (steel_finishing_out[classification_col] == 'Steel: Product finishing') |
        (steel_finishing_out[classification_col] == 'Steel: Furnaces, refining and rolling')
    ]

    # Industry labels
    is_prod_finish = steel_finishing_out[classification_col] == 'Steel: Product finishing'
    is_furn_ref_roll = steel_finishing_out[classification_col] == 'Steel: Furnaces, refining and rolling'
    is_eaf = steel_finishing_out['to_node'] == 'electric-arc-steel'
    is_isw = steel_finishing_out['to_node'] == 'integrated-steelworks-steel'

    steel_finishing_out.loc[is_prod_finish & is_eaf, 'Industry'] = 'steel-electric-arc-finishing-' + ref_or_alt
    steel_finishing_out.loc[is_furn_ref_roll & is_eaf, 'Industry'] = 'steel-electric-arc-rolling-' + ref_or_alt
    steel_finishing_out.loc[is_prod_finish & is_isw, 'Industry'] = 'steel-integrated-steelworks-finishing-' + ref_or_alt
    steel_finishing_out.loc[is_furn_ref_roll & is_isw, 'Industry'] = 'steel-integrated-steelworks-rolling-' + ref_or_alt

    # Energy: sum per country to drop zero rows
    energy_sum = steel_finishing_out.groupby([country_code_col,'to_node'])['energy_use_converted'].sum().reset_index()
    energy_sum = energy_sum.rename(columns={'energy_use_converted': 'energy_use_sum_per_country'})
    steel_finishing_out = steel_finishing_out.merge(energy_sum, on=[country_code_col, 'to_node'], how='left')
    steel_finishing_out = steel_finishing_out[steel_finishing_out['energy_use_sum_per_country'] != 0]

    # Energy simplified: mean + std
    grp_energy = ['sector_id','to_node', 'Industry', classification_col, 'energy_carrier_tc', 'unit_energy_use_converted']
    steel_finishing_out_energy = steel_finishing_out.groupby(grp_energy+['country_code'])['energy_use_converted'].sum().reset_index()
    energy_mean = steel_finishing_out_energy.groupby(grp_energy)['energy_use_converted'].mean().reset_index()
    energy_std  = steel_finishing_out_energy.groupby(grp_energy)['energy_use_converted'].std().reset_index().rename(columns={'energy_use_converted': 'std'})
    energy_simplified = energy_mean.merge(energy_std, on=grp_energy, how='left')
    energy_simplified = energy_simplified.rename(columns={
        'energy_carrier_tc': 'from_node',
        'unit_energy_use_converted': 'unit',
        'energy_use_converted': energy_base_year
    })

    # Fill all requested energy years with the base value
    if len(energy_years) > 1:
        for y in energy_years:
            energy_simplified[y] = energy_simplified[energy_base_year]

    # CO2 simplified: sum per country → filter → mean + std (excluding country)
    grp_co2_country = [country_code_col, 'sector_id','to_node', 'Industry', classification_col, 'co2_emissions_per_capacity_unit_converted']
    co2_sum = steel_finishing_out.groupby(grp_co2_country)['CO2_emissions_per_capacity_converted'].sum().reset_index()

    grp_co2 = ['sector_id','to_node', 'Industry', classification_col, 'co2_emissions_per_capacity_unit_converted']
    co2_mean = co2_sum.groupby(grp_co2)['CO2_emissions_per_capacity_converted'].mean().reset_index()
    co2_std  = co2_sum.groupby(grp_co2)['CO2_emissions_per_capacity_converted'].std().reset_index().rename(columns={'CO2_emissions_per_capacity_converted': 'std'})
    co2_simplified = co2_mean.merge(co2_std, on=grp_co2, how='left')
    co2_simplified = co2_simplified.rename(columns={
        'co2_emissions_per_capacity_unit_converted': 'unit',
        'CO2_emissions_per_capacity_converted': co2_base_year
    })
    co2_simplified['emission'] = 'co2_emission'


    # Fill all requested co2 years with the base value
    if len(co2_years) > 1:
        for y in co2_years:
            co2_simplified[y] = co2_simplified[co2_base_year]

    # Lifetime
    tmp = steel_finishing_out.groupby(grp_co2_country)['CO2_emissions_per_capacity_converted'].sum().reset_index()
    tmp2 = tmp.groupby(grp_co2)['CO2_emissions_per_capacity_converted'].mean().reset_index()
    lifetime_out = tmp2[['sector_id','to_node', 'Industry']].drop_duplicates()

    lifetime_out['unit'] = lifetime_unit
    lifetime_out['life'] = lifetime_value

    return {
        'steel_finishing_out': steel_finishing_out,
        'energy_simplified': energy_simplified,
        'co2_simplified': co2_simplified,
        'lifetime_out': lifetime_out
    }