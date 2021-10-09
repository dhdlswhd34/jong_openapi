#include <stdio.h>

// 숫자 중복 체크 (중복 : 위치 리턴)
int check_num(int *result, int cur ,int num)
{
  int i = 0;
  for( i=0 ; i<cur ; i++)
  {
    if(result[i] == num)
    {
      return i;
    }
  }
  return -1;
}

void set_num_pos(int (*num_list)[2] , int *result , int cur)
{
  int i =0;
  memset(num_list, -1, 80);
  for( i=0 ; i<cur ; i++)
  {
    if(i == 0)
    {
      num_list[result[i]][1] = result[i+1];
    }
    else if(i+1 == cur)
    { 
      num_list[result[i]][0] = result[i-1];
    }
    else
    {
      num_list[result[i]][0] = result[i-1];
      num_list[result[i]][1] = result[i+1];
    }
  }
  return 0;
}

int main()
{
  // char *fp_buffer;
  // int temp = 0;
  // int temp_list[3];
  // int size = 0;
  // int word_len = 0;
  // int i = 0, j = 0;
  // int arr[10] = {0,};
  // int result[10] = {0,};
  // int num_List[10][2];
  // int cur = 0;
  // FILE *fp;

  // fp = fopen("keylog.txt", "r");

  // if(fp == NULL){
  //   printf("파일열기 실패\n");
  // } 

  // fseek(fp, 0, SEEK_END);    
  // size = ftell(fp) + 1; 
  // rewind(fp);


  // fp_buffer = (char *)malloc(size);
  // memset(result, -1, 10);
  // //memset(num_List, -1, sizeof(num_List) );
  // //첫번째 줄 넣기
  // fgets(fp_buffer,4,fp);
  // for(i = 0 ; i < 3; i++)
  // {
  //   result[i] = fp_buffer[i]-48;
  // }
  // cur = 3;  //현재 번호 길이
  // set_num_pos(num_List,result,cur);

  // while (!feof(fp)) 
  // {
  //   fgets(fp_buffer,4,fp);
  //   for(i = 0 ; i < 3; i++)
  //   {
  //     temp_list[i] = check_num(result, cur, fp_buffer[i]-48); // 중복 체크
  //   }  
    
  // }

  // // for(i = 0 ; i < 10 ;i++)
  // // {
  // //   if (arr[i] == 1)
  // //   {
  // //     printf("%d\n",i);
  // //   }
  // // }
  // for(i = 0 ; i < 10 ;i++)
  // { 
  //   printf("%d: ",i);
  //   for(j = 0 ; j < 2; j++){
  //     printf("%d ",num_List[i][j]);
  //   }
  //   printf("\n");
  // }
  // fclose(fp);

  return 0;
}