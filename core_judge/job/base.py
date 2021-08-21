

import logging
class CallbackJob:
    SUCCESS=-3
    INCOME=-2
    FAILED=-1

    STORAGE=0
    COMPILER=1
    EXECUTION=2
    EXECUTION_CHECKER=3
    EVALUATION_CHECKER=4
    
    COMPILATION_ERROR="CE"
    TIME_LIMIT_EXCEEDED="TLE"
    WRONG_ANSWER="WA"
    ACCEPTED="AC"
    FILE_STORAGE_FAILED="FILE STORAGE FAILED MAYBE NOT YOUR FAILED PLS CONTACT ADMIN"
    COMPILATION_DONE="COMPILATION_DONE"
    SIGNAL_RECEVIED='Runtime Error'
    
    STORAGE_CALLBACK={
        FAILED:"FAILED PROCESS FILE STORAGE. MAY BE CHECK SANDBOX FILE OR IF YOU USED PATH PLS CHECK FILE HAS ALREADY EXITS",
        INCOME:"IN PROCESS STORAGE JOB. BE PATIENT!!",
        SUCCESS:"PREPARE FILE SUCCESS TOTALLY"
    }
    COMPILER_CALLBACK={
        FAILED:"COMPILER EROOR",
        INCOME:"IN PROCESS COMPILER",
        SUCCESS:"COMPILER SUCCES"
        
    }
    EXECUTION_CALLBACK={
        FAILED:"COMPILER EROOR",
        INCOME:"IN PROCESS COMPILER",
        SUCCESS:"COMPILER SUCCESS"
    }
    REVERSER_DICT={
        SUCCESS:"SUCCESS",
        FAILED:"FAILED",
        INCOME:"INCOME",
        EXECUTION:"EXECUTION",
        COMPILER:"COMPILER",
        STORAGE:"STORAGE",
        EXECUTION_CHECKER:"EXECUTION_CHECKER",
        EVALUATION_CHECKER:"EVALUATION_CHECKER"
    }
    def __init__(self) -> None:
        pass
    def to_str(self, value:int, status:str)->str:
        if value == CallbackJob.STORAGE:
            return self.callback_storage(value, status)
        if value == CallbackJob.COMPILER:
            return self.callback_compiler(value, status)
    def callback_storage(self, value:int, status:str)->str:
        return self.STORAGE_CALLBACK[status]
    def callback_compiler(self, value:int, status:str)->str:
        pass
    

class JobBase(object):
    
    def __init__(self,**kwargs):
        for item in kwargs.keys():
            self.item = kwargs[item]
    

    def run(self):
        raise Exception('IMPLEMENT')

    def prepare_file(self):
        raise Exception("implement")

    def update_status(self,log:dict)->None:
        logging.info(
            str(log)
        )
        if self.celery_task_object is not None:
            if 'meta'  in log:
                self.celery_task_object.update_state(state="PROGRESS", 
                                            meta={'meta':log['meta']})
    def eval_status(self):
        self.sandbox.cleanup()

    def collected_info(self, info):
        time = 0
        mem = 0
        wal=0
        for i in info:
            time = max(time, i['execution_time'])
            mem = max(mem,i['execution_memory'] / 256 ) #MB
            wal  = max(wal, i['execution_wall_clock_time']/256)

        return {'execution_time':time,'execution_memory':mem,'execution_wall_clock_time':wal}