import json


def remove_last_sentence(text):
	"""移除文本的最后一句话（基于最后一个句号位置）"""
	# 找到最后一个句号的位置
	last_period_index = text.rfind('.')

	# 如果找到句号，截取到该位置（包括句号）
	if last_period_index != -1:
		return text[:last_period_index + 1]
	return text


# 定义输入和输出文件名
input_file = 'en.json'
output_file = 'en_modified.json'

# 读取原始JSON文件
with open(input_file, 'r', encoding='utf-8') as f:
	data = json.load(f)

# 处理每个元素中的question字段
for item in data:
	if "question" in item:
		# 移除最后一句话
		item["question"] = remove_last_sentence(item["question"])

# 将修改后的数据写入新文件
with open(output_file, 'w', encoding='utf-8') as f:
	json.dump(data, f, indent=2, ensure_ascii=False)

print(f"处理完成！已生成 {output_file}")