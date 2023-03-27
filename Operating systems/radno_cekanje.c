#include<stdio.h>
#include<signal.h>
#include<sys/types.h>
#include<sys/ipc.h>
#include<sys/shm.h>
#include<values.h>
#include<sys/msg.h>
#include<sys/sem.h>
#include<pthread.h>
#include<stdlib.h>
#include<time.h>
#include<unistd.h>
#include<wait.h>

int Id; //ident broj segmenta
int ZajednickaVar; //medudretvena komunikacija
int *ZajednickaMem; //komunikacija medu procesima

void obrisiMem(int sig) 
{
 (void) shmdt ((char *) ZajednickaMem); 
 (void) shmctl(Id, IPC_RMID, NULL); 
 exit(0);
}
 
void *NovaDretva(void *x){
    printf("Pokrenuta ULAZNA DRETVA\n"); 
    int i=0;
    
    while(i < *((int*)x)){
      if(ZajednickaVar==0){
      sleep(3);
      ZajednickaVar = (rand() % (100 - 1 + 1)) + 1;      
      printf("ULAZNA DRETVA: broj %d\n", ZajednickaVar);
      i++;
      }
    }
}

int main(int argc, char *argv[]) 
{
	int brojac = atoi(argv[1]);
	srand(time(NULL));
	
	if(brojac < 1) {
	printf("Neispravan argument\n");
	exit(1);
        }
        int brojacZaRadnu = brojac;
        int brojacZaIzlaznu = brojac;
	pthread_t thr_id;


	Id = shmget(IPC_PRIVATE, sizeof(int), 0600); //zauzimanje memorije

	if (Id == -1) 
        exit(1);
   
	ZajednickaMem = (int *) shmat(Id, NULL, 0); 

	struct sigaction act; 

	act.sa_handler = obrisiMem;
	sigemptyset(&act.sa_mask);
	act.sa_flags = 0;
	sigaction(SIGINT, &act, NULL);

	if(fork() == 0) { //proces dijete ce imat dretve radnu i ulaznu 

        if(pthread_create(&thr_id, NULL, NovaDretva, &brojac) != 0) {  //ulazna
        printf("Greska pri stvaranju dretve!\n"); 
        exit(1); 
        }
        
        printf("Pokrenuta RADNA DRETVA\n"); 
        
        int j = 0;
                                                            //radna
        while(j < brojacZaRadnu){
      		if(ZajednickaVar!=0 && *ZajednickaMem == 0){
      		int citajBroj = ZajednickaVar;
      		*ZajednickaMem = citajBroj + 1;    
      		printf("RADNA DRETVA: procitan broj %d i povecan na %d\n",citajBroj, *ZajednickaMem);
      		j++;
      		while(*ZajednickaMem != 0) {}
      		ZajednickaVar = 0;
      		}
    	}
       pthread_join(thr_id, NULL);
       exit(0);
       
       } 
       else { //proces roditelj izvrsava izlaznu dretvu
     
       printf("Pokrenut IZLAZNI PROCES\n"); 
 
       int k=0;
       int procitajBroj; 
       FILE *ispis;
       ispis = fopen("ispis.txt", "w+");
       while(k < brojacZaIzlaznu){
          if(*ZajednickaMem != 0) {
      	 	 procitajBroj = *ZajednickaMem; 
     	 	 fprintf(ispis, "%d\n",procitajBroj);
      	 	 printf("IZLAZNI PROCES: broj upisan u datoteku %d\n", procitajBroj);
      	         k++;
      	         *ZajednickaMem = 0;
      	  }
       }
       fclose(ispis);
       
       }
       
       wait(NULL);
       
       sleep(1);
       printf("Zavrsila ULAZNA DRETVA\n"); 
       printf("Zavrsila RADNA DRETVA\n");
       printf("Završio IZLAZNI PROCES\n");
       obrisiMem(0);
 
   return 0;
}
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   

