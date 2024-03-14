# Cluster User Emulation System (CUE)

![](doc/img/logo.png)

**Project Design Purpose**: Our objective is to develop a distributed, automated, flexible and reusable toolkits set for generating both benign and malicious activities and traffic. This toolkit is designed to fulfill the following requirements:

- Simulation of a mid size of cluster/network with active users (generate human activities) for Digital Forensics and Incident Response (DFIR). 
- Simulation of red team attacks or recurrent attack scenarios in cyber exercise/events.
- Simulation of blue team defense activities or the creation of live honeypots. 
- Provide real time monitoring and management interface of cyber exercise management team. 
- Automated to do regular penetration test or stress test for a system or service. 
- Assistance in cyber-security education and professional training. 
- Building the customizable malware for researching purposes. 

By meeting these objectives, our toolkit aims to enhance cybersecurity preparedness, training, and research efforts by providing comprehensive and adaptable functionalities.

```
version:     v0.2.2
Copyright:   Copyright (c) 2024 LiuYuancheng
License:     MIT License   
```

**Table of Contents**

[TOC]

------

### Introduction

The Cluster User Emulation System operates within a network/compute cluster environment, simulating multiple users' actions and monitoring their network traffic and activities. This system serves various purposes, including:

- Providing a library repository with benign and malicious activities&traffic plugin module for customers to create customized complex "Human / Hacker / device" type actions.
- Providing automatically robotic processes and tasks (RPT) or repeating/replaying specified attacking path/scenario of red team and defense activities of blue team during cyber exercise/event.
- Generating network traffic flows with different protocols for target system penetration testing, service stress testing or using for network security research projects.
- Providing the management interface for monitoring and controlling the tasks, processes, network traffic, node activities, and group-users interactive actions.
- Establishing repeatable test environments for testing and verifying AI/ML trained models.

With its versatile capabilities, the Cluster User Emulation system proves invaluable for cybersecurity exercises, research projects, AI/ML testing, and process automation.

#### System Structure 

The Custer User Emulator System contents three main parts, the `Activities Generation Modules Repository`, the `Users Action Emulator` and the `System Status Orchestrator` as shown blow:

![](doc/img/systemStructure.png)

The Activities Generation Modules Repository is a collection of library modules for generating both benign and malicious activities and traffic. The Organic repository comprises 33 different plugin modules and the Malicious repository contains 24 different plugin modules. 

The User Action Emulator serves as the activating agent, utilizing assembled plugin modules from the `Activities Generation Modules Repository` to execute tasks on the target machine according to a user-defined timeline.

The System Orchestrator is a cloud-based server that aggregates all User Action Emulator task execution states and offers a management website interface for users to monitor and manage the User Action Emulators



------

### Project Design 

This section will introduce the design of system workflow, the design of system execution in the cyber range and the design of the three project main section. 



#### Design of System Work Flow 

The system workflow consists of five main steps, outlined below:

![](doc/img/systemWorkflow.png)

1. **Behavior Module Assembly**: This step involves gathering library modules from the `Activities Generation Modules Repository` based on the user's configuration file.

2. **Activities Profile Building**: The gathered library modules and playbook files are packaged into a specific format profile, tailored for use by the emulator.

3. **Customized User Emulator**: The profile package is imported to the emulator to create a customized "Role" program, ensuring it behaves according to user specifications.

4. **Activities and Traffic Generation**: Upon execution, the emulator follows the playbook within the profile to generate relevant activities and traffic flow as per the user's requirements.

5. **Procedure Monitoring**: This step involves monitoring the progress of task execution to ensure tasks are carried out efficiently and effectively.

   

##### Benign Activities and Traffic Generation 

The detailed 5 steps workflow of the system generating the benign traffic is shown below:

![](doc/img/workflow.png)

With different playbook and profile config the emulator can act as different type of users and device in a cyber range such as 

IT/OT Specialist: Maintenance engineer, Network admin, Pentest engineer and Support engineer

Company Officer's Daily Work : HR officer Finance Manager, HQ Operator and Company Intern







##### Activities Generation Modules Repository

This repository houses a collection of library modules for generating both benign and malicious activities and traffic. These modules can be seamlessly integrated with other components to generate organic activities across hardware, network, operating system, and application levels. Examples of such activities include initiating online meetings, sending/receiving emails, uploading/downloading files, editing MS-Office documents, toggling Windows Firewall, and watching online/offline videos.

The **Organic** repository comprises 33 different plugin modules categorized into four types:

- Network Activities Generation plugin [11 modules]
- Application/Software Interaction and Control Activities plugin [9 modules]
- Human Operation Activities plugin [8 modules]
- System Activities plugin [5 modules]

Conversely, the **Malicious** repository contains 24 different plugin modules across five types:

- Credentials and Critical Data Compromise plugin [4 modules]
- Phishing and Scam plugin [4 modules]
- Scan and Record plugin [5 modules]
- Denial of Service plugin [5 modules]
- System Destruction plugin [6 modules]

These modules offer a comprehensive range of functionalities to support various simulation and testing requirements, enhancing the versatility and effectiveness of the activities generation process.



##### User Action Emulator 

The User Action Emulator serves as the activating agent, utilizing assembled plugin modules from the `Activities Generation Modules Repository` to execute tasks on the target machine according to a user-defined timeline. It consists of two main components module:

- **Activities Scheduler Module**: The Activities Scheduler interprets the user's task timeline configuration and selects plugin modules from the `Activities Generation Modules Repository` based on task type specifications. Subsequently, it constructs a "playbook" to organize the execution sequence of each task according to the scheduled timeline. Once all modules and the playbook are imported, the Activities Scheduler packages them into a single package ( emulator profile ) for execution by the Action Emulator module.

- **Action Emulator Module**: Each Action Emulator instance loads a user profile (generated by the scheduler module) and assumes the role required for simulation. It executes tasks based on the timeline configuration, saving the execution results in emulator local database and updating them to the Orchestrator server for user access. Depending on the timeline configuration, the Action Emulator can generate regular or random human, software, or malware activities and traffic on a daily, weekly, or monthly schedule.



##### System Orchestrator

The System Orchestrator is a cloud-based server that aggregates all User Action Emulator task execution states and offers a management website interface for users to monitor and manage the User Action Emulators. The Orchestrator provides two distinct web interfaces:

- **Emulator Procedure Management Interface**: This web dashboard displays comprehensive information about all connected emulators, including their current state and task details. Users can efficiently oversee the execution of tasks across multiple emulators from this interface.
- **Malware Command and Control Interface**: This web dashboard presents the task execution states of all connected malware instances and offers a web API for the red team to dynamically control the malware. This interface empowers red team members with the flexibility to manage malware operations effectively in real-time.

 

------

 















#### System structure 

The user Emulator system can be deployed on single compute node, real network system, VMs based SDN (software defined network). The product contents three parts, the “User actions repository”, the “User action emulator/scheduler” and the “scheduler monitor hub”. (The 3 parts relationship is shown in the below system deployment structure diagram)

![](doc/img/RM_diagram_system.png)

- 

The modules relationship diagram is shown below: 

![](doc/img/RM_diagram_module.png)

`Version: 0.1`

------

### Product overview 

There are several kinds of well-developed network traffic generators, task scheduler tools and the tasks progress monitors hub in the market. But most of these tools’ functions are very general and don’t cover all the three areas ( emulation, management and monitoring), so the customer still speed a lot of time and effort to build their system. Our Cluster Users Emulator is aimed to provide a packaged all-in-one light solution allow our customers to simulate a groups of different users’ complex human type action, then schedule these events and monitor / control them without spending much workload to play with several different tools. 

#### SWOT Business Analysis

![](doc/img/RM_diagram_swot.png)

##### Who may be interested about using it: 

- Customers whose system config setting and requirements keep updating, or need flexible tool to integrate different apps. 
- Customer who wants to create some complex “human type” action especially related UI operation and Windows platform.
- Customer who needs different kinds of pre-configured activities scenario and try to avoid spending much development effort on the events/traffic generation details. 
- Researcher who want to automatically repeat specific scenario with small changes for their experiments.

##### Why user choose using it : 

- **Open** : Our product is open source and focuses on more specific activities generation tasks, so compare with other general tools, our product is more suitable for the customer to create complex scenario. 
- **Reusable**: Our product can provide activities library for customer to reuse and integrate to their software/program. 
- **Flexible**: Our pre-build user cluster’s activities scenario can be easily changed to match customers’ requirement to help reduce the customer’s development effort. 

##### **User Action emulator demo video:** 

- https://www.youtube.com/watch?v=jgm3gQhzUq4&t=57s
- https://www.youtube.com/watch?v=wZsRmYPcPTQ



------

### System Design

We want to create an intelligent "actor” program which can simulate a normal MS-Windows user’s daily action ( different kinds of network access, system level operation and different app level operation) to generate user’s regular or random event based on the customer’s requirement. So, it can:

- Be used to repeat/replay specified large numbers of users (blue team) activities in cyber exercise event.
- Generate required network traffic flow for network security research project. 
- Be used as repeatable user’s test environment for AI/ML trained module’s verification.

##### System Work Flow Diagram

The system will work under the below work diagram 

![](doc/img/RM_Diagram_workflow.png)



#### User Actions Repository

User Actions Repository is library APIs repository to simulate simple user’s normal activities/events under hardware, network, OS and App level. (Such as starting the online meeting, send/receive email, upload/download files, edit MS-Office doc, On/Off Windows FW, watch online/offline video…)

Currently we provide 5 main repositories with 18 kinds of basic user action functions and 28 kinds of pre-built complex user’s actors components. The 5 main feature repositories covers: 

- Network traffic action generators. 
- Application operation action generators. 
- User’s human activities action generators.
- System control action generators.
- Other action generators.

**The detail document link of User Action Repository** [click [here](ReadMe_User_Actions_Repository.md) ] 



#### **User Action Emulator**

User Actor Emulator is a RPA type scheduler to invoke the lib from action repository to build more complex “Human type” activities and run the tasks based on the users’ timeline playbook configuration. The emulator program provides four levels of components to build/implement the customers requirement: 

- **Basic action function[lvl-0] :** Do one basic action such as file send tcp request, file copy, run cmd. 
- **User action [lvl-1]:** Grouped basic functions with a schedule config file to implement complex user’s action such read and write email, join a zoom meeting. 
- **Actor [lvl-2]:** Grouped user actions with a schedule config file to implement human normal activity such as edit a PPT and share to the cloud, play a sample game, surf the internet and download the contents. 
- **User emulator [lvl-3]:** Schedule the actors with a customized timeline so the emulator can implement a specific user’s daily event, such as a network admin.

The components relationship is shown below:

![](doc/img/RM_Diagram_components.png)

**The detail document link of  User Action Emulator** [click [here](ReadMe_User_Actions_Emulator.md) ] 



#### **Scheduler Monitor Hub**

The Scheduler Monitor hub is a no-centralized monitor website host which provides plug and play tasks state view function for the customer to monitor and control all/parts of their schedulers in a computers/servers cluster. The emulator's task monitor Page/ tasks view is shown below:

![](doc/img/RM_diagram_Monitor_page1.png)

The scheduler monitor hub program provide a website for the customer to check each user emulator’s tasks execution state and do some basic control**.** As shown in the workflow diagram section, the user can connect to the monitor hub server to view the webpage or plug their own laptop in the cluster to “Fetch” the emulators’ state basic their local setting.

**The detail document link of  Scheduler Monitor Hub** [click [here](ReadMe_User_Actions_Emulator.md) ] 





------

### Program Setup [under editing]

###### Development Environment : python 3.7.4

Additional Lib/Software Need: 

###### Hardware Needed : None

###### Program  Folder Structure;



######  

------

### Program Usage



#### Program Execution 

##### User action Emulator

Your can use program execution 1 or program execution 2

- Program execution 1: Run `src/runScheduler_win.bat`
- Program execution 2: cd to `src/actionScheduler` run `python ScheduleRun.py`

##### Scheduler Monitor Hub

Your can use program execution 1 or program execution 2

- Program execution 1: Run `src/runMonitor_win.bat`
- Program execution 2: cd to `src/monitorHub/frontend` run `python app.py`



remove access the windows vm:

```
ssh -L 127.0.0.1:3389:192.168.57.10:3389 -p 6022 -J rp_fyp_ctf@gateway.ncl.sg ls23@172.18.178.10
```





------

### Program Use Case 



------

> Last edit by LiuYuancheng(liu_yuan_cheng@hotmail.com) at 03/02/2023, if you have any problem or find anu bug, please send me a message .