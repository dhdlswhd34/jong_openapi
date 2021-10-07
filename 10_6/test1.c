#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//참고
//10월 7일 완료 -> 주석 및 환경 알려주기
#define MAX_LEN_NAME 20
#define MAX_LEN 20000


void BubleSortString(char (*buffer)[MAX_LEN_NAME], int name_size)
{
  int i,j;
  char temp[MAX_LEN_NAME];

  for(i = 0 ; i < name_size-1 ; i++ ){
      for( j = 0 ; j < name_size-1-i ; j++ ){
          if(strcmp(buffer[j] , buffer[j+1]) > 0 ){
              strcpy(temp,buffer[j]);
              strcpy(buffer[j],buffer[j+1]);
              strcpy(buffer[j+1],temp);
          }
      }
  }
}

int GetNameScore(char (*buffer)[MAX_LEN_NAME], int count)
{
  int i;
  int len = strlen(buffer[count]);
  int result=0;

  for(i = 0 ; i < len ; i++)
  {
    result += buffer[count][i] - 64;
    //printf("%s %c %d\n",buffer[count],buffer[count][i],buffer[count][i]-64);
  }
  //printf("%d %d\n",result,result * (count+1));
  return result*(count+1);
}

int main()
{  
  FILE *fp;
  char *fp_buffer;
  char *temp;
  int size = 0;
  int name_size=0;
  int i = 0, j = 0;
  int result=0;

  char buffer[MAX_LEN][MAX_LEN_NAME];

  fp = fopen("names.txt", "r");

  if(fp == NULL)
  {
    printf("file_open_error!\n");
    return 0;
  }

  fseek(fp, 0, SEEK_END);    
  size = ftell(fp) + 1; 
  rewind(fp);

  fp_buffer = (char *)malloc(size);
  
  fgets(fp_buffer,size,fp);

  temp = strtok(fp_buffer,"\",\"");
  while(temp != NULL)
  {
    strcpy(buffer[i],temp);
    temp = strtok(NULL,"\",\"");
    i++;
  }

  name_size = i;

  // /*버블 정렬*/
  BubleSortString(buffer,name_size);

  for( i = 0 ; i < name_size; i++ ){
      //printf("%s\n",buffer[i]);
      result += GetNameScore(buffer,i);
  }

  printf("fin result %d\n",result);
  fclose(fp);
  free(fp_buffer);

  return 0;
}