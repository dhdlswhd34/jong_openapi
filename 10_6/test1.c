#include <stdio.h>
#include <stdlib.h>
#include <string.h>



int main()
{  
  FILE *fp;
  char *buffer;
  char *temp;
  int size = 0;
  int i = 0;
  fp = fopen("names.txt", "r");

  if(fp == NULL)
  {
    printf("file_open_error!\n");
    return 0;
  }
  fseek(fp, 0, SEEK_END);    
  size = ftell(fp) + 1; 
  rewind(fp);

  buffer = (char *)malloc(size);
  
  fgets(buffer,size,fp);

  char * ttemp;
  temp = strtok(buffer,",");
  while(temp != NULL)
  {
    ttemp = temp;
    temp = strtok(NULL,",");
  }

  fclose(fp);
  free(buffer);

  return 0;
}