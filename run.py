# run.py

from app import create_app

# 创建 Flask 应用实例
app = create_app()

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)
