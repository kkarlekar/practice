#include <stdio.h>
#include <stdbool.h>


int max(int a, int b) 
{
	if (a>b) 
		return a;
	else
		return b; 
}

int knapsack(int W, int *val, int *wt, int n)
{
	if (n <=0 || W <=0)
		return 0;

	if (wt[n-1] > W) 
		return knapsack(W, val, wt, n-1);
	else
		return(max (knapsack(W, val, wt, n-1),
			val[n-1] + knapsack(W-wt[n-1], val, wt, n-1)));

}

int main()
{
	int val[] = {60, 100, 120};
	int wt[] = {10, 20,30};
	int W = 35;

	int no_of_items = sizeof(val)/sizeof(val[0]);
	printf("%d\n", knapsack(W, val, wt, no_of_items));
}
