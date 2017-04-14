#include <stdio.h> 
#include <stdlib.h> 
#include <fcntl.h> 
#include <sys/ioctl.h>  
//needed for IO things. Attention that this is different from kernel mode 
int lcd; 
struct dev_msg_t {
  char data[100];
};
#define LCD_IOC_MAGIC  'k' 
#define LCD_IOC_HELLO _IO(LCD_IOC_MAGIC,   1) 
#define LCD_IOC_WRITE _IOW(LCD_IOC_MAGIC, 2, struct dev_msg_t)
#define LCD_IOC_READ _IOR(LCD_IOC_MAGIC, 3, struct dev_msg_t)
#define LCD_IOC_WR _IOWR(LCD_IOC_MAGIC, 4, struct dev_msg_t)

void test()
{ 
  int k, i, sum; 
  char s[3]; 
  struct dev_msg_t dev_msg;
  memset(dev_msg.data, 0, sizeof(dev_msg.data));
  memset(s, '2', sizeof(s)); 
  printf("test begin!\n"); 

  k = write(lcd, s, sizeof(s)); 
  printf("written = %d\n", k); 
  k = ioctl(lcd, LCD_IOC_HELLO); 
  printf("result = %d\n", k); 

  strcpy(dev_msg.data, "ioctl_write");
  k = ioctl(lcd, LCD_IOC_WRITE, &dev_msg);
  printf("write result = %d msg = %s\n", k, dev_msg.data);

  memset(dev_msg.data, 0, sizeof(dev_msg.data));
  printf("cleara msg = %s\n", dev_msg.data);
  k = ioctl(lcd, LCD_IOC_READ, &dev_msg);
  printf("read result = %d msg = %s\n", k, dev_msg.data);

  strcpy(dev_msg.data, "ioctl_exchange");
  printf("before exchange msg = %s\n", dev_msg.data);
  k = ioctl(lcd, LCD_IOC_WR, &dev_msg);
  printf("exchange result = %d msg = %s\n", k, dev_msg.data);

  memset(dev_msg.data, 0, sizeof(dev_msg.data));
  k = ioctl(lcd, LCD_IOC_READ, &dev_msg);
  printf("read result = %d msg = %s\n", k, dev_msg.data);
} 

int main(int argc, char **argv) 
{ 
  lcd = open("/dev/bytes4m", O_RDWR); 
  if (lcd == -1) { 
    perror("unable to open bytes4m"); 
    exit(EXIT_FAILURE); 
  } 


  test(); 

  close(lcd); 
  return 0; 
}
