#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main() {
  FILE* fp;
  char data[5 * 1024 * 1024];
  size_t written = 0;

  memset(data, '0', sizeof(data));
  data[0] = 'S';
  data[-1]= 'e';
  fp = fopen("/dev/onebyte4m", "wb");
  written = fwrite(data, sizeof(char), sizeof(data)/sizeof(char), fp);
  fclose(fp);
  printf("%lu\n", written);

  return 1;
}
