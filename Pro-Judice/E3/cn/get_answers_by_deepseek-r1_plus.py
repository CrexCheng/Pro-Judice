from openai import OpenAI
import pandas as pd
import ean


start_row = 8426
# 读取 Excel 文件
df = pd.read_excel('prompts_CN.xlsx', header=None, skiprows=start_row)
case_id = df[0].tolist()
principle = df[1].tolist()
experiment = df[2].tolist()
answer = []
answer_value = []
prompt = df[4].tolist()

client = OpenAI(api_key="**********", base_url="https://api.deepseek.com")

i_temp = start_row
result_file = 'results_deepseek-r1.xlsx'

# 检查文件是否存在，如果存在就先读取已有的数据
try:
    existing_df = pd.read_excel(result_file)
except FileNotFoundError:
    existing_df = None

for pro in prompt:
    try:
        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": pro + "\n严格限制你的回复格式必须有且仅有：x个月\n（其中，x由阿拉伯数字组成）"},
            ],
            stream=False
        )
        res = response.choices[0].message.content
        if isinstance(res, str):
            answer.append(res)
            value_list = ean.extract_all_numbers(res)
            if len(value_list) == 0:
                answer_value.append("")
            else:
                answer_value.append(value_list[-1])
        else:
            answer.append("")
            answer_value.append("")
        print("ds-r1第", i_temp, "次已完成")
        # i_temp = i_temp + 1
    except:
        answer.append("")
        answer_value.append("")
        print("ds-r1第", i_temp, "次失败")
        # i_temp = i_temp + 1

    # 每次循环迭代后保存到文件中
    data = {
        'CaseId': [case_id[i_temp-start_row]],
        'Principle': [principle[i_temp-start_row]],
        'Experiment': [experiment[i_temp-start_row]],
        'answer': [answer[i_temp-start_row]],
        'answerValue': [answer_value[i_temp-start_row]],
        'prompt': [prompt[i_temp-start_row]]
    }

    df_row = pd.DataFrame(data)

    # 如果文件存在，就追加写入，否则就新建文件
    if existing_df is not None:
        # 每次写入前重新读取文件，以确保数据是最新的
        existing_df = pd.read_excel(result_file)
        existing_df = pd.concat([existing_df, df_row])
        existing_df.to_excel(result_file, index=False)
    else:
        df_row.to_excel(result_file, index=False)
        existing_df = pd.read_excel(result_file)

    print("ds-r1第", i_temp, "条数据已保存至 results_deepseek-r1.xlsx")
    i_temp = i_temp + 1

print("表格已保存至 results_deepseek-r1.xlsx.")