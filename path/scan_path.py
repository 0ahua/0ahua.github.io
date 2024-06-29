import tkinter as tk
from tkinter import filedialog
import requests
from tkinter import ttk

def scan_website_directory():
    domain = domain_entry.get()
    directory_file = directory_var.get()

    base_url = f"{domain}"
    with open(directory_file, 'r', encoding='utf-8') as file:
        directories = file.read().splitlines()

    result_text.delete('1.0', tk.END)  # 清空输出文本框内容

    progress_bar['maximum'] = len(directories)
    progress_bar['value'] = 0

    for i, directory in enumerate(directories, start=1):
        url = f"{base_url}/{directory}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                result_text.insert(tk.END, f"Directory found: {url}\n")
            else:
                #result_text.insert(tk.END, f"Directory not found: {url}\n")
                pass
        except requests.exceptions.RequestException:
            result_text.insert(tk.END, f"Connection error: {url}\n")

        progress_bar['value'] = i
        progress_label.config(text=f"Progress: {i}/{len(directories)}")
        window.update()  # 处理窗口事件
        # 或者使用 window.update_idletasks()，根据需要选择其中之一

def browse_directory_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        directory_var.set(file_path)

# 创建主窗口
window = tk.Tk()
window.title("网站目录扫描工具")

# 域名输入框
domain_label = tk.Label(window, text="网址:")
domain_label.pack()
domain_entry = tk.Entry(window)
domain_entry.pack()

# 目录字典选择
directory_label = tk.Label(window, text="目录字典:")
directory_label.pack()
directory_var = tk.StringVar()
directory_entry = tk.Entry(window, textvariable=directory_var, state='readonly')
directory_entry.pack()

# 浏览按钮
browse_button = tk.Button(window, text="浏览", command=browse_directory_file)
browse_button.pack()

# 开始扫描按钮
scan_button = tk.Button(window, text="开始扫描", command=scan_website_directory)
scan_button.pack()

# 进度条
progress_frame = tk.Frame(window)
progress_frame.pack(pady=10)
progress_label = tk.Label(progress_frame, text="Progress: 0/0")
progress_label.pack(side=tk.LEFT)
progress_bar = ttk.Progressbar(progress_frame, mode='determinate', length=400)
progress_bar.pack()

# 扫描结果输出
result_label = tk.Label(window, text="扫描结果:")
result_label.pack()
result_text = tk.Text(window, height=30, width=80)
result_text.pack()

window.mainloop()