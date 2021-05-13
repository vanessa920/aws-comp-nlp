# aws-comp-nlp

AWS Hackathon Online 2021
Organizer: 机器之心

## Project Name

AI Meeting Notes

## Background

在工作和生活中，会议记录的分发和整理是一件费力不讨好的事情，对于想要了解具体开会内容的人，阅读连篇累牍的会议记录很难快速获取自身感兴趣的摘要内容。我们利用政府公开的会议记录作为训练数据集，也寄希望于能帮助政府提高政务公开的透明度和可查询性，推动公众纳税人参与政务监督与市政建设。 通常政府的市政会议内容会以PDF的格式进行线上公开，人们很难根据具体内容进行检索和查阅。我们对会议内容进行结构细分和文本预处理，把文本数据转换成便于机器学习算法直接使用的实值向量，并用自然语言处理的算法进行主题模型(Topic Modeling)，加入词嵌入（Word2Vec）技术进行分类特征处理，从而让公众可以对市政会议里感兴趣的主题进行跨时间线的检索与订阅，像翻阅便签条一样，无须阅读完整的会议记录而获取感兴趣的细分内容。作品未来的愿景是推广到企业内部，对于各部门会议的具体内容进行片断式的高效分类、检索和订阅，从而节省部分与会者的参与时间，建立自动化的AI系统来提高开会和沟通的效率。

## Goal

The goal is parse a large dataset of public meetings (i.e. City Council, School Board, Planning Commission) and surface critical insights to everyday community members. This may involve imagine recognition, natural language processing, and sentiment analysis. Meeting minutes are often stored as PDFs so we need help running image recognition on the PDFs. 

An example use case: we want to analyze the structure of each meeting and serialize the meeting structure so we can pass it to other software applications. 
Another example use case: we want to analyze the meeting contents so we can tag meetings. A user may want to subscribe to meetings that talk about housing so we need to tag meetings that talk about housing in the agenda."

The goal is to build out the NLP capabilities in processing text documents to accurately and succinctly capture relevant information on key words.

[Code for San Jose Project List](https://docs.google.com/spreadsheets/d/15nBWVyG4nFTOFKP4u1tOgFxH9xwAF8uaZG47ABm7HQ4/edit#gid=545916388)

## Data

San Jose City Council Meeting Minutes 加州圣荷塞市政厅会议记录 [Legistar](https://sanjose.legistar.com/Calendar.aspx)

## Features

1. 主题关键词查询功能
2. 跨时间线查询检索
3. 会议主题快速浏览
4. 用户个性化设置
5. 预算相关查询检索


