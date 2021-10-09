#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LEN_NAME 20
#define MAX_LEN 20000

/*
  환경: CentOS Linux release 7.9.2009 
  tool: gcc version 4.8.5 20150623 (Red Hat 4.8.5-44) (GCC)
*/

//버블 정렬
void BubleSortString(char (*buffer)[MAX_LEN_NAME], int name_size)
{
  int i,j;
  char temp[MAX_LEN_NAME];

  for(i = 0 ; i < name_size-1 ; i++ ){
      for( j = 0 ; j < name_size-1-i ; j++ ){
          if(strcmp(buffer[j] , buffer[j+1]) > 0 )    //알파벳 순으로 정렬
          {
              strcpy(temp,buffer[j]);
              strcpy(buffer[j],buffer[j+1]);
              strcpy(buffer[j+1],temp);
          }
      }
  }
}

//아스키 코드 점수 값 리턴
int GetNameScore(char (*buffer)[MAX_LEN_NAME], int count)
{
  int i;
  int len = strlen(buffer[count]);
  int result=0;

  for(i = 0 ; i < len ; i++)
  {
    result += buffer[count][i] - 64;
  }
  return result*(count+1);
}

int main()
{  
  FILE *fp;
  char *fp_buffer;
  char *temp;
  int size = 0;
  int name_size=0;
  int i = 0;
  int result=0;

  char buffer[MAX_LEN][MAX_LEN_NAME];

  fp = fopen("names.txt", "r");

  if(fp == NULL)
  {
    printf("file_open_error!\n");
    return 0;
  }

  fseek(fp, 0, SEEK_END);    
  size = ftell(fp) + 1;   //파일 사이즈 체크
  rewind(fp);

  fp_buffer = (char *)malloc(size);
  
  fgets(fp_buffer,size,fp);

  temp = strtok(fp_buffer,"\",\"");   //문자열 이름만 추출
  while(temp != NULL)
  {
    strcpy(buffer[i],temp);   //문자열 이름 복사
    temp = strtok(NULL,"\",\"");
    i++;
  }

  name_size = i;  //이름 총 개수

  /*버블 정렬*/
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