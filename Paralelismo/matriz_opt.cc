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

int main()
{
    vector<vector<int>> A;
    vector<vector<int>> X;

    A = {{0, 1, 3, g, g, g, g, g, 3, 6, g},
         {5, 0, 1, 8, g, g, g, g, 1, 8, g},
         {g, 9, 0, g, 8, g, g, g, g, 7, g},
         {g, g, g, 0, g, g, g, g, g, g, 7},
         {g, g, 7, g, 0, g, 2, 7, 5, g, 2},
         {g, 1, g, 4, g, 0, 7, g, g, 2, 7},
         {4, g, 7, g, g, g, 0, g, 4, 8, g},
         {g, g, g, g, g, 1, g, 0, g, 2, 7},
         {g, g, 7, g, 5, g, 2, 7, 0, g, 2},
         {g, g, 7, g, 3, g, 5, 7, g, 0, 3},
         {3, 1, 3, g, g, g, g, g, 3, 6, 0}};

    strange2(A, X);
    printMatrix(X);
    diameterMat(X);
    cout<<"\n!!!!!!!!!!!!Matriz original!!!!!!!!!!!!!!!!!"<<endl;
    printMatrix(A);
    return 0;
}
