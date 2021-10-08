#include <stdio.h>

void main()
{
  char *fp_buffer;
  char temp;
  int size = 0;
  int word_len = 0;
  int i = 0, j = 0;
  int result = 0;
  int arr[10] = {0,};

  FILE *fp;

  fp = fopen("keylog.txt", "r");

  if(fp == NULL){
    printf("파일열기 실패\n");
  } 

  fseek(fp, 0, SEEK_END);    
  size = ftell(fp) + 1; 
  rewind(fp);

  fp_buffer = (char *)malloc(size);
  
  while (!feof(fp)) 
  {
    fgets(fp_buffer,size,fp);
    for(i = 0 ; i < 3; i++)
    {
      //arr[fp_buffer[i]] = 1;
      printf("%d\n",fp_buffer[i]);
    }
    //printf("%s",fp_buffer);
  }

  for(i = 0 ; i < 10 ;i++)
  {
    if (arr[i] == 1)
    {
      printf("%d\n",i);
    }
  }

  fclose(fp);

}