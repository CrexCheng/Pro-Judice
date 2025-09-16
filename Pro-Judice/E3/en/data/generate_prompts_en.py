import json

import pandas as pd

# 读取 Excel 文件
df = pd.read_excel('Principle_english.xlsx', header=None, skiprows=1, nrows=9)

# 将三列分别存储到三个列表中
principle_list = df[1].tolist()
experiment_3_1_list = df[3].tolist()
experiment_3_2_list = df[5].tolist()
# 读取 JSON 文件
with open('en_question_list.json', 'r', encoding='utf-8') as f:
    json_list = json.load(f)  # [{},{},{}]

# 创建数据表格
case_id = []
principle = []
experiment = []
answer = []
prompt = []

index = 1 # case_id
for json_element in json_list:
    for i in range(9):
        case_id.append(index)
        principle.append(principle_list[i])
        experiment.append('E_3_1')
        answer.append('')
        prompt.append("Case facts:\n" + json_element+'\n'
                    + experiment_3_1_list[i] + '\n' + '\nPlease estimate a likely the term of imprisonment，estimate a likely prison sentence and give only one final number in months.\n'
                    + '\nAnswer:\n' + '【】months.')

        case_id.append(index)
        principle.append(principle_list[i])
        experiment.append('E_3_2')
        answer.append('')
        prompt.append("Case facts:\n" + json_element + '\n' + '\n'
                      + experiment_3_2_list[
                          i] + '\n' + '\nPlease estimate a likely the term of imprisonment，estimate a likely prison sentence and give only one final number in months.\n'
                      + '\nAnswer:\n' + '【】months.')
    index = index + 1

data = {
    'CaseId' : case_id,
    'Principle' : principle,
    'Experiment' : experiment,
    'answer' : answer,
    'prompt' : prompt
}

df = pd.DataFrame(data)

df.to_excel('prompts_EN.xlsx', index = False)
print("表格已保存至 prompts_EN.xlsx 文件。")