# 实现能够完成合同审查、文案审查以及通用对话的智能法务系统

## author: Huanchao Feng

## 项目技术：
FastAPI + LangGraph + Langchain + SQLite + PostgreSQL/Mysql
* FastAPI实现系统服务化
* LangGraph构建工作流编排（类似Dify低代码工具流平台）
* LangChain实现模型调用以及工具类编写
* SQLite实现LangGraph状态持久化
* PostgreSQL/Mysql实现用户、会话持久化，用于查询、渲染功能

## 1、完成文档收集、清洗与向量存储

* 加载文档、切分、嵌入、写入Milvus向量数据库
* 检索Milvus、取出检索文本
* Milvus向量数据库存储文档embedding
    ```python
    wget https://github.com/milvus-io/milvus/releases/download/v2.6.6/milvus-standalone-docker-compose.yml -O docker-compose.yml
    docker compose up -d
    docker-compose ps
    ```

## 2、完成workflow搭建


## 3、搭建数据库存储聊天记录，实现多轮对话记忆功能


## 4、系统服务化处理