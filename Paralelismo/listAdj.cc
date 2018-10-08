#include <iostream>
#include <cstdlib>
#include <fstream>
#include <string>
#include <utility>
#include <string.h>
#include <vector>
#include <math.h>
#include <limits.h>
#include <typeinfo>
#include "timer.hh"

using namespace std;

void fillListAd(vector<vector<pair<int, int>>>& A)
{
    string line;
    int nodeI, nodeF, weigth;
    ifstream dataRoma("dataRoma.txt");
    
    if (dataRoma.is_open())
    {   
        getline(dataRoma, line);
        // while (getline(dataRoma, line))
        // {
            cout << line << '\n';
            for(int i=0; i<line.size(); i++)
                cout<<line[i]<<" ";
        // }
        
        dataRoma.close();
    }
    else
    {
        cout << "Unable to open file";
    }
}

int main()
{
    vector<vector<pair<int, int>>> A;

    fillListAd(A);

    return 0;
}
