#include <stdio.h>
#include <stdbool.h>


int max(int a, int b)
{
	if (a>b)
		return a;
	else
		return b;
}


int main()
{
	int val[] = {60, 100, 120};
	int wt[] = {10, 20,30};
	int W = 35;

	int no_of_items = sizeof(val)/sizeof(val[0]);
	printf("%d\n", knapsack_dp(W, val, wt, no_of_items));
}

