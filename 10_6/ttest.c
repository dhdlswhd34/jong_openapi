#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//참고
//https://blog.naver.com/PostView.nhn?blogId=tipsware&logNo=221301535902
//10월 7일 git 연결 다시 수정
int main()
{  
    int i =0,step=0;
    char temp_str[5];
    // char str_list[5][16] = {
    //   "\"tipsware\"","\"naver\"","\"microsoft\"","\"blog\"","\"mvp\""
    // };
    char str_list[5][16] = {
      "tipsware","naver","microsoft","blog","mvp"
    };

    for( i = 0 ; i < 5; i++ ){
        printf("%s\n",str_list[i]);
    }

    printf("-----------------\n");
    for(step =0 ; step < 4 ; step++ ){
        for(i=0 ; i < 4 -step ; i++ ){
            if(strcmp(str_list[i] , str_list[i+1]) >0 ){
                strcpy(temp_str,str_list[i]);
                strcpy(str_list[i],str_list[i+1]);
                strcpy(str_list[i+1],temp_str);
            }
        }
    }

    for(  i = 0 ; i < 5; i++ ){
        printf("%s\n",str_list[i]);
    }


    return 0;
}