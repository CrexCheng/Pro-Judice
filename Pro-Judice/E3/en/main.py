from concurrent.futures import ThreadPoolExecutor
import llm_qa_process as lp

tasks = [
	("llama-3.3", "meta-llama/llama-3.3-70b-instruct", "**********"
	, "https://openrouter.ai/api/v1", "results/results_llama-3.3.xlsx"),
	# ("qwen-2.5", "qwen2.5-72b-instruct", "**********"
	#  , "https://dashscope.aliyuncs.com/compatible-mode/v1", "results/results_qwen-2.5.xlsx"),
	# ("deepseek-v3", "deepseek-chat", "**********"
	# , "https://api.deepseek.com", "results/results_deepseek-v3.xlsx"),
	# ("deepseek-r1", "deepseek-reasoner", "**********"
	# , "https://api.deepseek.com", "results/results_deepseek-r1.xlsx")
]

def main():
	if len(tasks) > 5:
		print("线程数大于5，请人工复查后重新运行代码")
		return
	print(f"启动 {len(tasks)} 个并行数据处理任务")
	failed_tasks = []

	with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
		# 提交所有任务
		futures = {executor.submit(lp.get_answers_by_llm, *task): task for task in tasks}

		# 等待并检查所有任务
		for future in futures:
			task_params = futures[future]
			try:
				future.result()  # 仅用于捕获异常
				print(f"!!!!任务成功: {task_params[0]}")
			except Exception as e:
				failed_tasks.append(task_params)
				print(f"!!!!任务失败: {task_params[0]} - {e}")

	# 结果统计
	success_count = len(tasks) - len(failed_tasks)
	print(f"\n处理完成! 成功: {success_count}, 失败: {len(failed_tasks)}")

	if failed_tasks:
		print("失败的任务:")
		for task in failed_tasks:
			print(f"  - {task[0]}")

if __name__ == "__main__":
	main()