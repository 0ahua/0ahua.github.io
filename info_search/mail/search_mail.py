import whois

def get_domain_email(domain):
    try:
        # 查询域名注册信息
        domain_info = whois.whois(domain)

        # 提取注册人邮箱信息
        emails = domain_info.emails

        if emails:
            print("关联邮箱信息：")
            for email in emails:
                print(email)
        else:
            print("无关联邮箱信息")

        # Write emails to email.txt file
        with open("E:\python\FinalProject\info_search\\result\email.txt", "w",encoding='utf-8') as file:
            if emails:
                file.write("关联邮箱信息：\n")
                file.write("".join(emails))
            else:
                file.write("无关联邮箱信息")

    except Exception as e:
        print("发生错误：", e)

# Example usage
get_domain_email("jd.com")