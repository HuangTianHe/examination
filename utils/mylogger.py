# -*- coding: utf-8 -*- 
'''
该日志类可以把不同级别的日志输出到不同的日志文件中
''' 
import os
import sys
import time
import logging
import logging.handlers
import inspect
from os import makedirs
import multiprocessing
import threading


_loggingdict={}

class TNLog(object):
    def printfNow(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    
    def __init__(self,level='noset',logname='default',handlers=None,name=None,log_dir=None):
        self.__loggers = {}
        if not name:
            self.name=logname
        else:
            self.name=name
        self.handlers={}
        self._setlogfile(logname=logname,handlers=self.handlers,log_dir=log_dir)
        self.createHandlers()
        logLevels = self.handlers.keys()
        current_process_name = multiprocessing.current_process().name
        current_thread_name = threading.current_thread().name
        for level in logLevels:
            logger = logging.getLogger("%s-%s-%s-%s"%(current_process_name,current_thread_name,self.name,level))
            #如果不指定level，获得的handler似乎是同一个handler? 
            #fmt='[%(asctime)s](%(levelname)s, %(message_info)s): %(message)s'
            #format2=logging.Formatter(fmt)
            format2 = logging.Formatter()
            self.handlers[level].setFormatter(format2)          
            logger.addHandler(self.handlers[level])
            #print level
            lev='lev=logging.'+level.upper()
            exec(lev)
            #print lev
            logger.setLevel(int(lev))
            
            self.__loggers.update({level:logger})
        #print self.__loggers

    def getLogMessage(self,level,message):
        frame,filename,lineNo,functionName,code,unknowField = inspect.stack()[2]
        current_process_name=multiprocessing.current_process().name
        current_thread_name=threading.current_thread().name
        '''日志格式：[时间] [类型] [当前进程名] [当前线程名] 信息'''
        return "[%s] (%s,%s,%s,%s) %s" %(self.printfNow(),level,current_process_name,current_thread_name,functionName,message)
    
    def info(self,message):
        message = self.getLogMessage("info",message)
        self.__loggers["info"].info(message)
    
    def error(self,message):
        message = self.getLogMessage("error",message)
        self.__loggers["error"].error(message)
    
    def warning(self,message):
        message = self.getLogMessage("warning",message)
        self.__loggers['warning'].warning(message)

    
    def debug(self,message):
        message = self.getLogMessage("debug",message)
        self.__loggers['debug'].debug(message)

    
    def critical(self,message):
        message = self.getLogMessage("critical",message)
        self.__loggers['critical'].critical(message)


    def createHandlers(self):
        logLevels = self.handlers.keys()
        for level in logLevels:
            path = os.path.abspath(self.handlers[level])
            #self.handlers[level]= logging.handlers.RotatingFileHandler(path)
            self.handlers[level] = logging.handlers.TimedRotatingFileHandler(path,when='d')

    def _setlogfile(self,handlers=None,logname=None,log_dir=None):
        try:
            if not os.path.exists('%s/%s'%(log_dir,logname)):
                makedirs('%s/%s'%(log_dir,logname))
        except:
            pass
        default_handlers = {
                'notset':"%s/%s/%s_notset.log"%(log_dir,logname,logname),
                'debug':"%s/%s/%s_debug.log"%(log_dir,logname,logname),
                'info':"%s/%s/%s_info.log"%(log_dir,logname,logname),
                'warning':"%s/%s/%s_warning.log"%(log_dir,logname,logname),
                "error":"%s/%s/%s_error.log"%(log_dir,logname,logname),
                'critical':"%s/%s/%s_critical.log"%(log_dir,logname,logname)
                }
        if handlers:
            default_handlers.update(handlers)
        self.handlers.update(default_handlers)

def setlogfile(logname='default',handlers=None,log_dir=None):
    if not logname in _loggingdict.keys():
        logger = TNLog(logname=logname,handlers=handlers,log_dir=log_dir)
        _loggingdict[logname]=logger
    
def get_log(logname='default',log_dir='.'):
    if not logname in _loggingdict.keys():
        setlogfile(logname=logname,log_dir=log_dir)
    return _loggingdict[logname]
if __name__ == "__main__":
    get_log('JsonToHtm333').error('mmmmmmmdfsfsfsfsfs')
    get_log("sss").info('ssss')
    get_log("tttt").info('tttt')
    get_log("sss").info('ssss')
    get_log("tttt").info('tttt')
    get_log("mmmm").info('mmmm')
    get_log("mmmm").info('mmmm')
    get_log("sss").info('ssss')

