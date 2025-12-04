# 智能AI审查系统

## 项目目标:实现能够完成合同审查、文案审查以及通用对话的智能AI审查系统

#### **tip:** 起步阶段，因为这是Huanchao Feng根据工作时一个项目思路构思的系统，没有太多用户反馈和产品规划

#### Author: Huanchao Feng

## 项目入口：./ai_web

## 项目技术：
FastAPI + LangGraph + Langchain + Mysql
* FastAPI实现系统服务化
* LangGraph构建工作流编排（类似Dify低代码工具流平台）
* LangChain实现模型调用以及工具类编写
* Mysql实现用户、会话持久化，用于查询、渲染功能

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
流程：输入文本——>小模型意图识别——>合同审查/文案审查/通用对话——>对应处理
* 合同审查——>对应Prompt + 对应知识库 + 处理思路
* 文案审查——>对应Prompt + 对应知识库 + 处理思路
* 普通对话——>对应Prompt + 模型输出结果
对话记忆：提取数据库最后n轮的对话记录(pair对：human + ai), 在每次提问前，将数据查询出并嵌入state中，与用户新问题（位于最后一条消息）一起拼接

## 3、搭建数据库存储聊天记录，实现对话持久化功能
流程：采用Mysql实现数据库功能，对于聊天记录的存储，只存放AIMessage以及HumanMessage，截取每一轮对话的User和Ai（最终结果），保存至数据库，数据库存储包括：创建时间（根据时间来展示历史记录）、Type(AI/Human)、SessionId（会话窗口）、Titile（会话窗口的名称,可采用AI总结第一次对话内容或者直接截取第一次对话的前n个字符）、所属用户（账户），目前仅支持对话式，后期拓展文件上传功能

Mysql数据库实现聊天记录存储：
2张表：chat_message、session表
* chat_message表存储全部会话的历史记录
* session表存储会话的title

## 4、系统服务化处理
这个阶段需要把函数接口打造成http请求接口，并实现用户权限管理，登录管理，注册管理，新增用户表与权限表，并且进行限流操作
* 对话接口开发
* 登录接口开发
* 注册接口开发
* 用户权限开发
* 限流操作（可使用令牌桶或者ip限流的方式进行，同时对于恶意刷接口操作进行黑名单管理）