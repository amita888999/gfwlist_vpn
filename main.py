import base64
import re
import requests

################################################################################
# 获取原始文件的项目
# https://github.com/gfwlist/gfwlist

# 网络上的原始文件 可从https://github.com/gfwlist/gfwlist获得
# 这个地址必须是本机可以访问的地址
gfwlist_url = 'https://bitbucket.org/gfwlist/gfwlist/raw/HEAD/gfwlist.txt'

# 编码的原始文件
gfwlist_base64_file = "res/base64.txt"

# 编码的转换文件
gfwlist_base64_convert_file = "res/base64_convert.txt"

# 生成的白名单文件
out_whitelist_file = "res/block_domain.txt"


################################################################################

# 删除多余部分，非法字符删除，空行不处理，至少有一个点，头部点删除，/符号后的内容删除，只保留域名部分
def deal_part(part):
    if part.startswith("!"):
        return False

    deal_sign = ["@", "|", "http://", "https://"]

    if len(part) == 0:
        return False

    part = part.replace("%2F", "/")

    for s in deal_sign:
        part = part.replace(s, "")

    if part.startswith("."):
        part = part[1:]

    if part.find(".") < 0:
        return False

    i = part.find("/")
    if i >= 0:
        part = part[:i]

    # 处理通配符 *，只处理头部出现的即可
    star_regex = r'^[a-zA-Z0-9-_]*\*[a-zA-Z0-9-_]*\.'
    part = re.sub(star_regex, "", part)

    if len(part) == 0:
        return False

    # 正则表达式判定是否为合法域名
    domain_regex = r'^([a-zA-Z0-9]([a-zA-Z0-9-_]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z0-9-_]{2,20}(:[0-9]{1,5})?$'
    if not re.match(domain_regex, part):
        # print("error domain:", part)
        return False

    return part


# 处理一行
def deal_line(coll, line_content):
    # 包含此文字后的不处理
    end_string = "General List End"
    parts = line_content.split("\n")
    line_no = 0
    for part in parts:
        line_no += 1
        if part.find(end_string) >= 0:
            # 停止处理
            print("停止处理行:", line_no)
            return
        if part.startswith("!"):
            continue
        p = deal_part(part)
        if p:
            coll.append(p)


# 处理内容
def deal_content(line_content):
    coll = []
    deal_line(coll, line_content)
    # 对结果去重
    no_repeat = []
    for item in coll:
        if len(no_repeat) == 0 or no_repeat[-1] != item:
            no_repeat.append(item)
    return no_repeat


# 解析文本文件
def get_firewall_content_from_file(file):
    all_base64 = []
    with open(file) as f:
        for line in f.readlines():
            all_base64.append(line)
    line_content = str(base64.b64decode("".join(all_base64)), encoding='utf-8')

    return deal_content(line_content)


# 解析网络路径
def get_firewall_content_from_url(url):
    page = requests.get(url).text
    with open(gfwlist_base64_file, "w", encoding="utf-8") as f:
        f.write(page)
        print("写入文件", gfwlist_base64_file)
    base64_content = page.replace("\n", "")
    line_content = str(base64.b64decode(base64_content), encoding='utf-8')
    with open(gfwlist_base64_convert_file, "w", encoding="utf-8") as f:
        f.write(line_content)
        print("写入文件", gfwlist_base64_convert_file)
    return deal_content(line_content)


# 写入文件
def write_file(coll, file):
    with open(file, "w", encoding="utf-8") as f:
        for item in coll:
            f.write(item)
            f.write("\n")


if __name__ == '__main__':
    print('开始处理')
    url = gfwlist_url
    file = out_whitelist_file
    # print(get_firewall_content_from_file("res/gfwlist.txt"))
    # print(get_firewall_content_from_url(url))
    print("网络访问", url)
    domain_list = get_firewall_content_from_url(url)
    print("写入文件", file)
    write_file(domain_list, file)
    print('结束处理')
