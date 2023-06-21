# -*- coding: utf-8 -*-
"""
@Author：wang jian wei
@date：2023/6/21 16:10
"""
import uvicorn

if __name__ == '__main__':
    uvicorn.run(app="app:app", host="127.0.0.1", port=8000, reload=True)
