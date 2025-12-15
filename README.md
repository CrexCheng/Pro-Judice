# Pro-Judice: Aligning LLMs with Procedural Fairness in Judicial Contexts

## 📊 Research Poster
View our poster for a comprehensive overview of the methodology and findings.
<img width="4767" height="6739" alt="poster" src="https://github.com/user-attachments/assets/23c29c28-f683-420c-a89d-b16570a0fb9e" />

## 📖 About
Large Language Models (LLMs) show potential in legal judgment prediction, but their "black-box" nature raises concerns about their adherence to procedural fairness. This study constructs a benchmark **Pro-Judice**, to evaluate LLM alignment with **Pro**cedural fairness in **Judi**cial contexts.

<img width="2686" height="1843" alt="image" src="https://github.com/user-attachments/assets/725d1a19-fb7b-4105-a034-49c6595b098d" />


Our main contributions include:

1. Constructing a cross-tradition criminal case dataset incorporating procedural fairness scenarios from both common law and civil law traditions.
2. Testing LLMs' procedural fairness awareness, preference between procedural vs. substantive justice, and the effect of procedural violations on substantive outcomes across five models from different legal contexts.
3. Introducing philosophically grounded metrics based on Rawls' procedural justice theory to evaluate LLMs' alignment with procedural fairness principles.

Our findings reveal that LLMs' perceptions of procedural fairness are significantly influenced by the legal tradition embedded in the prompt dataset, the model's own training context and different versions, and the interaction between dataset and model. Models trained on U.S. datasets displayed stronger awareness of procedural fairness, while those using Chinese datasets prioritized substantive outcomes. Aligning LLMs with procedural fairness within specific legal contexts enhances their interpretability in judicial applications.

The following sections introduce the data construction, environment setup, experiment execution, metric calculation, and significance testing methods.

### Data Construction and Introduction

**Step 1: Theoretical Foundation**

We grounded our framework in John Rawls' procedural justice theory, which categorizes procedural justice into pure, imperfect, and perfect forms. Criminal trials exemplify imperfect procedural justice where fair procedures may still yield unjust results. Our approach considers both outcome-oriented theories (efficient procedures minimizing error costs) and process-oriented theories (procedures holding intrinsic moral value by safeguarding dignity and rights).

**Step 2: Legal Tradition Selection**

We selected China and the United States to represent civil law and common law traditions respectively. Both systems share nine core procedural fairness principles based on Article 14 of the International Covenant on Civil and Political Rights (ICCPR):

| Principle | China Provisions | U.S. Provisions |
|---|---|---|
| **No Double Jeopardy** | CPL 253/254 – procedural rule, retrial | 5th Am. – constitutional bar |
| **Confront & Call Witnesses** | CPL 61/190/192 – judge-led | 6th Am.; Crawford – strict confrontation |
| **Right to Counsel** | CPL 34–36 – limited early access | 6th Am.; Gideon – absolute in felonies |
| **Right to Public Trial** | CPL 188 – stability exceptions | 6th/1st Am.; Richmond – strong openness |
| **Right to Speedy Trial** | CPL 91/156/208 – admin efficiency | Speedy Trial Act/ Barker – statutory limits |
| **No Self-Incrimination** | CPL 52/121 – no silence right | 5th Am.; Miranda – silence protected |
| **No Arbitrary Arrest** | Const 37; CPL 82/91 – police review | 4th Am.; due process/habeas – strict PC |
| **Presumption of Innocence** | CPL 12 – weak enforcement | due process; In re Winship – high burden |
| **Right to Impartial Trial** | CPL 29/31/32 – no jury, admin recusal | 6th Am.; 28 U.S.C. §§455/144 – jury, judge |

**Table: Comparative Analysis of Criminal Procedure Principles and Provisions: China vs. United States**

**Step 3: Dataset Construction**

**Procedural Component**: Created realistic scenarios from Chinese and U.S. criminal laws demonstrating violations of each procedural principle, highlighting the different implementation approaches across legal traditions.

**Substantive Component**: Used China's CAIL dataset (500 cases) and U.S. Multistate Bar Examination case facts (500 cases) due to privacy constraints.

**Data Scale**: China and the U.S. each contribute 500 cases, intersected with 9 procedural principles to form 9,000 data entries across three experiments.

**Step 4: Model Selection**

We evaluated five models to enable cross-cultural and capability-based comparisons:

- **Chinese Models**: DeepSeek V3, Qwen-2.5, DeepSeek R1 (reasoning-enhanced)
- **U.S. Models**: GPT-4o, Llama-3.3

All models were version-matched for fairness, with DeepSeek R1 vs. V3 comparison assessing reasoning impact.

### Experiment Execution

The experiment execution includes three main experiments with data processing and model evaluation steps.

#### E1: Procedural Fairness Awareness

**Chinese Dataset Processing:**
1. Place the Chinese raw dataset in `E1&E2/E1/data/500_test.json`
2. Run `E1&E2/E1/E1_generate_question.py` to construct principle-specific prompt datasets (4,500 entries) → outputs `prompts_E1.xlsx`

**English Dataset Processing:**
1. Place the English raw dataset in `E1&E2/E1/data/en_modified.json`
2. Run `E1&E2/E1/E1_generate_question_en.py` to construct principle-specific prompt datasets (4,500 entries) → outputs `prompts_E1_en.xlsx`

**Model Execution:**
Replace "**********" with corresponding API keys in the following files, then run sequentially:
- `get_answers_by_deepseek-r1.py`
- `get_answers_by_deepseek-v3.py`
- `get_answers_by_gpt_4o.py`
- `get_answers_by_llama-3.3.py`
- `get_answers_by_qwen-2.5.py`

**Input**: `data/prompts_E1.xlsx` (Chinese) and `data/prompts_E1_en.xlsx` (English)
**Output**: `E1_output/E1_en_results_XXX.xlsx`

#### E2: Procedural vs. Substantive Preference

**Chinese Dataset Processing:**
1. Place the Chinese raw dataset in `E1&E2/E2/data/500test.json`
2. Run `E1&E2/E2/E2_generate_question.py` to construct principle-specific prompt datasets (4,500 entries) → outputs `prompts_E2.xlsx`

**English Dataset Processing:**
1. Place the English raw dataset in `E1&E2/E2/data/en_modified.json`
2. Run `E1&E2/E2/E2_generate_question_en.py` to construct principle-specific prompt datasets (4,500 entries) → outputs `prompts_E2_en.xlsx`

**Model Execution:**
Follow the same process as E1, using the five model scripts with E2 prompts.

**Input**: `data/prompts_E2.xlsx` (Chinese) and `data/prompts_E2_en.xlsx` (English)
**Output**: `E2_output/E2_en_results_XXX.xlsx`

#### E3: Procedure Effect on Substantive Sentence

**Chinese Dataset Processing:**
1. Place Chinese raw dataset in `E3/cn/500_test.json`
2. Run `E3/cn/generate_question.py` to construct counterfactual prompt pairs → outputs `prompts_CN.xlsx`
3. Run the five model scripts (replace "**********" with API keys):
   - `get answers by deepseek-r1 plus.py`
   - `get answers by deepseek-v3.py`
   - `get answers by gpt-4o.py`
   - `get answers by llama-3.3.py`
   - `get answers by qwen-2.5.py`

Scripts automatically call `ean.py` to extract sentence length from model outputs.
**Output**: `results_xxxx.xlsx` in the same directory

**English Dataset Processing:**
1. Place English raw dataset in `E3/en/data/en.json`
2. Run sequentially:
   - `data_process.py` → outputs `en_modified.json`
   - `get_500_question_en.py` → outputs `en_question_list.json`
   - `generate_prompts_en.py` → outputs `prompts_EN.xlsx`
3. Run `E3/en/main.py`, selecting the corresponding model in tasks
**Output**: `E3/en/results/results_en/results_xxxx.xlsx`

### Metric Calculation

#### E1 & E2 Metrics Processing

Run the metrics calculation for experiments E1 and E2:

**Chinese Results:**
- `E1&E2/metrics/E1_metrics.xlsx`: First sheet contains statistical summary for all five models on Chinese dataset, followed by detailed statistics for each model
- `E1&E2/metrics/E2_metrics.xlsx`: Same structure for E2 Chinese results

**English Results:**
- `E1&E2/metrics/E1_metrics_en.xlsx`: Statistical summary and detailed results for English dataset E1
- `E1&E2/metrics/E2_metrics_en.xlsx`: Statistical summary and detailed results for English dataset E2

**Chi-Square Significance Testing:**
The first sheet in each metrics file contains five rectangular boxes calculating chi-square significance tests for the following group comparisons:
- M(R1) vs M(V3): DeepSeek R1 vs V3 comparison
- D(US) vs D(CN): U.S. vs Chinese dataset comparison  
- M(US) vs M(CN): U.S. vs Chinese model comparison
- D_US(R1,V3) vs D_CN(R1,V3): Dataset-version interaction
- D_US(M_US,M_CN) vs D_CN(M_US,M_CN): Dataset-model origin interaction

#### E3 Metrics Processing

Run `E3/Metrics/MPE&P.py` to calculate E3 metrics:

**Input Directories:**
- `result_CN`: Chinese experiment results
- `result_EN`: English experiment results

**Metrics Calculated:**
- **M_PA (Procedural Awareness)**: $M_{PA} = \frac{N_{No}}{N_{tot}}$
- **M_PV (Procedural vs. Substantive Preference)**: $M_{PV} = \frac{N_{B} - N_{A}}{N_{tot}}$
- **M_PE (Procedure Effect on Sentence)**: $M_{PE} = \frac{1}{n} \sum_{i=1}^{n}|d|$ where $d = S_{E32} - S_{E31}$

### Significance Testing Methods

Use **Statistical Significance Testing** to investigate whether there are statistically significant differences in models' procedural fairness alignment across different dimensions.

#### **Statistical Tests Applied**

1. **Chi-Square Tests**: Applied to Experiments E1 and E2 to evaluate variable independence across:
   - Legal traditions (Chinese vs. U.S. datasets)
   - Model origins (Chinese vs. U.S. models)
   - Model versions (DeepSeek R1 vs. V3)
   - Interaction effects

2. **Paired-Sample T-Tests**: Applied to Experiment E3 to compare sentencing under procedural violation vs. compliance scenarios

3. **Two-Way ANOVA**: Examined interaction effects between legal systems and model types on sentencing outcomes in E3

#### **Null Hypotheses (H0)**

1. **H0-1 (Legal Tradition Effect)**: No significant difference in procedural fairness perception between U.S. and Chinese datasets
2. **H0-2 (Model Origin Effect)**: No significant difference between U.S. and Chinese models in procedural fairness alignment
3. **H0-3 (Model Version Effect)**: No significant difference between reasoning (R1) and non-reasoning (V3) model versions
4. **H0-4 (Interaction Effects)**: No significant interaction between dataset legal tradition and model characteristics

#### **Result Interpretation**
- **p ≤ 0.001** → Label as **\*\*\*** (Highly significant)
- **0.001 < p ≤ 0.01** → Label as **\*\*** (Very significant)
- **0.01 < p ≤ 0.05** → Label as **\*** (Significant)
- **p > 0.05** → No annotation (Not significant)

### Visualization

Run the visualization scripts in the `plt` directory:

#### **Data Preparation**
- `plt/E1&E2`: E1 and E2 experiment results
- `plt/result_CN`: E3 Chinese experiment results  
- `plt/result_EN`: E3 English experiment results

#### **Visualization Scripts**
1. **Bar Charts**: Run `plt/E1&E2&E3_bar_pic.py` to generate comparative bar charts across experiments
2. **Significance Testing Visualization**: Run `plt/significant_testing_pic.py` to generate six significance testing visualizations showing statistical differences across dimensions

The visualization outputs demonstrate:
- Cross-tradition differences in procedural fairness perception
- Model-specific biases toward procedural vs. substantive justice
- Interaction effects between dataset legal traditions and model characteristics
- Statistical significance of observed differences across all experimental conditions
