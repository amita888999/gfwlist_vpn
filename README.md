# gfwlist_vpn

本项目是生成一个GFW屏蔽网址的列表，供有特殊需要的方面使用，
[gfwlist](https://github.com/gfwlist/gfwlist) 中生成文件是特殊格式压缩的，还带有特殊的前缀，不能直接使用，可以使用本项目生成列表文件。

## 使用方法

- 本地库依赖 base64; re; requests;

- 获得项目后执行

```python
python main.py
```

- 查看 res/whitelist.txt 文件

- 如果网络无法访问，修改 main.py 中 gfwlist_url 为可访问的地址，从
[gfwlist](https://github.com/gfwlist/gfwlist) 中查询

## 已知应用

- sslspeedy2 (vpnsoso)

- 各类针对防火墙的规则，正则表达式匹配即可