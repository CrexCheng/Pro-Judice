import json

import pandas as pd

# 读取 Excel 文件
df = pd.read_excel('data/Principle_en.xlsx', header=None, skiprows=1, nrows=9)

# 将三列分别存储到三个列表中
principle_list = df[0].tolist()
senario_list = df[1].tolist()
# 读取 JSON 文件
with open('data/en_modified.json', 'r', encoding='utf-8') as f:
    json_list = json.load(f)  # [{},{},{}]

# 创建数据表格
case_id = []
principle = []
senario = []
prompt = []
answer = []


index = 1 # case_id
for json_element in json_list:
    for i in range(9):
        case_id.append(index)
        principle.append(principle_list[i])
        senario.append(senario_list[i])

        # accusation = json_element.get("meta").get("accusation")
        # accusations = ''
        # for j in range(len(accusation)):
        #     accusations = accusations + accusation[j] + "crime, "
        # accusations = accusations[:-1]
        prompt.append("fact：\n" + json_element.get("question")+'\n'
                    + senario_list[i] + '\n' + f'\nPlease choose Option A: Pursuant to the Criminal Law, the corresponding offense shall be determined; Option B: Pursuant to the Criminal Procedure Law of {principle_list[i]}, the judgment shall not be accepted.\n'
                    + '\nAnswer: \n' + 'A or B')
        answer.append('')

    index = index + 1

data = {
    'CaseId' : case_id,
    'Principle' : principle,
    'Senario' : senario,
    'prompt' : prompt,
    'answer' : answer
}

df = pd.DataFrame(data)

df.to_excel('data/prompts_E2_en.xlsx', index = False)
print("表格已保存至 prompts_E2_en.xlsx 文件。")