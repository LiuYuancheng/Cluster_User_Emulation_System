# **User Action Emulator**

[TOC]

### Introduction

User Actor Emulator is a RPA type scheduler to invoke the lib from action repository to build more complex “Human type” activities and run the tasks based on the users’ timeline playbook configuration. The emulator program provides four levels of components to build/implement the customers requirement: 

- **Basic action function[lvl-0] :** Do one basic action such as file send tcp request, file copy, run cmd. 
- **User action [lvl-1]:** Grouped basic functions with a schedule config file to implement complex user’s action such read and write email, join a zoom meeting. 
- **Actor [lvl-2]:** Grouped user actions with a schedule config file to implement human normal activity such as edit a PPT and share to the cloud, play a sample game, surf the internet and download the contents. 
- **User emulator [lvl-3]:** Schedule the actors with a customized timeline so the emulator can implement a specific user’s daily event, such as a network admin.

The components relationship is shown below:

![](doc/img/RM_Diagram_components.png)





------

> Last edit by LiuYuancheng(liu_yuan_cheng@hotmail.com) at 03/02/2023, if you have any problem or find anu bug, please send me a message .