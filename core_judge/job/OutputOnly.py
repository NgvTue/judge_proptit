


import logging
import os
import os,sys,inspect
from select import error
from .base import JobBase
from .base import CallbackJob
try:
    from ..sandbox.sandbox import IsolateSandbox as Sandbox
    from ..languageall import get_language,filename_to_language
    from ..steps.compilation import compilation_step
    from ..config import env
    from ..steps.evaluation import evaluation_step_after_run,evaluation_step_before_run,evaluation_step, human_evaluation_message
except:
    from sandbox.sandbox import IsolateSandbox as Sandbox
    from languageall import get_language,filename_to_language
    from steps.compilation import compilation_step
    from config import env
    from steps.evaluation import evaluation_step_after_run,evaluation_step_before_run,evaluation_step,human_evaluation_message
try:
    from ..sandbox.sandbox import IsolateSandbox ,wait_without_std
except:
    from sandbox.sandbox import IsolateSandbox,wait_without_std
import os



class OutputOnly(JobBase):
    def __init__(self, jobdescription, celery_task_object=None):
        
        self.celery_task_object = celery_task_object
        self.jobdescription = jobdescription
        self.sandbox = IsolateSandbox(box_id=jobdescription.get("id",None))
        self.multiprocess = self.jobdescription.get("multiprocess",None)
        self.time_limit = self.jobdescription.get("time",1.)
        self.memory_limit= self.jobdescription.get("mem",None)
        self.dirs_map = self.jobdescription.get("dirs_map",None)
        if 'checker_lang' not in self.jobdescription.keys():
            self.jobdescription['checker_lang'] = self.jobdescription['checker'].split(".")[-1]
        # contestant_source = self.jobdescription["contestant_source"]
        self.lang_source = self.jobdescription["contestant_lang"]
        self.file_source =os.path.join(self.sandbox.temp_dir,"contestant_source" + "."+self.lang_source)
        self.path_contestant = "contestant_source." + jobdescription['contestant_lang']
        
    def prepare_file(self):

        log = dict(
            name='PREPARE_FILE',
            status = 'INPROGRESS',
            participant_hint = '',
            judge_hint = 'FIRST STEP PREPARE FILE - THIS STEP FAILED IF THE JUDGE HAS A BUG INSIDE',
            step_status = 'UNK'           
        )
        self.update_status(log=log)
        try:
            self.sandbox.create_file_from_string(self.path_contestant,self.jobdescription['contestant_source'],secure=False)
            
            # prepare inputs
            if self.jobdescription['inputs_from_string'] == 'False':
                self.sandbox.create_file_from_storage('inputs',self.jobdescription['inputs'],secure=True)
                self.sandbox.create_file_from_storage('outputs',self.jobdescription['outputs'],secure=True)
                
            else:
                self.sandbox.create_folder("inputs", secure=True)
                self.sandbox.create_folder("outputs", secure=True)
                for index,(input,output) in enumerate(zip(self.jobdescription['inputs'],self.jobdescription['outputs']),1):
                    self.sandbox.create_file_from_string(f"inputs/{index}.in",input, secure=True)
                    self.sandbox.create_file_from_string(f"outputs/{index}.out", output, secure=True)
        except Exception as e:
            
            log = dict(
                    name='PREPARE_FILE',
                    status = 'FAILED',
                    participant_hint = 'this is not your fail, pls contact admin to fix this bug',
                    judge_hint = e,
                    step_status = 'DONE' 
                )
            self.update_status(
                log = log
            )
            return  {'status':'FAILED','meta':log}
        # prepare checkers
        
        try:
            if self.jobdescription['inputs_from_string'] == 'True':
                self.sandbox.create_file_from_storage("testlib.h",env.TESTLIB,secure=True)
                self.sandbox.create_file_from_string('checker.' + self.jobdescription['checker_lang'],self.jobdescription['checker'],secure=True)
            else:
                self.sandbox.create_file_from_storage('checker.' + self.jobdescription['checker_lang'],self.jobdescription['checker'],secure=True)
                self.sandbox.create_file_from_storage("testlib.h",env.TESTLIB,secure=True)
            
            log = dict(
                name='PREPARE_FILE_CHECKER',
                status = 'INPROGRESS',
                participant_hint = '',
                judge_hint = 'FIRST STEP PREPARE FILE - THIS STEP FAILED IF THE JUDGE HAS A BUG INSIDE',
                step_status = 'DONE'           
            )
            self.update_status(
                log = log
            )
            return {'status':'SUCCESS'}
        except Exception as e:
            log = dict(
                name='PREPARE_FILE_CHECKER',
                status = 'FAILED',
                participant_hint = '',
                judge_hint = 'FIRST STEP PREPARE FILE - THIS STEP FAILED IF THE JUDGE HAS A BUG INSIDE',
                step_status = 'FAILED'           
            )
            self.update_status(
                log=log
            )
            return {'status':'FAILED','meta':log}
    def compiler(self):

      
        source_filename = ['contestant_source.' + self.lang_source]
        executable_filename = "contestant_source"
        lang = filename_to_language(self.path_contestant)
        commands =lang.get_compilation_commands(source_filename,executable_filename)
        status = compilation_step(self.sandbox,commands)

        if status[0] is not True or status[1] is not True:
            logging.info(str(status))

            log = dict(
                name='COMPILER',
                status = 'FAILED',
                participant_hint = status[-1]['stderr'],
                judge_hint = '',
                step_status = CallbackJob.COMPILATION_ERROR
            )
            self.update_status(
                log=log
            )
            return {'status':'FAILED','meta':log}
        
        log = dict(
                name='COMPILER',
                status = 'DONE',
                participant_hint = "COMPILATION DONE",
                judge_hint = '',
                step_status = CallbackJob.COMPILATION_DONE
            )
        self.update_status(
                log=log
        )
        source_filename=[os.path.join(self.sandbox.secure_folder,'checker') + "." + self.jobdescription['checker_lang']]
        executable_filename=os.path.join(self.sandbox.secure_folder,'checker')
        lang = filename_to_language("." + self.jobdescription['checker_lang'])
        commands = lang.get_compilation_commands(source_filename,executable_filename)
        status = compilation_step(self.sandbox,commands)
        if status[0] is not True or status[1] is not True:
            status[-1]['status'] = CallbackJob.COMPILATION_ERROR
            status[-1]['value'] ="Checker :" + status[-1]['stderr']
            log = dict(
                name='COMPILER_CHECKER',
                status = 'FAILED',
                participant_hint = 'this is not your failed, pls contact admin fix bug in side compiler checker',
                judge_hint = "Checker :" + status[-1]['stderr'],
                step_status = CallbackJob.COMPILATION_ERROR
            )
            self.update_status(
                log=log
            )
            return {'status':'FAILED','meta':log}
        self.update_status(
                log=dict(
                    name='COMPILER_CHECKER',
                    status="DONE",
                    participant_hint = '',
                    judge_hint = "Checker :" + status[-1]['stderr'],
                    step_status = CallbackJob.COMPILATION_DONE
                )
            )
        return {"status":"DONE"}
    
    def run(self):
        # prepare file
        
        status  =  self.prepare_file()
        if status['status'] == 'FAILED':
            return status['meta']
        # compiler
        status = self.compiler()
        if status['status'] == 'FAILED':
            return status['meta']
        
        
        # run pertest 
        inputs = self.sandbox.get_dir("inputs",secure=True)
        # print(inputs)
        info=[]
        for idx,item in enumerate(inputs,1):
            status= self.run_per_test(idx)
            if status['status'] == 'FAILED':
                return status['meta'] 
            info.append(status['meta']['info'])
        return dict(
            name='VALIDATE_DONE',
            status = 'SUCCESS',
            participant_hint = CallbackJob.ACCEPTED,
            judge_hint = "",
            step_status =CallbackJob.ACCEPTED,
            info = self.collected_info(info)
            
        )


    def run_per_test(self,idx):
        commands = ["contestant_source"]
        stdin_redirect="inputs" 
        stdin_redirect = os.path.join(stdin_redirect,"{}.in".format(idx))
        stdin_redirect = os.path.join(self.sandbox.secure_folder,stdin_redirect)
        stdout_redirect = "{}.out".format(idx)

        jury_output="outputs"
        jury_output = os.path.join(jury_output,"{}.out".format(idx))
        jury_output = os.path.join(self.sandbox.secure_folder,jury_output)
        processes=evaluation_step_before_run(self.sandbox,commands,self.time_limit,memory_limit= self.memory_limit,dirs_map=self.dirs_map,
                    stdin_redirect=stdin_redirect,stdout_redirect= stdout_redirect,multiprocess=self.multiprocess,wait=False)
        wait_without_std([processes])

        status_step= \
            evaluation_step_after_run(self.sandbox)
        if status_step[1] != True:
            # status_step[2]['value'] = 
            st = human_evaluation_message(status_step[2])
            # print(st)
            log = dict(
                name='TESTCASE',
                status = 'FAILED',
                participant_hint = st[1] + f" in testcase {idx}",
                judge_hint = "",
                step_status =st[0],
                info = status_step[2]
            )
            self.update_status(
                log=log
            )
            return {'status':'FAILED','meta':log}
        checker_exec = os.path.join(self.sandbox.secure_folder,"checker")

        commands = [[checker_exec] +[stdin_redirect] +[stdout_redirect]+ [jury_output] ]
        status_step = evaluation_step(self.sandbox, commands,self.time_limit,self.memory_limit,self.dirs_map,
            stdin_redirect=None, stdout_redirect=None,multiprocess=self.multiprocess)
        if status_step[1] != True:
            if status_step[2].get("exit_status",None) != 'nonzero return':

                st = human_evaluation_message(status_step[2])
                log =dict(
                    name='TESTCASE',
                    status = 'FAILED',
                    participant_hint = "CHECKER failed: this might not your fail pls contact admin : " +  st[0],
                    judge_hint = st[1],
                    step_status =st[0],
                    info = status_step[2]
                )
                return  {'status':'FAILED','meta':log}
            else:
                log = dict(
                    name='TESTCASE',
                    status = 'FAILED',
                    participant_hint = self.sandbox.get_stderr() + f" in testcase {idx}",
                    judge_hint ="",
                    step_status =CallbackJob.WRONG_ANSWER,
                    info = status_step[2]
                )
                self.update_status(log=log)
            return {'status':'FAILED','meta':log}

        log = dict(
            name='TESTCASE',
            status = 'SUCCESS',
            participant_hint = self.sandbox.get_stderr(),
            judge_hint ="",
            step_status =CallbackJob.ACCEPTED,
            info = status_step[2]
        )
        
        return {'status':'SUCCESS','meta':log}

    