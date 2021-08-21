
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

---------------------------------------------------------------------------------------------------
STRUCT Judge
core_jduge
|-isolate : Folder lưu core sandbox
|-job : Lưu các job chính của service bao gồm : validator-output_only-iteractive
    |-- iteractive.py 
    |-- outputOnly.py
    |-- validator.py
|-language: lưu định dạng mã nguồn file thí sinh, nhiệm vụ từ mã nguồn mà có câu lệnh run tương ứng ví dụ c++ thì là g++ x.cpp -o x.out etc...
|-sandbox: Binding API để gọi tới ISOLATE 