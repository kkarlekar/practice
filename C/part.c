#include <stdio.h>
#include <stdbool.h>

bool part(int *s, int n, int total)
{
	if (total == 0)
		return true;

	if (n < 0 || total < 0) 
		return false;
	
        bool include = part(s, n-1, total - s[n]);
	if (include)
		return true;

	bool exclude = part(s, n-1, total);
	return exclude;
		
}


int main () 
{
	int s[] = {3,3,4};
	int total = 0;
	for (int i = 0; i< sizeof(s)/sizeof(s[0]); i++) {
		total =   total + s[i];	
	}


	if( part (s, sizeof(s)/sizeof(s[0]) - 1, total/2) == true) 
		printf("True\n");
	else
		printf("False\n");
}
