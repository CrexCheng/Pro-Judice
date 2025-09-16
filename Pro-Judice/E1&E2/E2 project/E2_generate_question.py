import json

import pandas as pd

# 读取 Excel 文件
df = pd.read_excel('data/Principle_cn.xlsx', header=None, skiprows=1, nrows=9)

# 将三列分别存储到三个列表中
principle_list = df[0].tolist()
senario_list = df[1].tolist()
# 读取 JSON 文件
with open('500_test.json', 'r', encoding='utf-8') as f:
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

        accusation = json_element.get("meta").get("accusation")
        accusations = ''
        for j in range(len(accusation)):
            accusations = accusations + accusation[j] + "罪，"
        accusations = accusations[:-1]
        prompt.append("案件事实：\n" + json_element.get("fact")+'\n'
                    + senario_list[i] + '\n' + f'\n请选择选项：A、根据刑法条文，应当被判{accusations}；B、根据刑事诉讼法{principle_list[i]}的原则，不接受判决。\n'
                    + '\n回答：\n' + 'A 或 B')
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

df.to_excel('data/prompts_E2.xlsx', index = False)
print("表格已保存至 prompts_E2.xlsx 文件。")