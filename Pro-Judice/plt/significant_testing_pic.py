import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings

warnings.filterwarnings('ignore')


def load_and_clean_data(file_path):
    """Load Excel file and extract clean numeric data"""
    try:
        df = pd.read_excel(file_path)
        # Clean the data
        df['answerValue'] = pd.to_numeric(df['answerValue'], errors='coerce')
        df = df.dropna(subset=['answerValue'])
        print(f"Loaded {len(df)} valid records from {os.path.basename(file_path)}")
        return df
    except Exception as e:
        print(f"Error loading {file_path}: {str(e)}")
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

    # Load Chinese data
    for model, filename in file_mapping.items():
        cn_file = f'data/result_CN/{filename}'
        if os.path.exists(cn_file):
            df = load_and_clean_data(cn_file)
            if not df.empty:
                df['Legal_System'] = 'CN'
                df['Model'] = model
                all_data.append(df)

    # Load English data
    for model, filename in file_mapping.items():
        en_file = f'data/result_EN/{filename}'
        if os.path.exists(en_file):
            df = load_and_clean_data(en_file)
            if not df.empty:
                df['Legal_System'] = 'EN'
                df['Model'] = model
                all_data.append(df)

    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        return combined_df
    else:
        return pd.DataFrame()


def calculate_mpe_by_principle(df, model=None, model_type=None):
    """Calculate MPE (E3_2 - E3_1) for each principle and legal system"""
    results = []

    # Filter data if specific model or model type specified
    if model:
        df = df[df['Model'] == model]
    elif model_type:
        if model_type == 'Chinese':
            df = df[df['Model'].isin(['deepseek_v3', 'qwen_2_5'])]
        elif model_type == 'English':
            df = df[df['Model'].isin(['gpt_4o', 'llama_3_3'])]

    # Group by Legal System and Principle
    for legal_system in ['CN', 'EN']:
        legal_data = df[df['Legal_System'] == legal_system]

        if 'Principle' in legal_data.columns:
            principles = legal_data['Principle'].unique()

            for principle in principles:
                principle_data = legal_data[legal_data['Principle'] == principle]

                # Get E3_1 and E3_2 data
                e31_data = principle_data[principle_data['Experiment'] == 'E_3_1']['answerValue']
                e32_data = principle_data[principle_data['Experiment'] == 'E_3_2']['answerValue']

                if len(e31_data) > 0 and len(e32_data) > 0:
                    e31_mean = e31_data.mean()
                    e32_mean = e32_data.mean()
                    mpe = abs(e32_mean - e31_mean)  # MPE as absolute difference

                    results.append({
                        'Legal_System': legal_system,
                        'Principle': principle,
                        'MPE': mpe,
                        'E31_mean': e31_mean,
                        'E32_mean': e32_mean
                    })

    return results


def create_comprehensive_six_panel(df):
    """Create the comprehensive 2x3 panel analysis with MPE"""

    # Set up the figure
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    # Colors
    colors = {
        'CN': '#3498db', 'EN': '#e74c3c',
        'Chinese': '#2ecc71', 'English': '#f39c12',
        'deepseek_r1': '#e74c3c', 'deepseek_v3': '#3498db'
    }

    # === TOP ROW: MPE DISTRIBUTION PLOTS ===

    # Top Left: Legal System Distribution (MPE)
    ax1 = axes[0, 0]

    # Calculate MPE for overall legal systems
    overall_mpe = calculate_mpe_by_principle(df)
    if overall_mpe:
        cn_mpe_values = [item['MPE'] for item in overall_mpe if item['Legal_System'] == 'CN']
        en_mpe_values = [item['MPE'] for item in overall_mpe if item['Legal_System'] == 'EN']

        box_data = [cn_mpe_values, en_mpe_values] if cn_mpe_values and en_mpe_values else [[0], [0]]

        bp1 = ax1.boxplot(box_data, labels=['Civil Law\n(CN)', 'Common Law\n(EN)'], patch_artist=True)
        bp1['boxes'][0].set_facecolor(colors['CN'])
        bp1['boxes'][1].set_facecolor(colors['EN'])
        for box in bp1['boxes']:
            box.set_alpha(0.7)

    ax1.set_title('Dataset Distribution', fontweight='bold', fontsize=16)
    ax1.set_xticklabels(['Civil Law\n(CN)', 'Common Law\n(EN)'], fontsize=16)
    ax1.set_ylabel('MPE (months)', fontsize=16)
    ax1.set_ylim(0, 50)  # Set y-axis range
    ax1.grid(True, alpha=0.3)

    # Top Middle: Model Type Distribution (MPE)
    ax2 = axes[0, 1]

    # Calculate MPE for Chinese vs English models
    chinese_mpe = calculate_mpe_by_principle(df, model_type='Chinese')
    english_mpe = calculate_mpe_by_principle(df, model_type='English')

    chinese_values = [item['MPE'] for item in chinese_mpe] if chinese_mpe else [0]
    english_values = [item['MPE'] for item in english_mpe] if english_mpe else [0]

    box_data = [chinese_values, english_values]

    bp2 = ax2.boxplot(box_data, labels=['Chinese\nModels', 'English\nModels'], patch_artist=True)
    bp2['boxes'][0].set_facecolor(colors['Chinese'])
    bp2['boxes'][1].set_facecolor(colors['English'])
    for box in bp2['boxes']:
        box.set_alpha(0.7)

    ax2.set_title('Model Type Distribution', fontweight='bold', fontsize=16)
    ax2.set_ylabel('MPE (months)', fontsize=16)
    ax2.set_xticklabels(['Chinese\nModels', 'English\nModels'], fontsize=16)
    ax2.set_ylim(0, 50)  # Set y-axis range
    ax2.grid(True, alpha=0.3)

    # Top Right: DeepSeek Version Distribution (MPE)
    ax3 = axes[0, 2]

    # Calculate MPE for DeepSeek versions
    r1_mpe = calculate_mpe_by_principle(df, model='deepseek_r1')
    v3_mpe = calculate_mpe_by_principle(df, model='deepseek_v3')

    r1_values = [item['MPE'] for item in r1_mpe] if r1_mpe else [0]
    v3_values = [item['MPE'] for item in v3_mpe] if v3_mpe else [0]

    box_data = [r1_values, v3_values]

    bp3 = ax3.boxplot(box_data, labels=['DeepSeek\nR1', 'DeepSeek\nV3'], patch_artist=True)
    bp3['boxes'][0].set_facecolor(colors['deepseek_r1'])
    bp3['boxes'][1].set_facecolor(colors['deepseek_v3'])
    for box in bp3['boxes']:
        box.set_alpha(0.7)

    ax3.set_title('Model Version Distribution', fontweight='bold', fontsize=16)
    ax3.set_ylabel('MPE (months)', fontsize=16)
    ax3.set_xticklabels(['DeepSeek\nR1', 'DeepSeek\nV3'], fontsize=16)
    ax3.set_ylim(0, 50)  # Set y-axis range
    ax3.grid(True, alpha=0.3)

    # === BOTTOM ROW: MPE INTERACTION PLOTS ===

    # Bottom Left: Legal System × Model Type (MPE)
    ax4 = axes[1, 0]

    # Calculate average MPE for each model type by legal system
    cn_chinese_mpe = np.mean([item['MPE'] for item in chinese_mpe if item['Legal_System'] == 'CN']) if chinese_mpe else 0
    en_chinese_mpe = np.mean([item['MPE'] for item in chinese_mpe if item['Legal_System'] == 'EN']) if chinese_mpe else 0
    cn_english_mpe = np.mean([item['MPE'] for item in english_mpe if item['Legal_System'] == 'CN']) if english_mpe else 0
    en_english_mpe = np.mean([item['MPE'] for item in english_mpe if item['Legal_System'] == 'EN']) if english_mpe else 0

    legal_systems = ['CN', 'EN']
    chinese_line = [cn_chinese_mpe, en_chinese_mpe]
    english_line = [cn_english_mpe, en_english_mpe]

    ax4.plot(legal_systems, chinese_line, 'o-', linewidth=3, markersize=10,
             color=colors['Chinese'], label='Chinese Models', alpha=0.8)
    ax4.plot(legal_systems, english_line, 's-', linewidth=3, markersize=10,
             color=colors['English'], label='English Models', alpha=0.8)

    # Add value labels with corrected positioning
    for i, (cn_val, en_val) in enumerate(zip(chinese_line, english_line)):
        if cn_val > 0:
            ax4.annotate(f'{cn_val:.1f}', (i, cn_val), textcoords="offset points",
                         xytext=(0, 15), ha='center', fontweight='bold', fontsize=10)
        if en_val > 0:
            ax4.annotate(f'{en_val:.1f}', (i, en_val), textcoords="offset points",
                         xytext=(0, -15), ha='center', fontweight='bold', fontsize=10)

    ax4.set_title('Dataset × Model Type', fontweight='bold', fontsize=14)
    ax4.set_xticklabels(['CN', 'EN'], fontsize=18)
    ax4.set_ylabel('MPE (months)', fontsize=16)
    ax4.set_ylim(0, 14)  # Set y-axis range
    ax4.legend(fontsize=12)
    ax4.grid(True, alpha=0.3)

    # Bottom Middle: Legal System × All Models (MPE)
    ax5 = axes[1, 1]

    # Calculate MPE for each individual model
    model_order = ['deepseek_r1', 'deepseek_v3', 'qwen_2_5', 'gpt_4o', 'llama_3_3']
    model_display_names = {
        'deepseek_r1': 'DeepSeek R1',
        'deepseek_v3': 'DeepSeek V3',
        'gpt_4o': 'GPT-4o',
        'llama_3_3': 'Llama 3.3',
        'qwen_2_5': 'Qwen 2.5'
    }

    cn_model_mpe = []
    en_model_mpe = []

    for model in model_order:
        model_mpe = calculate_mpe_by_principle(df, model=model)
        cn_mpe = np.mean([item['MPE'] for item in model_mpe if item['Legal_System'] == 'CN']) if model_mpe else 0
        en_mpe = np.mean([item['MPE'] for item in model_mpe if item['Legal_System'] == 'EN']) if model_mpe else 0
        cn_model_mpe.append(cn_mpe)
        en_model_mpe.append(en_mpe)

    x_positions = range(len(model_order))
    model_labels = [model_display_names[model] for model in model_order]

    ax5.plot(x_positions, cn_model_mpe, 'o-', linewidth=3, markersize=8,
             color=colors['CN'], label='Civil Law (CN)', alpha=0.8)
    ax5.plot(x_positions, en_model_mpe, 's-', linewidth=3, markersize=8,
             color=colors['EN'], label='Common Law (EN)', alpha=0.8)

    # Add value labels
    for i, (cn_val, en_val) in enumerate(zip(cn_model_mpe, en_model_mpe)):
        if cn_val > 0:
            ax5.annotate(f'{cn_val:.1f}', (i, cn_val), textcoords="offset points",
                         xytext=(0, 10), ha='center', fontweight='bold', fontsize=9, color=colors['CN'])
        if en_val > 0:
            ax5.annotate(f'{en_val:.1f}', (i, en_val), textcoords="offset points",
                         xytext=(0, -15), ha='center', fontweight='bold', fontsize=9, color=colors['EN'])

    ax5.set_title('Dataset × All Models', fontweight='bold', fontsize=14)
    ax5.set_ylabel('MPE (months)', fontsize=16)
    ax5.set_xticks(x_positions)
    ax5.set_xticklabels(model_labels, rotation=45, ha='right', fontsize=16)
    ax5.set_ylim(0, 14)  # Set y-axis range
    ax5.legend(fontsize=12)
    ax5.grid(True, alpha=0.3)

    # Bottom Right: Legal System × DeepSeek Version (MPE)
    ax6 = axes[1, 2]

    # Calculate average MPE for DeepSeek versions by legal system
    cn_r1_mpe = np.mean([item['MPE'] for item in r1_mpe if item['Legal_System'] == 'CN']) if r1_mpe else 0
    en_r1_mpe = np.mean([item['MPE'] for item in r1_mpe if item['Legal_System'] == 'EN']) if r1_mpe else 0
    cn_v3_mpe = np.mean([item['MPE'] for item in v3_mpe if item['Legal_System'] == 'CN']) if v3_mpe else 0
    en_v3_mpe = np.mean([item['MPE'] for item in v3_mpe if item['Legal_System'] == 'EN']) if v3_mpe else 0

    r1_line = [cn_r1_mpe, en_r1_mpe]
    v3_line = [cn_v3_mpe, en_v3_mpe]

    ax6.plot(legal_systems, r1_line, 'o-', linewidth=3, markersize=10,
             color=colors['deepseek_r1'], label='DeepSeek R1', alpha=0.8)
    ax6.plot(legal_systems, v3_line, 's-', linewidth=3, markersize=10,
             color=colors['deepseek_v3'], label='DeepSeek V3', alpha=0.8)

    # Add value labels
    for i, (r1_val, v3_val) in enumerate(zip(r1_line, v3_line)):
        if r1_val > 0:
            ax6.annotate(f'{r1_val:.1f}', (i, r1_val), textcoords="offset points",
                         xytext=(0, 15), ha='center', fontweight='bold', fontsize=10)
        if v3_val > 0:
            ax6.annotate(f'{v3_val:.1f}', (i, v3_val), textcoords="offset points",
                         xytext=(0, -15), ha='center', fontweight='bold', fontsize=10)

    ax6.set_title('Dataset × Model Version', fontweight='bold', fontsize=14)
    ax6.set_xticklabels(['CN', 'EN'], fontsize=18)
    ax6.set_ylabel('MPE (months)', fontsize=16)
    ax6.set_ylim(0, 14)  # Set y-axis range
    ax6.legend(fontsize=14)
    ax6.grid(True, alpha=0.3)

    # Adjust layout
    plt.tight_layout()

    # Save the plot
    plt.savefig('Significant_testing.png', dpi=300, bbox_inches='tight')
    plt.savefig('Significant_testing.pdf', bbox_inches='tight')

    plt.show()

    return df


def perform_statistical_analyses(df):
    """Perform statistical analyses on MPE values"""
    print(f"\n{'=' * 80}")
    print("MPE STATISTICAL ANALYSES")
    print(f"{'=' * 80}")

    # Calculate MPE for different groupings
    overall_mpe = calculate_mpe_by_principle(df)
    chinese_mpe = calculate_mpe_by_principle(df, model_type='Chinese')
    english_mpe = calculate_mpe_by_principle(df, model_type='English')
    r1_mpe = calculate_mpe_by_principle(df, model='deepseek_r1')
    v3_mpe = calculate_mpe_by_principle(df, model='deepseek_v3')

    if overall_mpe:
        print(f"\n1. OVERALL MPE ANALYSIS")
        print(f"{'-' * 50}")
        all_mpe_values = [item['MPE'] for item in overall_mpe]
        cn_mpe_values = [item['MPE'] for item in overall_mpe if item['Legal_System'] == 'CN']
        en_mpe_values = [item['MPE'] for item in overall_mpe if item['Legal_System'] == 'EN']

        print(f"Overall MPE: {np.mean(all_mpe_values):.2f} ± {np.std(all_mpe_values):.2f} months")
        print(f"CN MPE: {np.mean(cn_mpe_values):.2f} ± {np.std(cn_mpe_values):.2f} months")
        print(f"EN MPE: {np.mean(en_mpe_values):.2f} ± {np.std(en_mpe_values):.2f} months")

        if len(cn_mpe_values) > 1 and len(en_mpe_values) > 1:
            t_stat, p_val = stats.ttest_ind(cn_mpe_values, en_mpe_values)
            print(f"T-test (CN vs EN): t = {t_stat:.4f}, p = {p_val:.6f}")

    if chinese_mpe and english_mpe:
        print(f"\n2. MODEL TYPE MPE ANALYSIS")
        print(f"{'-' * 50}")
        chinese_values = [item['MPE'] for item in chinese_mpe]
        english_values = [item['MPE'] for item in english_mpe]

        print(f"Chinese Models MPE: {np.mean(chinese_values):.2f} ± {np.std(chinese_values):.2f} months")
        print(f"English Models MPE: {np.mean(english_values):.2f} ± {np.std(english_values):.2f} months")

        if len(chinese_values) > 1 and len(english_values) > 1:
            t_stat, p_val = stats.ttest_ind(chinese_values, english_values)
            print(f"T-test: t = {t_stat:.4f}, p = {p_val:.6f}")

    if r1_mpe and v3_mpe:
        print(f"\n3. DEEPSEEK VERSION MPE ANALYSIS")
        print(f"{'-' * 50}")
        r1_values = [item['MPE'] for item in r1_mpe]
        v3_values = [item['MPE'] for item in v3_mpe]

        print(f"DeepSeek R1 MPE: {np.mean(r1_values):.2f} ± {np.std(r1_values):.2f} months")
        print(f"DeepSeek V3 MPE: {np.mean(v3_values):.2f} ± {np.std(v3_values):.2f} months")

        if len(r1_values) > 1 and len(v3_values) > 1:
            t_stat, p_val = stats.ttest_ind(r1_values, v3_values)
            print(f"T-test: t = {t_stat:.4f}, p = {p_val:.6f}")

def main():
    print("Loading data for comprehensive six-panel MPE analysis...")
    df = load_all_data()

    if df.empty:
        print("Error: No data loaded. Please check file paths and data format.")
        return

    print(f"Total records loaded: {len(df)}")

    # Check data structure
    print(f"Columns: {list(df.columns)}")
    if 'Experiment' in df.columns:
        print(f"Experiments: {df['Experiment'].unique()}")
    if 'Legal_System' in df.columns:
        print(f"Legal Systems: {df['Legal_System'].unique()}")
    if 'Model' in df.columns:
        print(f"Models: {df['Model'].unique()}")

    # Create comprehensive visualization
    create_comprehensive_six_panel(df)

    # Perform statistical analyses
    perform_statistical_analyses(df)

    print(f"\n{'=' * 80}")
    print("ANALYSIS COMPLETED")
    print(f"{'=' * 80}")
    print("Comprehensive six-panel MPE visualization saved as:")
    print("- comprehensive_six_panel_mpe_analysis.png")
    print("- comprehensive_six_panel_mpe_analysis.pdf")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    main()
