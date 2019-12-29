#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

int max (int i, int j)
{
	if(i>j) 
		return i;
	else
		return j;
}

int lsc (char *str1, char *str2, int i, int j, int *memo[])
{

	if (memo[i][j] != -1) {
		return memo[i][j];
	} 
	if (str1[i] == '\0' || str2[j] == '\0') {
		memo[i][j] = 0;
		return 0;
	} else if (str1[i] == str2[j]) {
		memo[i][j] = 1 + lsc(str1, str2, i+1, j+1, memo);
		return memo[i][j];
	} else {
		memo[i][j] = (max (lsc(str1, str2, i+1, j, memo), lsc(str1,str2, i, j+1, memo)));
		return memo[i][j];
	}
}


int main(int argc, char **argv)
{
	if (argc < 2) {
		printf("usage %s str1 str2\n", argv[0]);
		exit(1);
	}
	int len1 =   strlen(argv[1]);
	int len2 =   strlen(argv[2]);
	int **memo = malloc(len1 *sizeof(int *));
	for (int i =  0; i < len1; i++) {
		memo[i] = malloc((len2 + 1) *sizeof(int));
		for (int j = 0; j < len2 +1; j++) 
			memo[i][j] = -1;
	}
	

	int count =  lsc(argv[1], argv[2], 0, 0, memo);
	printf ("%d\n", count);
}
