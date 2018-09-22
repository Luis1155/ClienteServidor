#include <iostream>
#include <cstdlib>
#include <fstream>
#include <string>
#include <utility>
#include <string.h>
#include <vector>
#include <tuple>
#include <math.h>
#include <limits.h>

using namespace std;

#define g INT_MAX

vector <vector <int>> matrixmult (vector <vector <int>> A, vector <vector <int>> B)
{
    int rows_A = A.size();
    int cols_A = A[0].size();
    int rows_B = B.size();
    int cols_B = B[0].size();

    vector <vector <int>> C;

    if(cols_A != rows_B)
        cout<<"Cannot multiply the two matrices. Incorrect dimensions."<<endl;

    for(int i=0; i<rows_A; i++){
        vector<int> aux(cols_B, g);

    }

    for(int i=0; i<rows_A; i++)
        for(int j=0; i<cols_B; j++)
            for(int k=0; k<cols_A; k++)


}