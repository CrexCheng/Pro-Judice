from openai import OpenAI
import pandas as pd
import json

# 读取 Excel 文件
df = pd.read_excel('data/prompts_E1_en.xlsx', header=None, skiprows=1, nrows=1000)
case_id = df[0].tolist()
principle = df[1].tolist()
senario = df[2].tolist()
prompt = df[3].tolist()
answer = []
answer_value = []

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key="***",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


i_temp = 1
for pro in prompt:
    try:
        completion = client.chat.completions.create(
            model="qwen2.5-72b-instruct",
            # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': pro + "\nStrictly limit your reply format to one of the following: Yes or No"}],
        )
        res = json.loads(completion.model_dump_json()).get("choices")[0].get("message").get("content")
        res = res[0]
        # if isinstance(res, str):
        #     answer.append(res)
        #     value_list = ean.extract_all_numbers(res)
        #     if len(value_list) == 0:
        #         answer_value.append("")
        #     else:
        #         answer_value.append(value_list[-1])
        # else:
        #     answer.append("")
        #     answer_value.append("")
        answer.append(res)
        print("qwen第", i_temp, "次已完成")
        i_temp = i_temp + 1
    except:
        answer.append("")
        answer_value.append("")
        print("qwen第", i_temp, "次失败")
        i_temp = i_temp + 1


data = {
    'CaseId': case_id,
    'Principle': principle,
    'Senario': senario,
    'prompt': prompt,
    'answer': answer
}

df = pd.DataFrame(data)
df.to_excel('E2_output_en/E2_en_results_qwen-2.5.xlsx', index = False)
print("表格已保存至 E2_output_en/E2_en_results_qwen-2.5.xlsx.")

