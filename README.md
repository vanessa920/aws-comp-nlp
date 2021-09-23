# Meeting Stickers Demo

**1st Place Winner** Project of AWS(China) Online Hackathon 2021: https://new.qq.com/omn/20210830/20210830A05BSB00.html


## Project Name

AI Meeting Stickers: [DEMO](https://meeting-stickers.000webhostapp.com/) | [Presentation](https://github.com/vanessa920/amazonaws-hackathon-2021/blob/main/%E5%96%84%E7%94%A8AI%EF%BC%8C%E5%88%9B%E9%80%A0%E7%BE%8E%E5%A5%BD%E7%94%9F%E6%B4%BB%E3%80%82/AI%20Meeting%20Stickers%20-%20AI%E4%BC%9A%E8%AE%AE%E4%BE%BF%E7%AD%BE%E6%9D%A1%20-%20%E7%82%92%E6%A0%97%E5%AD%90%E5%B0%8F%E9%98%9F/img/AI%20Meeting%20Stickers.pdf)

## Project Team

+ Vanessa Hu - https://www.linkedin.com/in/vanessahu/
+ Sheng Xiong Ding (Roland) - https://www.linkedin.com/in/roland-ding-403a5b1a/

## Background

In work and life, the distribution and sorting of meeting minutes is a thankless task. For those who want to know the content of the meeting, it is difficult to quickly obtain the direct content of their interest by reading the long list of meeting minutes. We use the government's public meeting records as a training data set, and we also hope to help the government improve the transparency and accessibility of government affairs, and promote public taxpayers to participate in government affairs supervision and municipal construction. Usually, the content of the government's municipal meeting is published online in PDF format, and it is difficult for people to search and consult according to the specific content. We perform structural segmentation and text preprocessing of the conference content, convert the text data into real-valued vectors that can be directly used by machine learning algorithms, and use natural language processing algorithms for topic modeling (Topic Modeling), adding word embedding (Word2Vec) technology Perform classification feature processing, so that the public can search and subscribe to the topics of interest in the municipal meeting across the timeline, like flipping through the notes, without having to read the complete meeting record to obtain the interesting segmented content. The future vision of the work is to promote the work within the enterprise, to efficiently classify, retrieve and subscribe to the specific content of each department meeting, so as to save the participation time of some participants, and establish an automated AI system to improve the efficiency of meetings and communication.

## Goal

The goal is parse a large dataset of public meetings (i.e. City Council, School Board, Planning Commission) and surface critical insights to everyday community members. This may involve imagine recognition, natural language processing, and sentiment analysis. Meeting minutes are often stored as PDFs so we need help running image recognition on the PDFs. 

An example use case: we want to analyze the structure of each meeting and serialize the meeting structure so we can pass it to other software applications. 
Another example use case: we want to analyze the meeting contents so we can tag meetings. A user may want to subscribe to meetings that talk about housing so we need to tag meetings that talk about housing in the agenda."

The goal is to build out the NLP capabilities in processing text documents to accurately and succinctly capture relevant information on key words.

[Code for San Jose Project List](https://docs.google.com/spreadsheets/d/15nBWVyG4nFTOFKP4u1tOgFxH9xwAF8uaZG47ABm7HQ4/edit#gid=545916388)

## Data

San Jose City Council Meeting Minutes Source: [Legistar](https://sanjose.legistar.com/Calendar.aspx)

## Features

1. Subject keyword query function
2. Cross-timeline query and retrieval
3. A quick tour of conference topics
4. User personalized settings
5. Budget related query retrieval


