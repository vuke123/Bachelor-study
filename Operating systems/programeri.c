#include <stdio.h>
#include <sys/shm.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <signal.h>
#include <pthread.h>
#include <unistd.h>
#include<wait.h>
#include <time.h>

#define programeri 10
int vrsta;  //globalna medudretvena varijabla, oznaka firmi
pthread_mutex_t monitor;
pthread_cond_t uvjet[2];
int cekanje[2];
int usao[2];
int sit[2]; //da sprijecimo izgladnjivanje


void Udi(int vrsta){ 
    pthread_mutex_lock(&monitor);
    cekanje[vrsta]++;

    while (usao[1-vrsta]>0 || (sit[vrsta]>programeri && cekanje[1-vrsta]>0 )) 
        pthread_cond_wait(&uvjet[vrsta],&monitor);

    cekanje[vrsta]--;  
    usao[vrsta]++; 
    sit[1-vrsta]=0; 


    pthread_mutex_unlock (&monitor);
}

void Izadi(int vrsta){ 
    pthread_mutex_lock (&monitor);

    usao[vrsta]--;

    if(usao[vrsta]==0)
        pthread_cond_broadcast(&uvjet[1-vrsta]);

    if(vrsta==1)
        printf("Linux Programer izašao\n");
    else if(vrsta==0) 
	printf("Microsoft Programer izašao\n");

    pthread_mutex_unlock (&monitor);


}
void *Programer(int vrsta){
    Udi(vrsta);
    Izadi(vrsta);

}
int main()
{
    pthread_mutex_init(&monitor, NULL);

    pthread_cond_init(uvjet, NULL);

    pthread_t thread_ids[programeri];

    srand(time(NULL));

    for(int i=0 ; i<programeri ; i++){
        int oznaka=rand()%2;
        pthread_create(&thread_ids[i], NULL, Programer, oznaka);
	sleep((rand()%4)+1); 
    }

    
    for(int i=0 ; i<programeri ; i++)
        pthread_join(thread_ids[i], NULL);


    return 0;
}