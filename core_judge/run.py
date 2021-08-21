
from job.OutputOnly import OutputOnly
from config import env

contestant_source = []
contestant_source = """
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
checker="""
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
"""
import glob
inputs = ['1907','2003']
outputs = ['112',"16"]
# inputs = glob.glob("/opt/problems_test/4/inputs/*.*")
# outputs = glob.glob("/opt/problems_test/4/outputs/*.*")
# inputs  = sorted(inputs)
# outputs  = sorted(outputs)
# inputs = [open_and_read(i) for i in inputs] #["1","2"]
# outputs = [open_and_read(i) for i in outputs] 
print(inputs)
print(outputs)
job_description = {
    "multiprocess":False,
    "time":1,
    "contestant_source":contestant_source,
    "contestant_lang":"cpp",
    "checker":checker, #"/opt/problems_test/4/checker_c.cpp",
    "checker_lang":"cpp",
    "inputs": inputs,#"/opt/problems_test/4/inputs", # list inputs
    "outputs":outputs,#"/opt/problems_test/4/outputs", # list_outputs
    "type":"ioi",
    "sess":"submit",
    "inputs_from_string":"True",
}
# 1000 testcase
wo = OutputOnly(job_description)
# wo.prepare_file()
# wo.compiler()
wo.run()
wo.eval_status()
wo.sandbox.cleanup()