import json

import pandas as pd

# 读取 Excel 文件
df = pd.read_excel('Principle.xlsx', header=None, skiprows=1, nrows=9)

# 将三列分别存储到三个列表中
principle_list = df[0].tolist()
experiment_3_1_list = df[1].tolist()
experiment_3_2_list = df[2].tolist()
# 读取 JSON 文件
with open('500_test.json', 'r', encoding='utf-8') as f:
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
        prompt.append("案件事实：\n" + json_element.get("fact")+'\n'
                    + experiment_3_1_list[i] + '\n' + '\n请回答刑期，精确到几个月，如36个月。\n'
                    + '\n回答：\n' + '【】个月。')

        case_id.append(index)
        principle.append(principle_list[i])
        experiment.append('E_3_2')
        answer.append('')
        prompt.append("案件事实：\n" + json_element.get("fact") + '\n' + '\n'
                      + experiment_3_2_list[i] + '\n' + '\n请回答刑期，精确到几个月，如36个月。\n'
                      + '\n回答：\n' + '【】个月。')
    index = index + 1

data = {
    'CaseId' : case_id,
    'Principle' : principle,
    'Experiment' : experiment,
    'answer' : answer,
    'prompt' : prompt
}

df = pd.DataFrame(data)

df.to_excel('prompts_CN.xlsx', index = False)
print("表格已保存至 prompts_CN.xlsx 文件。")