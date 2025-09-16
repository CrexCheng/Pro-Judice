import pandas as pd
from openai import OpenAI
import re

def extract_all_numbers(s):
    """
    从字符串中提取所有连续的数字。

    参数:
    s -- 输入字符串

    返回:
    一个包含所有连续数字的列表。
    """
    return re.findall(r'\d+', s)

def get_answers_by_llm(llm_name, model, api_key, base_url, result_file):
    start_row = 1
    # 检查文件是否存在，如果存在就先读取已有的数据
    try:
        existing_df = pd.read_excel(result_file)
        start_row = len(existing_df) + 1
    except FileNotFoundError:
        existing_df = None
    # 读取 Excel 文件
    df = pd.read_excel('data/prompts_new_EN.xlsx', header=None, skiprows=start_row)
    case_id = df[0].tolist()
    principle = df[1].tolist()
    experiment = df[2].tolist()
    answer = []
    answer_value = []
    prompt = df[4].tolist()

    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    i_temp = start_row
    for pro in prompt:
        try:
            response = client.responses.create(
                model=model,
                input=pro + "\nStrictly limit your response format to only: x months\nAmong which, x must consist of Arabic numerals.You cannot avoid answering the question and must provide the value of x."
            )
            res = response.output_text
            if isinstance(res, str):
                answer.append(res)
                value_list = extract_all_numbers(res)
                if len(value_list) == 0:
                    answer_value.append("")
                else:
                    answer_value.append(value_list[-1])
            else:
                answer.append("")
                answer_value.append("")
            print(llm_name, "第", i_temp, "次已完成")
        except:
            answer.append("")
            answer_value.append("")
            print(llm_name, "第", i_temp, "次失败")

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

        print(llm_name, "第", i_temp, "条数据已保存至 ", result_file)
        i_temp = i_temp + 1
    print("结果已保存至 ", result_file)


get_answers_by_llm("gpt-4o", "gpt-4o"
				   , "**********"
				   , "https://api.openai.com/v1", "results/results_gpt-4o.xlsx")