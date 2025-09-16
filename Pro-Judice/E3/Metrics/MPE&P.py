#!/usr/bin/env python3
"""
T-test Analysis for E3 Experiment MPE (Mean Procedure Effect)
Calculates MPE as |E_3_2 - E_3_1| for each case, then computes group differences
Author: Assistant
Date: 2025
"""

import pandas as pd
import numpy as np
from scipy import stats
import os
import warnings

warnings.filterwarnings('ignore')


def load_and_clean_data(file_path):
    """Load Excel file and extract clean numeric data"""
    try:
        df = pd.read_excel(file_path)
        if 'answerValue' not in df.columns:
            return pd.DataFrame()

        # Clean the data thoroughly
        df['answerValue'] = pd.to_numeric(df['answerValue'], errors='coerce')
        df = df.dropna(subset=['answerValue'])
        df = df[np.isfinite(df['answerValue'])]
        df = df[df['answerValue'] >= 0]

        return df
    except Exception as e:
        return pd.DataFrame()


def load_all_data():
    """Load all data files and organize them"""
    all_data = []

    file_mapping = {
        'deepseek_r1': 'results_deepseek-r1.xlsx',
        'deepseek_v3': 'results_deepseek-v3.xlsx',
        'gpt_4o': 'results_gpt-4o.xlsx',
        'llama_3_3': 'results_llama-3.3.xlsx',
        'qwen_2_5': 'results_qwen-2.5.xlsx'
    }

    # Load Chinese data (Group1)
    for model, filename in file_mapping.items():
        cn_file = f'data/result_CN/{filename}'
        if os.path.exists(cn_file):
            df = load_and_clean_data(cn_file)
            if not df.empty:
                df['Dataset'] = 'CN'
                df['Group'] = 'Group1'
                df['Model'] = model
                all_data.append(df)

    # Load English data (Group2)
    for model, filename in file_mapping.items():
        en_file = f'data/result_EN/{filename}'
        if os.path.exists(en_file):
            df = load_and_clean_data(en_file)
            if not df.empty:
                df['Dataset'] = 'EN'
                df['Group'] = 'Group2'
                df['Model'] = model
                all_data.append(df)

    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        return combined_df
    else:
        return pd.DataFrame()


def calculate_mpe_for_group(df, dataset=None, model_list=None):
    """Calculate MPE for a specific group (dataset + models)"""
    filtered_df = df.copy()

    if dataset:
        filtered_df = filtered_df[filtered_df['Dataset'] == dataset]
    if model_list:
        filtered_df = filtered_df[filtered_df['Model'].isin(model_list)]

    if len(filtered_df) == 0:
        return None

    # Group by CaseId and Principle to calculate MPE for each case
    mpe_values = []

    for (case_id, principle), case_group in filtered_df.groupby(['CaseId', 'Principle']):
        # Get E_3_1 and E_3_2 values for this case
        e31_rows = case_group[case_group['Experiment'] == 'E_3_1']
        e32_rows = case_group[case_group['Experiment'] == 'E_3_2']

        if len(e31_rows) > 0 and len(e32_rows) > 0:
            e31_value = e31_rows['answerValue'].iloc[0]
            e32_value = e32_rows['answerValue'].iloc[0]
            mpe = abs(e32_value - e31_value)
            mpe_values.append(mpe)

    if len(mpe_values) > 0:
        return np.mean(mpe_values)
    else:
        return None


def perform_comprehensive_t_tests(df):
    """Perform all T-tests according to the experimental design"""
    results = []

    # 1. Dataset (LT): D(US) vs D(CN)
    group1_mpe = calculate_mpe_for_group(df, dataset='CN')  # Group1 = CN
    group2_mpe = calculate_mpe_for_group(df, dataset='EN')  # Group2 = EN

    if group1_mpe is not None and group2_mpe is not None:
        delta_mpe = group2_mpe - group1_mpe

        # T-test between EN and CN datasets
        cn_data = df[df['Dataset'] == 'CN']['answerValue']
        en_data = df[df['Dataset'] == 'EN']['answerValue']
        t_stat, p_val = stats.ttest_ind(en_data, cn_data)

        results.append({
            'Comparison': 'Dataset (LT)',
            'Groups': 'D(US) vs D(CN)',
            'Group1_MPE': group1_mpe,
            'Group2_MPE': group2_mpe,
            'Delta_MPE': delta_mpe,
            'P_value': p_val,
            'T_stat': t_stat,
            'Significant': p_val < 0.05
        })

    # 2. Model (ver): M(R1) vs M(V3)
    r1_mpe = calculate_mpe_for_group(df, model_list=['deepseek_r1'])
    v3_mpe = calculate_mpe_for_group(df, model_list=['deepseek_v3'])

    if r1_mpe is not None and v3_mpe is not None:
        delta_mpe = r1_mpe - v3_mpe

        # T-test between R1 and V3 models
        r1_data = df[df['Model'] == 'deepseek_r1']['answerValue']
        v3_data = df[df['Model'] == 'deepseek_v3']['answerValue']
        t_stat, p_val = stats.ttest_ind(r1_data, v3_data)

        results.append({
            'Comparison': 'Model (ver)',
            'Groups': 'M(R1) vs M(V3)',
            'Group1_MPE': v3_mpe,  # Group1 = V3
            'Group2_MPE': r1_mpe,  # Group2 = R1
            'Delta_MPE': delta_mpe,
            'P_value': p_val,
            'T_stat': t_stat,
            'Significant': p_val < 0.05
        })

    # 3. Model (LT): M(US) vs M(CN)
    us_models = ['gpt_4o', 'llama_3_3']
    cn_models = ['deepseek_v3', 'qwen_2_5']

    us_mpe = calculate_mpe_for_group(df, model_list=us_models)
    cn_mpe = calculate_mpe_for_group(df, model_list=cn_models)

    if us_mpe is not None and cn_mpe is not None:
        delta_mpe = us_mpe - cn_mpe

        # T-test between US and CN models
        us_data = df[df['Model'].isin(us_models)]['answerValue']
        cn_data = df[df['Model'].isin(cn_models)]['answerValue']
        t_stat, p_val = stats.ttest_ind(us_data, cn_data)

        results.append({
            'Comparison': 'Model (LT)',
            'Groups': 'M(US) vs M(CN)',
            'Group1_MPE': cn_mpe,  # Group1 = CN models
            'Group2_MPE': us_mpe,  # Group2 = US models
            'Delta_MPE': delta_mpe,
            'P_value': p_val,
            'T_stat': t_stat,
            'Significant': p_val < 0.05
        })

    # 4. Dataset x Model (LT): DUS(R1) vs DUS(V3) and DCN(R1) vs DCN(V3)
    dus_r1_mpe = calculate_mpe_for_group(df, dataset='EN', model_list=['deepseek_r1'])
    dus_v3_mpe = calculate_mpe_for_group(df, dataset='EN', model_list=['deepseek_v3'])
    dcn_r1_mpe = calculate_mpe_for_group(df, dataset='CN', model_list=['deepseek_r1'])
    dcn_v3_mpe = calculate_mpe_for_group(df, dataset='CN', model_list=['deepseek_v3'])

    if dus_r1_mpe is not None and dus_v3_mpe is not None:
        delta_mpe_dus = dus_r1_mpe - dus_v3_mpe

        # T-test for DUS interaction
        dus_r1_data = df[(df['Dataset'] == 'EN') & (df['Model'] == 'deepseek_r1')]['answerValue']
        dus_v3_data = df[(df['Dataset'] == 'EN') & (df['Model'] == 'deepseek_v3')]['answerValue']
        t_stat, p_val = stats.ttest_ind(dus_r1_data, dus_v3_data)

        results.append({
            'Comparison': 'Dataset x Model (LT) - DUS',
            'Groups': 'DUS(R1) vs DUS(V3)',
            'Group1_MPE': dus_v3_mpe,  # Group1 = V3
            'Group2_MPE': dus_r1_mpe,  # Group2 = R1
            'Delta_MPE': delta_mpe_dus,
            'P_value': p_val,
            'T_stat': t_stat,
            'Significant': p_val < 0.05
        })

    if dcn_r1_mpe is not None and dcn_v3_mpe is not None:
        delta_mpe_dcn = dcn_r1_mpe - dcn_v3_mpe

        # T-test for DCN interaction
        dcn_r1_data = df[(df['Dataset'] == 'CN') & (df['Model'] == 'deepseek_r1')]['answerValue']
        dcn_v3_data = df[(df['Dataset'] == 'CN') & (df['Model'] == 'deepseek_v3')]['answerValue']
        t_stat, p_val = stats.ttest_ind(dcn_r1_data, dcn_v3_data)

        results.append({
            'Comparison': 'Dataset x Model (LT) - DCN',
            'Groups': 'DCN(R1) vs DCN(V3)',
            'Group1_MPE': dcn_v3_mpe,  # Group1 = V3
            'Group2_MPE': dcn_r1_mpe,  # Group2 = R1
            'Delta_MPE': delta_mpe_dcn,
            'P_value': p_val,
            'T_stat': t_stat,
            'Significant': p_val < 0.05
        })

    # 5. Dataset x Model (ver): DUS(MUS) vs DUS(MCN) and DCN(MUS) vs DCN(MCN)
    dus_mus_mpe = calculate_mpe_for_group(df, dataset='EN', model_list=us_models)
    dus_mcn_mpe = calculate_mpe_for_group(df, dataset='EN', model_list=cn_models)
    dcn_mus_mpe = calculate_mpe_for_group(df, dataset='CN', model_list=us_models)
    dcn_mcn_mpe = calculate_mpe_for_group(df, dataset='CN', model_list=cn_models)

    if dus_mus_mpe is not None and dus_mcn_mpe is not None:
        delta_mpe_dus_ver = dus_mus_mpe - dus_mcn_mpe

        # T-test for DUS version interaction
        dus_mus_data = df[(df['Dataset'] == 'EN') & (df['Model'].isin(us_models))]['answerValue']
        dus_mcn_data = df[(df['Dataset'] == 'EN') & (df['Model'].isin(cn_models))]['answerValue']
        t_stat, p_val = stats.ttest_ind(dus_mus_data, dus_mcn_data)

        results.append({
            'Comparison': 'Dataset x Model (ver) - DUS',
            'Groups': 'DUS(MUS) vs DUS(MCN)',
            'Group1_MPE': dus_mcn_mpe,  # Group1 = CN models
            'Group2_MPE': dus_mus_mpe,  # Group2 = US models
            'Delta_MPE': delta_mpe_dus_ver,
            'P_value': p_val,
            'T_stat': t_stat,
            'Significant': p_val < 0.05
        })

    if dcn_mus_mpe is not None and dcn_mcn_mpe is not None:
        delta_mpe_dcn_ver = dcn_mus_mpe - dcn_mcn_mpe

        # T-test for DCN version interaction
        dcn_mus_data = df[(df['Dataset'] == 'CN') & (df['Model'].isin(us_models))]['answerValue']
        dcn_mcn_data = df[(df['Dataset'] == 'CN') & (df['Model'].isin(cn_models))]['answerValue']
        t_stat, p_val = stats.ttest_ind(dcn_mus_data, dcn_mcn_data)

        results.append({
            'Comparison': 'Dataset x Model (ver) - DCN',
            'Groups': 'DCN(MUS) vs DCN(MCN)',
            'Group1_MPE': dcn_mcn_mpe,  # Group1 = CN models
            'Group2_MPE': dcn_mus_mpe,  # Group2 = US models
            'Delta_MPE': delta_mpe_dcn_ver,
            'P_value': p_val,
            'T_stat': t_stat,
            'Significant': p_val < 0.05
        })

    return results


def create_summary_table(results):
    """Create a summary table of all results"""
    print("\n" + "=" * 100)
    print("CORRECTED MPE ANALYSIS SUMMARY TABLE")
    print("=" * 100)

    if results:
        df_results = pd.DataFrame(results)

        print(
            f"{'Comparison':<30} {'Groups':<25} {'Group1 MPE':<12} {'Group2 MPE':<12} {'Δ MPE':<10} {'P-value':<12} {'Sig':<5}")
        print("-" * 100)

        for _, row in df_results.iterrows():
            sig_marker = "***" if row['P_value'] < 0.001 else "**" if row['P_value'] < 0.01 else "*" if row[
                                                                                                            'P_value'] < 0.05 else ""
            g1_mpe = f"{row['Group1_MPE']:.3f}" if row['Group1_MPE'] is not None else "N/A"
            g2_mpe = f"{row['Group2_MPE']:.3f}" if row['Group2_MPE'] is not None else "N/A"
            delta_mpe = f"{row['Delta_MPE']:.3f}" if row['Delta_MPE'] is not None else "N/A"

            print(
                f"{row['Comparison']:<30} {row['Groups']:<25} {g1_mpe:<12} {g2_mpe:<12} {delta_mpe:<10} {row['P_value']:<12.6f} {sig_marker:<5}")

        print("\nSignificance levels: *** p<0.001, ** p<0.01, * p<0.05")
        print("Δ MPE = Group2 MPE - Group1 MPE")
        print("MPE calculated as |E_3_2 - E_3_1| for each case, then averaged")

        return df_results
    else:
        print("No results to display")
        return pd.DataFrame()


def main():
    df = load_all_data()

    if df.empty:
        print("Error: No data loaded. Please check file paths and data format.")
        return

    print(f"Total records loaded: {len(df)}")
    print("Computing corrected MPE analysis...")

    results = perform_comprehensive_t_tests(df)
    summary_df = create_summary_table(results)

    if not summary_df.empty:
        summary_df.to_csv('e3_corrected_mpe_results.csv', index=False)
        print(f"\nResults saved to 'e3_corrected_mpe_results.csv'")


if __name__ == "__main__":
    main()