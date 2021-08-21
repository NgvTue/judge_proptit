
import logging
import os,sys
import os,sys,inspect
# currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0,parentdir) 
try:
   from ..sandbox.sandbox import IsolateSandbox as Sandbox
   from ..config import env
   from .messeger import HumanMessage
except:
   from sandbox.sandbox import IsolateSandbox as Sandbox
   from config import env
   from steps.messeger import HumanMessage
# from .messege import HumanMessage, MessageCollection
# from .util import generic_step
from .util import generic_step
logging.basicConfig(level=env.level_logging)
logger = logging.getLogger(__name__)

def N_(message):
    return message
COMPILATION_MESSAGES = list([
    HumanMessage("success",
                 N_("Compilation succeeded"),
                 N_("Your submission successfully compiled to an "
                    "executable.")),
    HumanMessage("fail",
                 N_("Compilation failed"),
                 N_("Your submission did not compile correctly.")),
    HumanMessage("timeout",
                 N_("Compilation timed out"),
                 N_("Your submission exceeded the time limit while compiling. "
                    "This might be caused by an excessive use of C++ "
                    "templates, for example.")),
    HumanMessage("signal",
                 N_("Compilation killed with signal %s (could be triggered "
                    "by violating memory limits)"),
                 N_("Your submission was killed with the specified signal. "
                    "Among other things, this might be caused by exceeding "
                    "the memory limit for the compilation, and in turn by an "
                    "excessive use of C++ templates, for example.")),
])



def compilation_step(sandbox, commands):
   # sandbox.add_mapped_directory("/etc")
   sandbox.preserve_env = True
   sandbox.max_processes = env.compilation_sandbox_max_processes
   sandbox.timeout = env.compilation_sandbox_max_time_s
   sandbox.wallclock_timeout = 2 * sandbox.timeout + 1
   sandbox.address_space = env.compilation_sandbox_max_memory_kib * 1024
   sandbox.max_processes = 1000
   # print("compila ste",commands)
   stats = generic_step(sandbox, commands, "compilation", collect_output=True)
   if stats is None:
         logger.debug("Sandbox failed during compilation. "
                     "See previous logs for the reason."
                     "{}".format(commands))
         logger.debug(commands)
         logger.debug(str(sandbox.get.get_log()))
         return False, None, None, None
   exit_status = stats["exit_status"]
  
   if exit_status == Sandbox.EXIT_OK:
      # Execution finished successfully and the executable was generated.
      logger.debug("Compilation successfully finished.")
      text = "Compilation succeeded"
      return True, True, text, stats

   elif exit_status == Sandbox.EXIT_NONZERO_RETURN:
      # Error in compilation: no executable was generated, and we return
      # an error to the user.
      logger.debug("Compilation failed.")
      text = "Compilation failed"
      return True, False, text, stats

   elif exit_status == Sandbox.EXIT_TIMEOUT or \
         exit_status == Sandbox.EXIT_TIMEOUT_WALL:
      # Timeout: we assume it is the user's fault, and we return the error
      # to them.
      logger.debug("Compilation timed out.")
      text ="Compilation timed out"
      return True, False, text, stats

   elif exit_status == Sandbox.EXIT_SIGNAL:
      # Terminated by signal: we assume again it is the user's fault, and
      # we return the error to them.
      signal = stats["signal"]
      logger.debug("Compilation killed with signal %s.", signal)
      text = "Compilation killed with signal %s.".format(signal)
      return True, False, text, stats

   elif exit_status == Sandbox.EXIT_SANDBOX_ERROR:
      # We shouldn't arrive here, as we should have gotten a False success
      # from execute_without_std.
      logger.error("Unexpected SANDBOX_ERROR exit status.")
      return False, None, None, None

   else:
      logger.error("Unrecognized sandbox exit status '%s'.", exit_status)
     
      return False, None, None, None