import logging
import threading
import time
import os
import configparser
import requests
import subprocess
import sys
import xml.etree.ElementTree as ET

class JobInfo:
    pid : str
    status : str
    def setmeta(self,action,taskId,taskType,sourceFile,sourceId,sourcePw,targetPath,targetId,
    targetPw,param):
        self.Action = action
        self.TaskId = taskId
        self.TaskType = taskType
        self.SourceFile = sourceFile
        self.SourceId = sourceId
        self.SourcePw = sourcePw        
        self.TargetPath = targetPath
        self.TargetId = targetId
        self.TargetPw = targetPw
        self.Param = param        


def StrToBool(s):
    return s =='1'

def GetTask():
    while  True:        
        time.sleep(getJobInterval)
        jobInfo = JobInfo()

        if WebPost(jobInfo):
            AddTaskDataList(jobInfo) 
            ExecuteModule(jobInfo)
    
def AddTaskDataList(jobinfo):        

    for data in taskDataList:
        if (data.TaskId == jobinfo.TaskId):
            taskDataList.remove(data)
    
    taskDataList.append(jobinfo)     
  

def WebPost(jobInfo):

    #buf = '<Request><GetTask Action=\"assign\" Type=\"20\"/></Request>'
    #response = requests.post(getJobPage,buf)    

    #logger.info(response.text)    
    #Test
     data = open(testXmlPath,'r')
     data = data.read() 
    # #  Suc
     if 'Result' in data :
        tree = ET.ElementTree(ET.fromstring(data))
        root = tree.getroot()
        result = root.find('Result')

        resultAction = result.attrib.get('Action')
        taskId = result.find('TaskID').text
        taskType = result.find('TaskType').text

        sourceRoot =  result.find('SourceFile')                
        sourceId = sourceRoot.attrib.get('id')        
        sourcePw = sourceRoot.attrib.get('pw')               
        sourceFile = sourceRoot.text

        targetRoot = result.find('TargetPath')
        targetId = targetRoot.attrib.get('id')        
        targetPw = targetRoot.attrib.get('pw')               
        targetPath = targetRoot.text

        infoRoot = result.find('Info')        
        param = infoRoot.find('Parameter').text        
        #etc = result.find('Etc').text        


        jobInfo.setmeta(resultAction,taskId,taskType,sourceFile,sourceId,sourcePw,targetPath,targetId,targetPw,param)
        return True
     else:
         return False


def ExecuteModule(jobInfo):    
    jobInfo.status = 'START'
    jobInfo.pid = '1'
    modulePath = GetModulePath(jobInfo.TaskType)
    subprocess.Popen([modulePath,'123'])

def GetModulePath(jobType):
    if jobType == '10':
        return testModulePath

def LoadConfig():
    global webServer,getJobPage,getJobInterval,updatePage,cencelPage,webPort,catalogJob
    global transcoderJob,transferFTPJob

    config = configparser.ConfigParser()
    config.read(testIniPath)

    getJobInterval = int(config['Rules']['GetJobInterval'])    
    getJobPage = config['HTTP']['GetJobPage']
    updatePage  = config['HTTP']['UpdatePage']
    cencelPage  = config['HTTP']['CancelPage']
    webServer = config['HTTP']['WebServer']
    webPort = config['HTTP']['WebPort']

    catalogJob = StrToBool(config['HTTP']['CatalogJob'])
    transcoderJob = StrToBool(config['HTTP']['TranscoderJob'])
    transferFTPJob = StrToBool(config['HTTP']['TransferFTPJob'])
  

def InitLog(main):
      global logger

      logger = logging.getLogger(main)
      formatter = logging.Formatter('[%(asctime)s - %(levelname)s] | %(message)s' )
      streamHandler = logging.StreamHandler()
      fileHandler = logging.FileHandler(logPath)

      streamHandler.setFormatter(formatter)
      fileHandler.setFormatter(formatter)
      logger.addHandler(streamHandler)
      logger.addHandler(fileHandler)
      logger.setLevel(logging.INFO)


absPath = os.path.dirname(os.path.abspath(__file__))
logPath = absPath + '/test.log'
testTxtPath = absPath + '/test.txt'  
testIniPath = absPath + '/test.ini'
testXmlPath = absPath + '/test.xml'
testModulePath = absPath + '/Module/Testmodule'
taskDataList = []


if __name__ == '__main__':    

    InitLog(__name__)    
    LoadConfig()    

t = threading.Thread(target=GetTask)
t.start()

while True:
    pass