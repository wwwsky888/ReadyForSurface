# ReadyForSurface
微软商城·官翻版Surface Pro 8补货通知

 - 本仓库用于候补**微软商城**·`官翻版Surface Pro 8`，当产品补货时，会通过邮件自动发送通知到指定邮箱。

---

## 使用方法

- Fork本仓库
- 设置Secrets
   - 进入你Fork后仓库的Settings
   - 添加Secrets
     - `Name`：`conf`
     - `Value`:
  ```
  '{"m_filter": [["5483", "5919"], ["5928"]], "senderMail": {"addr": "example@exapmle.com", "passwd": "ExamplePassWd", "host": "smtp.example.com", "port": "587"}, "rcvMails": ["example@qq.com"]}'
  ```
  - [说明]
    - `m_filter`字段可选值（**非空**）：
      - 第一个列表（颜色）
        - `"5483"`：`亮铂金`
        - `"5919"`：`石墨黑`
      - 第二个列表（规格） 
        - `"5926"`: `英特尔酷睿 i5/8GB/128GB`
        - `"5927"`: `英特尔酷睿 i5/8GB/256GB`
        - `"5928"`: `英特尔酷睿 i5/16GB/256GB`
        - `"5929"`: `英特尔酷睿 i5/8GB/512GB`
        - `"5930"`: `英特尔酷睿 i7/16GB/256GB`
        - `"5931"`: `英特尔酷睿 i7/16GB/512GB`
        - `"5932"`: `英特尔酷睿 i7/16GB/1TB`
        - `"5933"`: `英特尔酷睿 i7/32GB/1TB`
    - `senderMail`字段
      - `"addr"`： 用于发送邮件通知的`邮箱地址`
      - `"passwd"`：用于发送邮件通知的`邮箱密码`或`授权码`
      - `"host"`：用于发送邮件通知的`邮箱SMTP服务器地址`
      - `"port"`：用于发送邮件通知的`邮箱SMTP服务器端口`
    - `rcvMails`字段（至少包含一个有效邮箱）
      - `"example01@qq.com"`
      - `"example02@outlook.com"`
      - `···`


 - 添加Actions
    - 参考配置如下
```
name: GITHUB ACITON ReadyForSurface

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]
  schedule:
    - cron: 1 * * * *

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: 'Set up Python'
        uses: actions/setup-python@v1
        with:
          python-version: 3.9
      - name: 'Install requests'
        run: pip install requests beautifulSoup4 yagmail
      - name: 'Working'
        env:
          conf: ${{ secrets.CONF }}
        run: python ./main.py
```
- 等待补货通知（邮件）


