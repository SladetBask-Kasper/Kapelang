#pragma once
#include <iostream>
#include <vector>
void print(vector<int> items) 
{
	using namespace std;
	int x = 0;
	for (int item : items) {
		if (x >= 5) {
			cout << endl;
			x = 0;
		}
		cout << item << ", ";
		x++;
	}
	if (x != 0) {
		cout << endl;
	}
}
void print(vector<vector<double>> items)
{
	int x = 0;
	for (vector<double> item : items) {
		if (x >= 5) {
			cout << endl;
			x = 0;
		}
		int y = 0;
		for (double d : item) {
			if (y >= 5) {
				cout << endl;
				y = 0;
			}
			cout << d << ", ";
			y++;
		}
		x++;
	}
	if (x != 0) {
		cout << endl;
	}
}
void print(vector<vector<double>> x1, vector<vector<double>> x2, vector<int> y1, vector<int> y2)
{
	cout << "X_train(" << x1.size() << "):" << endl;
	print(x1);
	cout << "X_test(" << x2.size() << "):" << endl;
	print(x2);
	cout << "y_train(" << y1.size() << "):" << endl;
	print(y1);
	cout << "y_test(" << y2.size() << "):" << endl;
	print(y2);
}