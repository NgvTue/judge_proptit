import json
from logging import log
import logging
from celery.result import AsyncResult
from fastapi import Body, FastAPI, Form, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, List
from fastapi.encoders import jsonable_encoder
from worker import create_task, judge_session, celery

class Job(BaseModel):
    multiprocess:bool = False
    time : float = 1.
    contestant_source:str = """
        #include<bits/stdc++.h>
        using namespace std;
        int a[10];
        int main(){
            int t;
            cin>>t;
            cout<<2019-t<<endl;
            while(true){
                cout<<t<<endl;
            }
        }
    """
    contestant_lang:str = 'cpp'
    checker:str="""
        #include "testlib.h"
        #include<vector>

        int main(int argc, char * argv[]){
            registerTestlibCmd(argc,argv);
            int anss = ans.readInt();
            
            int step =ouf.readInt();

            if (anss!=step){
                quitf(_wa, "expected %d , got %d", anss, step);
            }
            else
            {
                quitf(_ok,"Correct Answer");
            }
        }
    """ #"/opt/problems_test/4/checker_c.cpp",
    checker_lang:str = 'cpp'
    inputs: List[str]= ['1907','2003']#"/opt/problems_test/4/inputs", # list inputs
    outputs: List[str]=['112',"16"]#"/opt/problems_test/4/outputs", # list_outputs
    type:str = 'ioi'
    sess:str = 'submit'
    inputs_from_string:str = "True"

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.post("/submit")
async def submit(item: Job):
    logging.info(str(item))
    item = jsonable_encoder(item)
    task = celery.send_task("judge", [item,])
   
    return {'item':task.id}

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", context={"request": request})


@app.post("/tasks", status_code=201)
def run_task(payload = Body(...)):
    task_type = payload["type"]
    task = create_task.delay(int(task_type))
    return JSONResponse({"task_id": task.id})


@app.get("/tasks/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)


