
judge test proptit

REFERENCES:

    IOI-ISOLATE: [ISOLATE](https://github.com/ioi/isolate)

    CMS-DEV : [CMS-DEV](https://cms-dev.github.io/)

---

PROVIDE:

1. OUTPUT_INPUT_STANDART_JUDGE
2. ITERACTIVE_JUDGE
3. VALDATOR_JUDGE
4. CHECKER WITH TESTLIB
[ISOLATE](https://github.com/ioi/isolate)

---
STRUCT Judge

core_jduge

|-isolate : Folder lưu core sandbox

|-job : Lưu các job chính của service bao gồm : validator-output_only-iteractive

    |-- iteractive.py 

    |-- outputOnly.py

    |-- validator.py

|-language: lưu định dạng mã nguồn file thí sinh, nhiệm vụ từ mã nguồn mà có câu lệnh run tương ứng ví dụ c++ thì là g++ x.cpp -o x.out etc...

|-sandbox: Binding API để gọi tới ISOLATE 

---

API:

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

---

# RUN  SERVER

docker-compose up -d -build

port:8000

1. Go to 127.0.0.1:8000/docs

---

1. Call API job judge to worker.
2. Server will return the key which define your unique job.
3. Call api with get_task : to view progress in your job with id_task.

---
