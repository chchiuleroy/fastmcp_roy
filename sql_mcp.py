# -*- coding: utf-8 -*-
"""
Created on Tue Oct  7 15:20:45 2025

@author: roy
"""

import pymysql
import pandas as pd
from fastmcp import FastMCP

mcp = FastMCP("mcp_sql")

connection = None

@mcp.tool()
def connect_db(database:str)-> dict:
    """
    取得資料庫連結的資訊
    
    Args:
        database: 資料庫名稱，是字串 
        
    Returns:
        dict: 資料庫 回應的 JSON 資料
    """
    global connection
    try:
        connection = pymysql.connect(
                    host='', # input your own host and password or set env by yourself
                    port=3306,
                    user='root',
                    password='',
                    database=database,
                    charset='utf8mb4'
                )
        return {"status": "success", "message": "資料庫連線成功"}
    except Exception as e:
        return {"status": "error", "message": f"連線失敗: {str(e)}"}

@mcp.tool()
def show_tables()-> dict:
    """
    顯示所選資料庫內所有資料表名稱
    
    Args:
        
    Returns:
        dict: 回傳資料庫內所有資料表名稱
    """
    if not connection:
        return {"status": "error", "message": "請先建立資料庫連線"}
    try:
        query = 'SHOW TABLES'
        df = pd.read_sql(query, connection)
        return {
            "status": "success",
            "tables": df.to_dict(orient='records')
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
def show_columns(table:str)-> dict:
    """
    顯示選定資料表的所有欄位名
    
    Args: 
        table: 資料表名稱 是字串
    
    Returns:
        dict: 回傳資料庫內選定資料表的欄位名稱
    """
    if not connection:
        return {"status": "error", "message": "請先建立資料庫連線"}
    try:
        query = f'SHOW COLUMNS FROM {table}'
        df = pd.read_sql(query, connection)
        return {
            "status": "success",
            "columns": df.to_dict(orient='records')
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
def execute_query(query:str)-> dict:
    """
    執行 SQL 查詢
    
    Args:
        query: sql 查詢代碼 是字串
    
    Returns:
        dict: 回傳sql查詢代碼的數據
    """
    if not connection:
        return {"status": "error", "message": "請先建立資料庫連線"}
    try:
        df = pd.read_sql(query, connection)
        return {
            "status": "success",
            "data": df.to_dict(orient='records'),
            "row_count": len(df)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    mcp.run(host = '0.0.0.0',port=8888,transport='sse') # seting your host and port, then deploy this program in your server or cloud
