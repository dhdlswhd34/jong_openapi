CC = gcc
CFLAGS = -W -Wall
TARGET = test_out
OBJECT = test1.o test2.o test3.o 

$(TARGET) : $(OBJECT)
	$(CC) $(CFLAGS) -o test1_out test1.o
	$(CC) $(CFLAGS) -o test2_out test2.o
	$(CC) $(CFLAGS) -o test3_out test3.o

# test.o : test1.c test2.c test3.c
# 	$(CC) $(CFLAGS) -c -o test1.o test1.c
# 	$(CC) $(CFLAGS) -c -o test3.o test3.c
# 	$(CC) $(CFLAGS) -c -o test3.o test3.c


clean :
	rm -rf out/*
	rm -rf *.o *_out
