import json

# 定义输入和输出文件名
input_file = 'en_modified.json'
output_file = 'en_question_list.json'

# 读取原始JSON文件
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 提取question字段值，保持索引一致
question_list = [item["question"] for item in data]

# 将提取的数据写入新文件
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(question_list, f, indent=2, ensure_ascii=False)

print(f"处理完成！已生成 {output_file}")
print(f"提取了 {len(question_list)} 个问题，保持与原始数据索引一致")