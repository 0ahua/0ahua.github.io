import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import threading
# tkinter用于创建GUI界面，messagebox用于显示消息框，ttk用于创建进度条，threading用于执行多线程操作。

# 导入其他模块
from figerinfo import search_thumbprint as figer
from mail import search_mail as mail
from port import scanPort as po
from port.scanPort import port_file, port_info
from record import check as record
from record.check import api_key
from ssl_certi import search_ssl as ssl
from ssl_certi.search_ssl import port


class ScanGUI:
    def __init__(self):
        # GUI界面的初始化代码
        self.root = tk.Tk()     # 创建一个根窗口对象，即主窗口
        self.root.title("扫描程序")     # 设置主窗口的标题为"扫描程序"
        self.progress_var = tk.DoubleVar()      # 创建一个DoubleVar对象，用于存储进度条的进度值
        self.progress_label = tk.Label(self.root, text="当前进度：")     # 创建一个Label标签，用于显示"当前进度："的文本
        self.progress_text = tk.StringVar()     # 创建一个StringVar对象，用于存储当前进度的文本值
        self.progress_text.set("等待开始...")
        # 创建一个Label标签，用于显示当前进度的文本
        self.progress_text_label = tk.Label(self.root, textvariable=self.progress_text)
        # 创建一个Progressbar进度条，使用self.progress_var作为变量，设置最大值为100
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100)
        # 创建一个Label标签，用于显示"已生成的文件："的文本
        self.file_label = tk.Label(self.root, text="已生成的文件：")
        # 创建一个Text文本框，用于显示已生成的文件列表
        self.file_text = tk.Text(self.root, height=10, width=50)
        # 创建一个Label标签，用于显示"请输入域名："的文本
        self.domain_label = tk.Label(self.root, text="请输入域名：")
        # 创建一个Entry输入框，用户可以在此输入域名
        self.domain_entry = tk.Entry(self.root)
        # 创建一个Button按钮，显示"开始扫描"的文本，并设置点击按钮时执行self.start_scan方法
        self.scan_button = tk.Button(self.root, text="开始扫描", command=self.start_scan)
        # 创建一个Button按钮，显示"查看结果"的文本，并设置为初始状态不可用，点击按钮时执行self.show_result方法
        self.result_button = tk.Button(self.root, text="查看结果", state=tk.DISABLED, command=self.show_result)

        self.progress_label.pack()
        self.progress_text_label.pack()
        self.progress_bar.pack(fill=tk.X, padx=10, pady=5)
        self.file_label.pack()
        self.file_text.pack()
        self.domain_label.pack()
        self.domain_entry.pack()
        self.scan_button.pack(pady=10)
        self.result_button.pack(pady=5)

    def update_progress(self, progress, step):
        # 更新进度条和当前进度文本的方法
        self.progress_var.set(progress)     # 使用 set 方法将进度条的变量 self.progress_var 设置为指定的 progress 值，从而更新进度条的进度
        self.progress_text.set(step)        # 使用 set 方法将当前进度文本的变量 self.progress_text 设置为指定的 step 值，从而更新当前进度文本的显示

    def update_file_list(self, file):
        # 更新文件列表的方法
        # 将指定的 file 文件名插入到文件列表的文本框中的最后，加上换行符 "\n"，以实现文件名的换行显示
        self.file_text.insert(tk.END, file + "\n")

    def start_scan(self):
        # 开始扫描的方法
        self.scan_button.config(state=tk.DISABLED)      # 将扫描按钮设置为禁用状态，防止用户重复点击开始扫描
        self.result_button.config(state=tk.DISABLED)        # 将结果按钮设置为禁用状态，防止用户在扫描过程中查看结果
        self.file_text.delete(1.0, tk.END)  # 清空文件列表

        domain = self.domain_entry.get()  # 从文本框获取域名
        scan_thread = threading.Thread(target=self.perform_scans, args=(domain,))       # 创建一个线程对象，目标函数为self.perform_scans
        scan_thread.start()

    def perform_scans(self, domain):
        # 执行扫描任务
        self.update_progress(10, "正在执行 figerinfo 扫描...")
        figer.get_header_info(domain)
        self.update_file_list("result/figerinfo.txt")

        self.update_progress(20, "正在执行邮件扫描...")
        mail.get_domain_email(domain)
        self.update_file_list("result/email.txt")

        # path.scan_and_write_paths(domain, directories, path_file)
        # self.update_progress(30, "正在执行路径扫描...")
        # self.update_file_list("path.txt")

        self.update_progress(40, "正在执行端口扫描...")
        po.scan_ports_multithreaded(domain, port_info, port_file)
        self.update_file_list("result/port.txt")

        self.update_progress(50, "正在执行备案信息查询...")
        record.show_icp_info(domain, api_key)
        self.update_file_list("info_search/result/record.txt")

        #self.update_progress(60, "正在执行子域名扫描(此处需等待约1min)...")
        #sub.show_subdomains(domain, subdomains_file)
        #self.update_file_list("subdomain.txt")

        self.update_progress(70, "正在执行 SSH 证书查询...")
        ssl.get_certificate_info(domain, port)
        self.update_file_list("info_search/result/ssh.txt")

        # 扫描完成
        self.scan_button.config(state=tk.NORMAL)
        self.result_button.config(state=tk.NORMAL)
        self.update_progress(100, "扫描已完成")

    def show_result(self):
        result_window = tk.Toplevel(self.root)
        result_window.title("扫描结果")

        # 创建复选框
        checkbox_texts = ["figerinfo.txt", "mail.txt", "port.txt", "check.txt", "ssl_certi.txt"]  # 每个复选框的文本内容
        checkbox_vars = [tk.BooleanVar() for _ in range(5)]
        checkboxes = []
        for i, var in enumerate(checkbox_vars):
            checkbox = tk.Checkbutton(result_window, text=checkbox_texts[i], variable=var)
            checkbox.pack(anchor=tk.W)
            checkboxes.append(checkbox)

        # 创建查看按钮
        view_button = tk.Button(result_window, text="查看", command=lambda: self.view_files(checkbox_vars))
        view_button.pack()

    def view_files(self, checkbox_vars):
        # enumerate(checkbox_vars) 遍历了名为 checkbox_vars 的列表，并返回每个元素以及对应的索引。
        # if var.get() 判断当前复选框的状态是否为选中（即返回值为 True）。
        # [i+1 for i, var in enumerate(checkbox_vars) if var.get()] 使用列表推导式，将满足条件的索引（加1）添加到 selected_files 列表中。
        # selected_files = [i+1 for i, var in enumerate(checkbox_vars) if var.get()]
        selected_files = []
        for i, var in enumerate(checkbox_vars):
            if var.get():
                selected_files.append(i + 1)

        for file_num in selected_files:
            if file_num == 1:
                file_name = "result/figerinfo.txt"
            elif file_num == 2:
                file_name = "result/email.txt"
            elif file_num == 3:
                file_name = "result/port.txt"
            elif file_num == 4:
                file_name = "result/check.txt"
            elif file_num == 5:
                file_name = "info_search/result/ssh.txt"
            # 可以根据需要继续添加其他文件的处理逻辑

            # 打开对应的.txt文件并显示内容
            with open(file_name, "r", encoding='utf-8') as f:
                file_content = f.read()
            messagebox.showinfo("文件内容", file_content)


if __name__ == "__main__":
    gui = ScanGUI()
    gui.root.mainloop()
