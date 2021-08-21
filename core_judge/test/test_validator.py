






try:

    from ..job.OutputOnly import OutputOnly
    from ..job.validator import Validator

except:
    from job.OutputOnly import OutputOnly
    from job.validator import Validator
    from config import env





contestant_source = []
with open("/opt/source_code_for_testing/jury.cpp","r") as f:
    contestant_source = f.read()



job_description = {
    "id":1,
    "multiprocess":False,
    "time":3.,
    "jury_source":contestant_source,
    "jury_lang":"cpp",
    "checker":"/opt/problems_test/4/checker.cpp",
    "checker_lang":"cpp",
    "inputs":"/opt/problems_test/4/inputs",
    # "outputs":"/opt/problems_test/4/outputs",
    "type":"ioi",
    "sess":"submit",
}

wo = Validator(job_description)
# wo.prepare_file()
# wo.compiler()
wo.run()
wo.eval_status()
# wo.sandbox.cleanup()
# wo.sandbox.cleanup()