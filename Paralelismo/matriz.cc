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

    if (cols_A != rows_B)
        cout << "Cannot multiply the two matrices. Incorrect dimensions." << endl;

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

vector<vector<int>> strange(vector<vector<int>>& G)
{
    int nodes = G.size();
    int cont = 0;
    vector<vector<int>> A = G;

    for (int i = 0; i < nodes; i++)
    {
        A = matrixmult(G, A);
        cont++;
    }
    cout<<"Number of multiplications (Strange): "<<cont<<endl;

    return A;
}

vector<vector<int>> strange2(vector<vector<int>>& G)
{
    bool flag = false;
    int nodes = G.size();
    int cont = 0;
    vector<vector<int>> A = G;
    vector<vector<int>> path;
    
    cout<<"condicional"<<endl;
    
    if (nodes % 2 != 0)
    {
        flag = true;
        nodes = nodes - 1;
    }

    while (nodes != 1)
    {
        A = matrixmult(A, A);
        nodes = nodes / 2;
        cont++;
    }

    if (flag == true)
    {
        A = matrixmult(G, A);
        cont++;
    }

    cout<<"Number of multiplications (Strange2): "<<cont<<endl;

    return A;
}

int main()
{
    vector<vector<int>> A;
    vector<vector<int>> X;

    // A = {{0, g, 3, g},
    //      {g, 0, g, g},
    //      {g, g, 0, 1},
    //      {3, 1, g, 0}};
         
    A = {{0, 6, g, g, 6, g, g, g},
         {4, 0, g, g, g, g, g, g},
         {g, g, 0, g, 2, 9, 7, g},
         {g, g, g, 0, g, g, g, g},
         {g, g, 4, g, 0, g, g, g},
         {g, g, g, g, g, 0, g, 9},
         {g, g, g, g, 6, 2, 0, g},
         {g, g, g, g, g, g, g, 0}};

    // A = {{0, 1, 3, g, g, g, g, g, 3, 6, g},
        //  {5, 0, 1, 8, g, g, g, g, 1, 8, g},
        //  {g, 9, 0, g, 8, g, g, g, g, 7, g},
        //  {g, g, g, 0, g, g, g, g, g, g, 7},
        //  {g, g, 7, g, 0, g, 2, 7, 5, g, 2},
        //  {g, 1, g, 4, g, 0, 7, g, g, 2, 7},
        //  {4, g, 7, g, g, g, 0, g, 4, 8, g},
        //  {g, g, g, g, g, 1, g, 0, g, 2, 7},
        //  {g, g, 7, g, 5, g, 2, 7, 0, g, 2},
        //  {g, g, 7, g, 3, g, 5, 7, g, 0, 3},
        //  {3, 1, 3, g, g, g, g, g, 3, 6, 0}};
 
    X = strange(A);
    printMatrix(X);
    cout<<"\n";
    X = strange2(A);
    printMatrix(X);
    cout<<"\n!!!!!!!!!!!!Matriz original!!!!!!!!!!!!!!!!!"<<endl;
    printMatrix(A);
    return 0;
}
