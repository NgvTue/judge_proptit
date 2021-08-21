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