#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//참고
//https://blog.naver.com/PostView.nhn?blogId=tipsware&logNo=221301535902
//10월 7일 git 연결
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

  temp = strtok(buffer,",");
  printf("%s",temp);
  while(temp != NULL)
  {
    temp = strtok(NULL,",");
  }

  fclose(fp);
  free(buffer);

  return 0;
}