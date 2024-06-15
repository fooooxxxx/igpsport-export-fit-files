# igpsport-export-fit-files

> 本脚本仅适用于可通过 https://my.igpsport.com/ 登录的中国大陆账号,不适用于 https://i.igpsport.com/

## 功能简介

按时间范围批量导出 igpsport 的 fit 文件到本地。

## 使用流程

https://github.com/fooooxxxx/igpsport-export-fit-files/releases/latest

### 下载并启动脚本

如有 Python 环境可以直接下载 igpsport-export-fit-files.py，并使用 python igpsport-export-fit-files.py 启动脚本。

如没有 Python 环境，请下载 igpsport-export-fit-files.zip，解压后打开 igpsport-export-fit-files.exe进行操作
 
### 启动后操作流程

1. 按照提示选择鉴权 `用户名/密码`（推荐） 或 `Cookie` 登录方式。
2. 选择需要下载的时间范围，格式为 2023-01-01~2024-01-01，留空表示全部下载
3. 等待直到提示本次下载文件数量
4. 在脚本所在目录的 downloads 文件夹下即可找到下载的全部文件

> Cookie 打开浏览器的开发者窗口，复制带有 `loginTicket=` 作为 Cookie

## 用例

### 旧数据导入到 training peaks

`igpsport` 可以关联 training peaks 账号，关联后新纪录会自动同步到training peaks。但 igpsport 不会同步关联前上传的旧数据。

使用本脚本可以下载过往的fit数据，使用拖拽的方式将旧数据导入到 training peaks。

[training peaks 运动数据上传页](https://app.trainingpeaks.com/#calendar)

https://help.trainingpeaks.com/hc/en-us/articles/204072034-Drag-and-Drop-to-Upload-a-Device-File
