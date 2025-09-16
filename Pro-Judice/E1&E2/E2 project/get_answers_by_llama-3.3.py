from openai import OpenAI
import pandas as pd

# 读取 Excel 文件
df = pd.read_excel('data/prompts_E2_en.xlsx', header=None, skiprows=1, nrows=4500)
case_id = df[0].tolist()
principle = df[1].tolist()
senario = df[2].tolist()
prompt = df[3].tolist()
answer = []
answer_value = []

client = OpenAI(
    api_key="***",
    base_url="https://openrouter.ai/api/v1"
)

i_temp = 1
for pro in prompt:
	try:
		response = client.chat.completions.create(
			model="meta-llama/llama-3.3-70b-instruct",
			messages=[
				{"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
				{"role": "user", "content": pro + "\nStrictly limit your reply format to one of the following: A or B"}
			],
		)
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
    'Senario' : senario,
    'prompt' : prompt,
	'answer' : answer
}

df = pd.DataFrame(data)
df.to_excel('E2_output_en/E2_en_results_llama-3.3.xlsx', index = False)
print("表格已保存至 E2_output_en/E2_en_results_llama-3.3.xlsx.")
