#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/slab.h>
#include <linux/errno.h>
#include <linux/types.h>
#include <linux/fs.h>
#include <linux/proc_fs.h>
#include <asm/uaccess.h>
#include <linux/ioctl.h>
#include <linux/string.h>

struct dev_msg_t {
  char data[100];
};

#define MAJOR_NUMBER 66
#define DEV_SIZE 4 * 1024 * 1024
#define LCD_IOC_MAGIC 'k'
#define LCD_IOC_HELLO _IO(LCD_IOC_MAGIC, 1)
#define LCD_IOC_WRITE _IOW(LCD_IOC_MAGIC, 2, struct dev_msg_t)
#define LCD_IOC_READ _IOR(LCD_IOC_MAGIC, 3, struct dev_msg_t)
#define LCD_IOC_WR _IOWR(LCD_IOC_MAGIC, 4, struct dev_msg_t)

/* forward declaration */
int lcd_open(struct inode *inode, struct file *filep);
int lcd_release(struct inode *inode, struct file *filep);
loff_t lcd_llseek(struct file* filep, loff_t offset, int whence);
ssize_t lcd_read(struct file *filep, char *buf, size_t count, loff_t *f_pos);
ssize_t lcd_write(struct file *filep, const char *buf, size_t count, loff_t *f_pos);
long lcd_ioctl(struct file* filep, unsigned int cmd, unsigned long arg);
static void lcd_exit(void);

/* definition of file_operation structure */
struct file_operations lcd_fops = {
  llseek: lcd_llseek,
  read: lcd_read,
  write: lcd_write,
  open: lcd_open,
  release: lcd_release,
  .unlocked_ioctl = lcd_ioctl
};

char *lcd_data = NULL;
size_t stored = 0;
struct dev_msg_t dev_msg;

int lcd_open(struct inode *inode, struct file *filep)
{
  return 0; // always successful
}

int lcd_release(struct inode *inode, struct file *filep)
{
  return 0; // always successful
}

long lcd_ioctl(struct file* filep, unsigned int cmd, unsigned long arg)
{
  struct dev_msg_t* msg;
  struct dev_msg_t tmp;
  int retval = 0;   

  if (_IOC_TYPE(cmd) != LCD_IOC_MAGIC) return -ENOTTY;
  //if (_IOC_NR(cmd) > LCD_IOC_MAGIC) return ‐ENOTTY; 
  switch (cmd) {
    case LCD_IOC_HELLO:
      printk(KERN_WARNING "Hello.\n");
      break;
    case LCD_IOC_WRITE:
      msg = (struct dev_msg_t*) arg;
      copy_from_user(dev_msg.data, msg->data, 99);
      printk("write %s\n", dev_msg.data);
      break;
    case LCD_IOC_READ:
      msg = (struct dev_msg_t*) arg;
      copy_to_user(msg->data, dev_msg.data, 99);
      break;
    case LCD_IOC_WR:
      msg = (struct dev_msg_t*) arg;
      copy_from_user(tmp.data, msg->data, 99);
      copy_to_user(msg->data, dev_msg.data, 99);
      strncpy(dev_msg.data, tmp.data, 99);
      printk("LCD_IOC_WR dev_msg = %s\n", dev_msg.data);
      break;  
    default:
      return -ENOTTY;
  }
  return retval;
}

loff_t lcd_llseek(struct file* filep, loff_t offset, int whence)
{
  loff_t new_pos = 0;
  switch (whence) 
  {
    case 0: new_pos = offset;  // SEEK_SET
      break;
    case 1: new_pos = filep->f_pos + offset;  // SEEK_CUR
      break;
    case 2: new_pos = stored + offset;  // SEEK_END
      break;
    default: return -EINVAL;
  }
  if (new_pos < 0) return -EINVAL;
  if (new_pos > stored) new_pos = stored;
  filep->f_pos = new_pos;
  return new_pos;
}

ssize_t lcd_read(struct file *filep, char *buf, size_t count, loff_t *f_pos)
{
  if (*f_pos > stored) return -1;
  if (count + (*f_pos) > stored) count = stored - *f_pos;
  copy_to_user(buf, lcd_data + *f_pos, count);
  *f_pos += count;
  return count;
}

ssize_t lcd_write(struct file *filep, const char *buf, size_t count, loff_t *f_pos)
{
  if (*f_pos >= DEV_SIZE) return -ENOSPC;
  if (count + (*f_pos) > DEV_SIZE) count = DEV_SIZE - *f_pos;
  copy_from_user(lcd_data + *f_pos, buf, count);
  *f_pos += count;
  stored = *f_pos;
  if (stored == DEV_SIZE) return DEV_SIZE;
  return count;
  /*
  if (count > 1) {
    printk(KERN_INFO "lcd: try to write %zu bytes %s\n", count, buf);
    return -ENOSPC;
  }
  */
}

static int lcd_init(void)
{
  int result;
  // register the device
  result = register_chrdev(MAJOR_NUMBER, "bytes4m", &lcd_fops);
  if (result < 0) {
    return result;
  }
  // allocate one byte of memory for storage
  // kmalloc is just like malloc, the second parameter is
  // the type of memory to be allocated.
  // To release the memory allocated by kmalloc, use kfree.
  lcd_data = kmalloc(DEV_SIZE, GFP_KERNEL);
  if (!lcd_data) {
    lcd_exit();
    // cannot allocate memory
    // return no memory error, negative signify a failure
    return -ENOMEM;
  }
  // initialize the value to be X
  *lcd_data = '\0';
  dev_msg.data[99] = '\0';
  printk(KERN_ALERT "This is a 4m device module\n");
  return 0;
}

static void lcd_exit(void)
{
  // if the pointer is pointing to something
  if (lcd_data) {
    // free the memory and assign the pointer to NULL
    kfree(lcd_data);
    lcd_data = NULL;
  }

  // unregister the device
  unregister_chrdev(MAJOR_NUMBER, "bytes4m");
  printk(KERN_ALERT "4m device is unloaded\n");
}

MODULE_LICENSE("GPL");
module_init(lcd_init);
module_exit(lcd_exit);
