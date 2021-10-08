#include <stdio.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define KEY_LEN 3
#define WORD_MAX 20000



/*
10월 8일 완성 -> 코드 정리 and 주석 and fix 
알파벳 3개 연속으로 반복 소문자

특수문자 빈도수
https://linguistics.stackexchange.com/questions/12324/special-characters-and-uppercase-frequency
*/

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

int GetMostChar(char (*en_List)[WORD_MAX], int index, int word_len)
{  
  int temp[128] = {0,};
  int result = 0;
  int i =0;
  #if 1
  for(i = 0 ; i < word_len/3 ; i++ )
  {
    if (en_List[index][i] > 64)
    {
      temp[en_List[index][i]]++;
    }
  }

  for(i = 0 ; i < 128 ; i++ )
  {
    if (temp[i] > result)
    {
      result = i;
    }
  }
  #endif
  return result;
}


int main()
{
  char *fp_buffer;
  char *temp;
  int size = 0;
  int word_len = 0;
  int i = 0, j = 0;
  int result = 0;
  char key_input;
  char en_List[KEY_LEN][WORD_MAX];
  char key[KEY_LEN];
  char SPECIALCHAR[128] = {' ',',', '.', '"', ')', '(', '?', ':', '\'', ';', '-', '*', '@', '%', '$', '#'};

  FILE *fp;

  fp = fopen("cipher1.txt", "r");

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

  temp = strtok(fp_buffer,",");
  
  while(temp != NULL)
  {
    en_List[i%3][i/3] = atoi(temp);
    temp = strtok(NULL,",");
    i++;
  }
  word_len = i;


  printf("%d\n",(word_len/3) +( word_len%3));
  printf("%d\n",(word_len/3)  );
  printf("%d\n",( word_len%3));
  printf("%d\n",( word_len));
  for(i = 0 ; SPECIALCHAR[i] != NULL; i++)
  {
    for(j = 0 ; j < 3 ; j++)
    {
      key[j] = GetMostChar(en_List,j,word_len);
      key[j] = key[j]^SPECIALCHAR[i];
      printf("%c\n",key[j]);
    }
    result = FinfSpecialCharchar(en_List, key, word_len);
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