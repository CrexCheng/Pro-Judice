import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.stats import ttest_rel, ttest_ind, ttest_1samp
import seaborn as sns
from matplotlib import rcParams
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# Set English font support
rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
rcParams['axes.unicode_minus'] = False

# Define standard principle order exactly as specified (按照您提供的新顺序)
standard_principle_order = [
    "Impartial Jury",
    "No Double Jeopardy",
    "Presumption of Innocence",
    "Against Self Incrimination",
    "lawful Search & Seizure",
    "Confrontation Rights",
    "Right to Counsel",
    "Speedy Trial",
    "Public Trial"
]

# Define colors from the reference image (图4)
chinese_color = '#87CEEB'  # Light blue from image 4
english_color = '#FFA500'  # Orange from image 4


def get_picture_E1_horizontal():
    """E1 horizontal bar chart"""
    # 读取Excel文件
    file_path = "data/E1&E2/E1均值柱状图.xlsx"
    df = pd.read_excel(file_path)

    # 提取数据
    principles = df["principle"]
    chinese = df["中文数据集"]
    english = df["英文数据集"]

    print("E1原始数据:")
    for i, p in enumerate(principles):
        print(f"  {i}: {p}")

    # 创建原始Excel数据到标准原则的映射
    excel_to_standard_mapping = {
        "Presumption of Innocence": "Presumption of Innocence",
        "right against unreasonable searches and seizures/Protection Against Arbitrary Interference with Home and Privacy": "lawful Search & Seizure",
        "Right Against Self-Incrimination": "Against Self Incrimination",
        "Right to a Speedy Trial": "Speedy Trial",
        "Right to a Public Trial": "Public Trial",
        "Right to Counsel": "Right to Counsel",
        "Right to Confront Adverse Witnesses and to Procure Favorable Witnesses": "Confrontation Rights",
        "Protection Against Double Jeopardy": "No Double Jeopardy",
        "right to an impartial jury": "Impartial Jury"
    }

    # 创建数据字典
    data_dict = {}
    for i, principle in enumerate(principles):
        if principle in excel_to_standard_mapping:
            standard_name = excel_to_standard_mapping[principle]
            data_dict[standard_name] = (chinese[i], english[i])

    # 按标准顺序重新排列数据
    ordered_chinese = []
    ordered_english = []
    used_principles = []

    for std_principle in standard_principle_order:
        if std_principle in data_dict:
            used_principles.append(std_principle)
            ordered_chinese.append(data_dict[std_principle][0])
            ordered_english.append(data_dict[std_principle][1])

    # 设置横向柱状图位置
    y = np.arange(len(used_principles))
    height = 0.35

    # 作图
    plt.figure(figsize=(7, 8))
    plt.barh(y - height / 2, ordered_chinese, height, color=chinese_color)
    plt.barh(y + height / 2, ordered_english, height, color=english_color)

    # 设置标签 - 放大字体
    plt.xlabel("E1: Mean of Procedure Awareness", fontsize=14)
    plt.ylabel("Principle", fontsize=14)
    plt.yticks(y, used_principles, fontsize=14)
    plt.xticks(fontsize=14)  # 设置横坐标数字大小

    # 设置横轴范围到头 (根据数据范围设置)
    plt.xlim(0, 1)

    # 反转y轴顺序，使第一个原则在顶部
    plt.gca().invert_yaxis()

    plt.tight_layout()

    # Save as PNG file
    plt.savefig('E1_horizontal_chart.png', dpi=300, bbox_inches='tight')
    print("E1 chart saved as 'E1_horizontal_chart.png'")

    plt.show()


def get_picture_E2_horizontal():
    """E2 horizontal bar chart"""
    # 读取Excel文件
    file_path2 = "data/E1&E2/E2均值柱状图.xlsx"
    df2 = pd.read_excel(file_path2)

    # 提取数据
    principles = df2["principle"]
    chinese = df2["中文数据集"]
    english = df2["英文数据集"]

    print("E2原始数据:")
    for i, p in enumerate(principles):
        print(f"  {i}: {p}")

    # 创建原始Excel数据到标准原则的映射（与E1相同的映射）
    excel_to_standard_mapping = {
        "Presumption of Innocence": "Presumption of Innocence",
        "right against unreasonable searches and seizures/Protection Against Arbitrary Interference with Home and Privacy": "lawful Search & Seizure",
        "Right Against Self-Incrimination": "Against Self Incrimination",
        "Right to a Speedy Trial": "Speedy Trial",
        "Right to a Public Trial": "Public Trial",
        "Right to Counsel": "Right to Counsel",
        "Right to Confront Adverse Witnesses and to Procure Favorable Witnesses": "Confrontation Rights",
        "Protection Against Double Jeopardy": "No Double Jeopardy",
        "right to an impartial jury": "Impartial Jury"
    }

    # 创建数据字典
    data_dict = {}
    for i, principle in enumerate(principles):
        if principle in excel_to_standard_mapping:
            standard_name = excel_to_standard_mapping[principle]
            data_dict[standard_name] = (chinese[i], english[i])

    # 按标准顺序重新排列数据
    ordered_chinese = []
    ordered_english = []
    used_principles = []

    for std_principle in standard_principle_order:
        if std_principle in data_dict:
            used_principles.append(std_principle)
            ordered_chinese.append(data_dict[std_principle][0])
            ordered_english.append(data_dict[std_principle][1])

    # 设置横向柱状图位置
    y = np.arange(len(used_principles))
    height = 0.35

    # 作图
    plt.figure(figsize=(7, 8))
    plt.barh(y - height / 2, ordered_chinese, height, color=chinese_color)
    plt.barh(y + height / 2, ordered_english, height, color=english_color)

    # 设置标签 - 放大字体
    plt.xlabel("E2: Mean of Procedure vs Substance", fontsize=14)
    plt.yticks(y, used_principles, fontsize=12)
    plt.xticks(fontsize=14)  # 设置横坐标数字大小
    plt.axvline(x=0, color='black', linestyle='-', alpha=0.3)

    # 设置横轴范围到头 (根据数据范围设置)
    plt.xlim(-1, 1)

    # 反转y轴顺序，使第一个原则在顶部
    plt.gca().invert_yaxis()

    plt.tight_layout()

    # Save as PNG file
    plt.savefig('E2_horizontal_chart.png', dpi=300, bbox_inches='tight')
    print("E2 chart saved as 'E2_horizontal_chart.png'")

    plt.show()


class ProceduralJusticeHypothesisAnalyzer:
    """E3数据处理类"""

    def __init__(self, data_path="data"):
        self.data_path = Path(data_path)
        self.cn_path = self.data_path / "result_CN"
        self.en_path = self.data_path / "result_EN"
        self.models = ['deepseek-r1', 'deepseek-v3', 'gpt-4o', 'llama-3.3', 'qwen-2.5']

    def load_all_data(self):
        """Load all Excel files"""
        all_data = []

        print("Loading data files...")
        print("=" * 70)

        # Load Chinese data
        for model in self.models:
            file_pattern = f"results_{model}.xlsx"
            cn_file = self.cn_path / file_pattern

            if cn_file.exists():
                try:
                    df = pd.read_excel(cn_file)
                    df['Language'] = 'Chinese'
                    df['Legal_System'] = 'Chinese_Law'
                    df['Model'] = model
                    all_data.append(df)
                    print(f"✓ Loaded Chinese data: {file_pattern} ({len(df)} records)")
                except Exception as e:
                    print(f"✗ Failed to load: {file_pattern} - {e}")

        # Load English data
        for model in self.models:
            file_pattern = f"results_{model}.xlsx"
            en_file = self.en_path / file_pattern

            if en_file.exists():
                try:
                    df = pd.read_excel(en_file)
                    df['Language'] = 'English'
                    df['Legal_System'] = 'Common_Law'
                    df['Model'] = model
                    all_data.append(df)
                    print(f"✓ Loaded English data: {file_pattern} ({len(df)} records)")
                except Exception as e:
                    print(f"✗ Failed to load: {file_pattern} - {e}")

        if not all_data:
            raise ValueError("No data files loaded successfully!")

        # Combine all data
        combined_df = pd.concat(all_data, ignore_index=True)
        return self.process_data(combined_df)

    def process_data(self, df):
        """Process data - directly use answerValue column"""
        print(f"\nData processing:")
        print(f"  Total records: {len(df)}")

        # Use answerValue column directly
        df['sentence_months'] = pd.to_numeric(df['answerValue'], errors='coerce')

        # Statistics
        total_records = len(df)
        missing_values = df['sentence_months'].isna().sum()
        valid_values = total_records - missing_values

        print(f"  Valid values: {valid_values} ({valid_values / total_records * 100:.1f}%)")
        print(f"  Missing values: {missing_values} ({missing_values / total_records * 100:.1f}%)")

        return df

    def translate_chinese_principles(self, df):
        """Translate Chinese principle names to English - 使用原来的翻译方式"""
        principle_translation = {
            '无罪推定': 'Presumption of Innocence',
            '不受任意逮捕与拘禁/住宅、隐私不受任意干涉': 'Freedom from Arbitrary Arrest and Detention',
            '不被强迫自证其罪': 'Privilege Against Self-Incrimination',
            '迅速审判': 'Right to Speedy Trial',
            '公开审判': 'Right to Public Trial',
            '获得律师帮助': 'Right to Counsel',
            '与不利于己的证人当庭对质并申请有利于己的证人出庭作证': 'Right to Confront Witnesses',
            '反对双重归罪': 'Protection Against Double Jeopardy',
            '获得公正、公平审判的权利': 'Right to Fair Trial'
        }

        df_copy = df.copy()
        df_copy['Principle_EN'] = df_copy['Principle'].map(principle_translation).fillna(df_copy['Principle'])

        # Create short names for visualization (使用原来的短名称映射)
        short_name_mapping = {
            'Presumption of Innocence': 'Presumption',
            'Freedom from Arbitrary Arrest and Detention': 'No Arbitrary Arrest',
            'Privilege Against Self-Incrimination': 'No Self-Incrimination',
            'Right to Speedy Trial': 'Speedy Trial',
            'Right to Public Trial': 'Public Trial',
            'Right to Counsel': 'Right to Counsel',
            'Right to Confront Witnesses': 'Confront Witnesses',
            'Protection Against Double Jeopardy': 'No Double Jeopardy',
            'Right to Fair Trial': 'Fair Trial'
        }

        df_copy['Principle_Short'] = df_copy['Principle_EN'].map(short_name_mapping).fillna(df_copy['Principle_EN'])
        return df_copy

    def create_legal_system_sensitivity_chart_horizontal(self, df):
        """Create E3 horizontal bar chart - 使用绝对值来衡量效应大小"""
        print("\n" + "=" * 70)
        print("Generating E3 - Legal System Sensitivity by Principle Chart")
        print("=" * 70)

        df_clean = df.dropna(subset=['sentence_months']).copy()

        if len(df_clean) == 0:
            print("No valid data for visualization")
            return

        # Translate Chinese principles to English
        df_clean = self.translate_chinese_principles(df_clean)

        # Set style for the chart
        plt.style.use('default')

        print("Generating Chart: E3 - Legal System Sensitivity by Principle")
        plt.figure(figsize=(7, 8))

        if 'Principle_Short' in df_clean.columns:
            principle_legal_effects = []

            # 获取可用的原则 - 调试信息
            available_principles = df_clean['Principle_Short'].unique()
            print(f"E3可用原则: {list(available_principles)}")

            # 打印原始数据中的中文原则名称
            if 'Principle' in df_clean.columns:
                original_principles = df_clean['Principle'].unique()
                print(f"E3原始中文原则: {list(original_principles)}")

            for principle in available_principles:
                if pd.isna(principle):
                    continue

                principle_data = df_clean[df_clean['Principle_Short'] == principle]
                print(f"处理原则: {principle}, 数据行数: {len(principle_data)}")

                for legal_system in ['Chinese_Law', 'Common_Law']:
                    system_data = principle_data[principle_data['Legal_System'] == legal_system]

                    e31_data = system_data[system_data['Experiment'] == 'E_3_1']['sentence_months']
                    e32_data = system_data[system_data['Experiment'] == 'E_3_2']['sentence_months']

                    e31_mean = e31_data.mean()
                    e32_mean = e32_data.mean()

                    print(f"  {legal_system}: E31={e31_mean:.2f}({len(e31_data)}), E32={e32_mean:.2f}({len(e32_data)})")

                    if not pd.isna(e31_mean) and not pd.isna(e32_mean):
                        # Define principles that need E1-E2 calculation (使用原来的短名称)
                        reverse_calculation_principles = [
                            'Public Trial',  # 第5个原则：公开审判
                            'Right to Counsel',  # 第6个原则：获得律师帮助
                            'Confront Witnesses',  # 第7个原则：与不利于己的证人当庭对质并申请有利于己的证人出庭作证
                            'Fair Trial'  # 第9个原则：获得公正、公平审判的权利
                        ]

                        # Calculate difference based on principle
                        if principle in reverse_calculation_principles:
                            raw_diff = e31_mean - e32_mean  # E1 - E2 for principles 5,6,7,9
                        else:
                            raw_diff = e32_mean - e31_mean  # E2 - E1 for other principles

                        # 取绝对值来衡量效应大小（不管方向）
                        sentence_diff = abs(raw_diff)

                        print(f"  计算结果: raw_diff={raw_diff:.3f}, sentence_diff(abs)={sentence_diff:.3f} months")

                        principle_legal_effects.append({
                            'Principle': principle,
                            'Legal_System': 'Civil law (Chinese)' if legal_system == 'Chinese_Law' else 'Common law (US)',
                            'Sentence_Diff_Months': sentence_diff
                        })

            if principle_legal_effects:
                effect_df = pd.DataFrame(principle_legal_effects)
                print(f"E3最终数据: {len(effect_df)} 行")
                print(effect_df)

                # 创建透视表
                pivot_data = effect_df.pivot(index='Principle', columns='Legal_System', values='Sentence_Diff_Months')
                print(f"E3透视表:")
                print(pivot_data)

                # 创建短名称到标准名称的映射表（使用新的顺序）
                short_to_standard_mapping = {
                    'Presumption': 'Presumption of Innocence',
                    'No Arbitrary Arrest': 'lawful Search & Seizure',
                    'No Self-Incrimination': 'Against Self Incrimination',
                    'Speedy Trial': 'Speedy Trial',
                    'Public Trial': 'Public Trial',
                    'Right to Counsel': 'Right to Counsel',
                    'Confront Witnesses': 'Confrontation Rights',
                    'No Double Jeopardy': 'No Double Jeopardy',
                    'Fair Trial': 'Impartial Jury'
                }

                # 将短名称转换为标准名称
                pivot_data.index = pivot_data.index.map(lambda x: short_to_standard_mapping.get(x, x))

                # 手动排序以匹配新的标准顺序
                ordered_principles = []
                for std_principle in standard_principle_order:
                    if std_principle in pivot_data.index:
                        ordered_principles.append(std_principle)
                        print(f"匹配到原则: {std_principle}")

                if ordered_principles:
                    pivot_data = pivot_data.reindex(ordered_principles)

                    # 确保列的顺序
                    expected_columns = ['Civil law (Chinese)', 'Common law (US)']
                    for col in expected_columns:
                        if col not in pivot_data.columns:
                            pivot_data[col] = 0.0
                    pivot_data = pivot_data[expected_columns]

                    # 填充缺失值
                    pivot_data = pivot_data.fillna(0)

                    # 设置横向柱状图位置
                    y = np.arange(len(pivot_data.index))
                    height = 0.35

                    # 绘制横向柱状图
                    plt.barh(y - height / 2, pivot_data['Civil law (Chinese)'], height,
                             label='Civil law (Chinese)', color=chinese_color)
                    plt.barh(y + height / 2, pivot_data['Common law (US)'], height,
                             label='Common law (US)', color=english_color)

                    # 设置标签 - 放大字体
                    plt.xlabel('E3: MPE', fontsize=18)
                    plt.yticks(y, pivot_data.index, fontsize=11)
                    plt.xticks(fontsize=14)  # 设置横坐标数字大小

                    # 将图例放在右上角
                    plt.legend(loc='upper right')
                    plt.axvline(x=0, color='black', linestyle='-', alpha=0.3)

                    # 由于现在使用绝对值，横坐标范围从0开始
                    max_val = max(pivot_data.max())
                    plt.xlim(0, max_val * 1.1)

                    # 反转y轴顺序，使第一个原则在顶部
                    plt.gca().invert_yaxis()

                    plt.tight_layout()

                    # Save as PNG file
                    plt.savefig('E3_horizontal_chart.png', dpi=300, bbox_inches='tight')
                    print("E3 chart saved as 'E3_horizontal_chart.png'")

                    plt.show()
                else:
                    print("没有找到匹配的原则")
            else:
                print("没有有效的E3数据")

        print("E3 chart generated successfully!")

    def run_e3_chart_analysis(self):
        """Run analysis and generate E3 chart"""
        try:
            df = self.load_all_data()
            self.create_legal_system_sensitivity_chart_horizontal(df)
        except Exception as e:
            print(f"Error occurred during analysis: {e}")
            import traceback
            traceback.print_exc()


def get_picture_E3_horizontal():
    """Generate E3 horizontal bar chart"""
    analyzer = ProceduralJusticeHypothesisAnalyzer()
    analyzer.run_e3_chart_analysis()


# 运行所有三个图表
if __name__ == "__main__":
    print("Generating E1 Horizontal Chart:")
    get_picture_E1_horizontal()

    print("\nGenerating E2 Horizontal Chart:")
    get_picture_E2_horizontal()

    print("\nGenerating E3 Horizontal Chart:")
    get_picture_E3_horizontal()