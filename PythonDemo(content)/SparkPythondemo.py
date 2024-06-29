# coding: utf-8
import SparkApi
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import time
import threading

appid = "******"
api_secret = "*************************************"
api_key = "*************************************"
domain = "generalv3.5"
Spark_url = "wss://spark-api.xf-yun.com/v3.5/chat"

text = [
    {"role": "system", "content": "你现在是渗透测试课的老师，接下来请以这个身份回答我的问题"},
    # {"role": "user", "content": "你是谁"},
    # {"role": "assistant", "content": "....."},
]


def getText(role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text


def send_message():
    question = checklen(getText("user", input_box.get()))
    SparkApi.answer = ""
    print("星火：", end="")

    def execute_spark_api():
        SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
        getText("assistant", SparkApi.answer)
        output_box.insert(tk.END, "我： " + input_box.get() + "\n")
        output_box.insert(tk.END, "星火： " + SparkApi.answer + "\n")
        input_box.delete(0, tk.END)

    threading.Thread(target=execute_spark_api).start()
    '''
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
    getText("assistant", SparkApi.answer)
    output_box.insert(tk.END, "我： " + input_box.get() + "\n")

    output_box.insert(tk.END,"星火： " + SparkApi.answer + "\n")
    input_box.delete(0, tk.END)
    '''




if __name__ == '__main__':
    root = tk.Tk()
    root.title("渗透测试小客服")
    root.geometry("600x400")  # 设置窗口大小

    input_frame = tk.Frame(root, bg="lightblue", bd=5)  # 设置背景颜色和边框宽度
    input_frame.pack(pady=10)

    input_label = tk.Label(input_frame, text="我：", font=("宋体", 12), bg="lightblue")
    input_label.pack(side=tk.LEFT)

    input_box = tk.Entry(input_frame, width=50, font=("宋体", 12))
    input_box.pack(side=tk.LEFT)

    send_button = tk.Button(input_frame, text="发送", command=send_message, font=("宋体", 12), bg="lightgreen", relief=tk.GROOVE)
    send_button.pack(side=tk.LEFT)

    output_frame = tk.Frame(root, bg="lightblue", bd=5)
    output_frame.pack()

    output_box = ScrolledText(output_frame, wrap=tk.WORD, width=60, height=20, font=("宋体", 12), bg="white", fg="black", relief=tk.SUNKEN)
    output_box.pack()

    root.mainloop()
