try:

    from ..job.OutputOnly import OutputOnly

except:
    from job.OutputOnly import OutputOnly
    from config import env

contestant_source = []
with open("/opt/source_code_for_testing/par.cpp","r") as f:
    contestant_source = f.read()
def open_and_read(f):
    with open(f,"r") as ff:
        return ff.read()
import glob

inputs = glob.glob("/opt/problems_test/4/inputs/*.*")
outputs = glob.glob("/opt/problems_test/4/outputs/*.*")
inputs  = sorted(inputs)
outputs  = sorted(outputs)
inputs = [open_and_read(i) for i in inputs] #["1","2"]
outputs = [open_and_read(i) for i in outputs] 
print(inputs)
print(outputs)
job_description = {
    "multiprocess":False,
    "time":3.,
    "contestant_source":contestant_source,
    "contestant_lang":"cpp",
    "checker":"/opt/problems_test/4/checker_c.cpp",
    "checker_lang":"cpp",
    "inputs": inputs,#"/opt/problems_test/4/inputs", # list inputs
    "outputs":outputs,#"/opt/problems_test/4/outputs", # list_outputs
    "type":"ioi",
    "sess":"submit",
    "inputs_from_string":"True"
}

wo = OutputOnly(job_description)
# wo.prepare_file()
# wo.compiler()
wo.run()
wo.eval_status()
wo.sandbox.cleanup()