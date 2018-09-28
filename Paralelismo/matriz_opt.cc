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
/*
    Para compilar: g++ -std=c++11 -o matriz matriz.cc
    Para ejecutar: ./matriz
*/
#define g INT_MAX
// #define g 100
int minimo(int a, int b)
{
    if (a < b)
        return a;
    else
        return b;
}

void printMatrix(vector<vector<int>>& A)
{
    int rows_A = A.size();
    int cols_A = A[0].size();

    for (int i = 0; i < rows_A; i++)
    {
        for (int j = 0; j < cols_A; j++)
        {
            if(A[i][j] == g)
                cout<<"g ";
            else
                cout << A[i][j] << " ";
        }
        cout << "\n";
    }
}

vector<vector<int>> matrixmult(vector<vector<int>>& A, vector<vector<int>>& B)
{
    int rows_A = A.size();
    int cols_A = A[0].size();
    int rows_B = B.size();
    int cols_B = B[0].size();

    vector<vector<int>> C;

    for (int i = 0; i < rows_A; i++)
    {
        vector<int> aux(cols_B, g);
        C.push_back(aux);
    }

    for (int i = 0; i < rows_A; i++)
        for (int j = 0; j < cols_B; j++)
            for (int k = 0; k < cols_A; k++)
            {   
                if(A[i][k] == g || B[k][j] == g)
                    C[i][j] = minimo(C[i][j], g);    
                else
                    C[i][j] = minimo(C[i][j], A[i][k] + B[k][j]);
            }

    return C;
}

void strange2(vector<vector<int>>& G, vector<vector<int>>& X)
{
    bool flag = false;
    int nodes = G.size();
    int cont = 0;
    X = G;


    if (nodes % 2 != 0)
    {
        flag = true;
        nodes = nodes - 1;
    }

    while (nodes != 1)
    {
        X = matrixmult(X, X);
        nodes = nodes / 2;
        cout<<nodes<<endl;
        cont++;
    }

    if (flag == true)
    {
        X = matrixmult(G, X);
        cont++;
    }

    cout<<"Number of multiplications (Strange2): "<<cont<<endl;

}

void diameterMat(vector<vector<int>>& G)
{
    int max=0;
    int x, y;
    for(int i=0; i<G.size(); i++)
        for(int j=0; j<G[0].size(); j++)
        {
            if(G[i][j] > max && G[i][j] != g)
            {
                max = G[i][j];
                x = i;
                y = j;
            }
        }

    cout<<"\nDiameter: "<<max<<endl;
    cout<<"X: "<<x<<" Y: "<<y<<endl;
}

void fillMatriz(vector<vector<int>>& A)
{
    string line;
    int nodeI, nodeF, weigth;
    ifstream dataRoma("romaData.txt");
    
    if (dataRoma.is_open())
    {   
        dataRoma >> line >> nodeI >> nodeF >> weigth;

        for(int i=0; i<nodeF; i++)
        {
            vector<int> aux(nodeF, g);
            A.push_back(aux);
        }
        // printMatrix(A);

        while (dataRoma.good())
        {
            dataRoma >> line >> nodeI >> nodeF >> weigth;
            // cout<<line<<" "<<nodeI<<" "<<nodeF<<" "<<weigth<<endl;
            A[nodeI-1][nodeF-1] = weigth;
        }
        
        // printMatrix(A);
        dataRoma.close();
    }
    else
    {
        cout << "Unable to open file";
    }
    
    for(int i=0; i<A.size(); i++)
        A[i][i]=0;
}

int main()
{   
    vector<vector<int>> A;
    vector<vector<int>> X;

    Timer fill;
    fillMatriz(A);
    cout<<"Tiempo de fillMatriz: "<<fill.elapsed()<<endl;

    Timer strg;
    strange2(A, X);
    cout<<"Tiempo de fillMatriz: "<<strg.elapsed()<<endl;
    
    // printMatrix(X);
    diameterMat(X);
    cout<<"\n!!!!!!!!!!!!Matriz original!!!!!!!!!!!!!!!!!"<<endl;
    // printMatrix(A);

    return 0;
}
