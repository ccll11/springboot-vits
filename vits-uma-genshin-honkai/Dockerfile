# 使用Python作为基础镜像
FROM python:3.8

# 设置工作目录
WORKDIR /code

# 复制应用代码到容器中
COPY . .

# 安装依赖项
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 暴露应用端口
EXPOSE 5000

# 设置启动命令
CMD ["python", "app.py"]