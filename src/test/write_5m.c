#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main() {
  FILE* fp;
  char data[5 * 1024 * 1024];
  size_t result = 0;
  memset(data, '_', sizeof(data));
  data[0] = 'S';
  data[-1]= 'E';
  fp = fopen("/dev/bytes4m", "wb");
  result = fwrite(data, 1, 5 * 1024 * 1024, fp);
  printf("result = %zu bytes\n", result);
 
  fclose(fp);
  return 1;
}
