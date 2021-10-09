#include <stdio.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define KEY_LEN 3
#define WORD_MAX 20000

/*
  환경: CentOS Linux release 7.9.2009 
  tool: gcc version 4.8.5 20150623 (Red Hat 4.8.5-44) (GCC)
  
  특수문자 빈도수 https://linguistics.stackexchange.com/questions/12324/special-characters-and-uppercase-frequency
*/

//복호화
int FinfSpecialCharchar(char(*en_List)[WORD_MAX], char key[] , int word_len)
{
  int i =0;
  int result = 0;
  for(i = 0 ; i < word_len ; i++)
  {
    printf("%c",en_List[i%3][i/3]^key[i%3]);
    result += en_List[i%3][i/3]^key[i%3];
  }
  printf("\n");
  return result;
}

//최다 빈도 특수문자 체크
int GetMostChar(char (*en_List)[WORD_MAX], int index, int word_len)
{  
  int temp[128] = {0,};
  int result = 0;
  int i =0;
  #if 1
  for(i = 0 ; i < word_len/3 ; i++ )    //각자리 길이
  {
    if (en_List[index][i] > 64)   // 0100 0000 이상 특수문자만 체크
    {
      temp[en_List[index][i]]++;
    }
  }

  for(i = 0 ; i < 128 ; i++ )
  {
    if (temp[i] > result)   //최다 특수문자  리턴
    {
      result = i;
    }
  }
  #endif
  return result;
}


int main()
{
  int size = 0;
  int word_len = 0;
  int i = 0, j = 0;
  int result = 0;

  char *fp_buffer;
  char *temp;
  char key_input;
  char en_List[KEY_LEN][WORD_MAX];
  char key[KEY_LEN];
  char SPECIALCHAR[128] = {' ',',', '.', '"', ')', '(', '?', ':', '\'', ';', '-', '*', '@', '%', '$', '#'};   //빈도수에 따른 특수문자

  FILE *fp;

  fp = fopen("cipher1.txt", "r");

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

  temp = strtok(fp_buffer,",");   // , 기준으로 char 자르기
  
  while(temp != NULL)
  {
    en_List[i%3][i/3] = atoi(temp);   //키 위치에 맞게 분리
    temp = strtok(NULL,",");
    i++;
  }

  word_len = i;   //문장 길이(특수문자 포함)

  for(i = 0 ; SPECIALCHAR[i] != NULL; i++)
  {
    for(j = 0 ; j < 3 ; j++)
    {
      key[j] = GetMostChar(en_List,j,word_len);   //각 자리마다 최다 빈도 특수문자 체크
      key[j] = key[j]^SPECIALCHAR[i];   //키값 찾기
      printf("%c\n",key[j]);
    }

    result = FinfSpecialCharchar(en_List, key, word_len); //복호화
    printf("correct -> y | continue -> anykey");
    scanf("%c",&key_input);
    if(key_input == 'y')
    {
      printf("result: %d\n", result);
      return 0;
    }
  }

  fclose(fp);
   
  return 0;
}