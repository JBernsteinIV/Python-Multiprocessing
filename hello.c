#include <stdio.h>

void usage() {
	printf("USAGE: ./hello NAME\n");
}

int addition(int a, int b) {
	return a + b;
}

int main(int argc, char** argv) {
	if (argc < 2) {
		usage();
		return 1;	
	}

	int x, y; 
	x = 5;
	y = 14;

	printf("The result of %d + %d = %d\n", x, y, addition(x,y));
	printf("Hello, %s\n", argv[1]);
	
	return 0;
}
