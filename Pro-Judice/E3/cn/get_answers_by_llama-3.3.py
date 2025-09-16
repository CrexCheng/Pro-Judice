from openai import OpenAI
import pandas as pd
import ean

# 读取 Excel 文件
df = pd.read_excel('prompts_CN.xlsx', header=None, skiprows=1)
case_id = df[0].tolist()
principle = df[1].tolist()
experiment = df[2].tolist()
answer = []
answer_value = []
prompt = df[4].tolist()

client = OpenAI(
	api_key="**********",
	base_url="https://api.llmapi.com"
)

i_temp = 1
for pro in prompt:
	try:
		response = client.chat.completions.create(
			model="llama3.3-70b",
			messages=[
				{"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
				{"role": "user", "content": pro + "\n严格限制你的回复格式必须有且仅有：x个月"}
			],
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
		print("llama第", i_temp, "次已完成")
		i_temp = i_temp + 1
	except:
		answer.append("")
		answer_value.append("")
		print("llama第", i_temp, "次失败")
		i_temp = i_temp + 1

data = {
    'CaseId' : case_id,
    'Principle' : principle,
    'Experiment' : experiment,
    'answer' : answer,
	'answerValue' : answer_value,
    'prompt' : prompt
}

df = pd.DataFrame(data)
df.to_excel('results_llama-3.3.xlsx', index = False)
print("表格已保存至 results_llama-3.3.xlsx.")
