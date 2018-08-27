#include <stdio.h>

void usage() {
	printf("USAGE: ./hello NUMBER NUMBER\n");
}

int addition(int a, int b) {
	return a + b;
}

int main(int argc, char** argv) {
	if (argc < 3 || argc > 3) {
		usage();
		return 1;	
	}
	
	int x, y;
	x = atoi(argv[1]);
	y = atoi(argv[2]);
	
	printf("The result of %d + %d = %d\n", x, y, addition(x,y));
	
	return 0;
}
