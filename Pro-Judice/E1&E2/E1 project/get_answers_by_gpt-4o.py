from openai import OpenAI
import pandas as pd
import os

os.environ["http_proxy"] = 'http://127.0.0.1:7890'
os.environ["https_proxy"] = 'http://127.0.0.1:7890'

# 读取 Excel 文件
df = pd.read_excel('data/prompts_E1_en.xlsx', header=None, skiprows=1, nrows=4500)
case_id = df[0].tolist()
principle = df[1].tolist()
senario = df[2].tolist()
prompt = df[3].tolist()
answer = []
answer_value = []

client = OpenAI(
	api_key="***",
	base_url="https://api.openai.com/v1"
)

i_temp = 1
for pro in prompt:
	# try:
	response = client.chat.completions.create(
		model="gpt-4o",
		messages=[
			{"role": "system", "content": "You are a helpful assistant"},
			{"role": "user", "content": pro + "\nStrictly limit your reply format to one of the following: Yes or No"},
		],
		stream=False
	)
	# res = response.output_text
	res = response.choices[0].message.content
	# if isinstance(res, str):
	# 	answer.append(res)
	# 	value_list = ean.extract_all_numbers(res)
	# 	if len(value_list) == 0:
	# 		answer_value.append("")
	# 	else:
	# 		answer_value.append(value_list[-1])
	# else:
	# 	answer.append("")
	# 	answer_value.append("")
	answer.append(res)
	print("gpt第", i_temp, "次已完成")
	i_temp = i_temp + 1
	# except:
	# 	answer.append("")
	# 	answer_value.append("")
	# 	print("gpt第", i_temp, "次失败")
	# 	i_temp = i_temp + 1

data = {
	'CaseId': case_id,
	'Principle': principle,
	'Senario': senario,
	'prompt': prompt,
	'answer': answer
}

df = pd.DataFrame(data)
df.to_excel('E2_output_en/E2_en_results_gpt-4o.xlsx', index = False)
print("表格已保存至 E2_output_en/E2_en_results_gpt-4o.xlsx.")