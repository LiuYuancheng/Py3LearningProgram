#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>

int lcd;

void test() {
	int k, i, sum;
	char s[3];
	memset(s, '2', sizeof(s));

	printf("test begin!\n");

	k = lseek(lcd, 4, SEEK_CUR);
	printf("lseek = %d\n", k);

	k = write(lcd, s, sizeof(s));
	printf("written = %d\n", k);

	k = lseek(lcd, 0, SEEK_END);
	printf("lseek = %d\n", k);

	k = lseek(lcd, -4, SEEK_END);
	printf("lseek = %d\n", k);

	k = lseek(lcd, -4, -1);
	printf("lseek = %d\n", k);
}

void initial(char i) {
	char s[10];
	memset(s, i, sizeof(s));
	write(lcd, s, sizeof(s));
  char c[20] = "";
	int k = lseek(lcd, 0, SEEK_SET);
	printf("lseek = %d\n", k);
}

int main(int argc, char **argv) {
	lcd = open("/dev/bytes4m", O_RDWR);
	if (lcd == -1) {
		printf("unable to open lcd");
		exit(EXIT_FAILURE);
	}
	initial('1');
	test();
	close(lcd);
	return 0;
}

