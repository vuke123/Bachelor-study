#include <stdio.h>
#include <signal.h>
#include <stdlib.h>
#include <pthread.h>
#include <sys/types.h>
#include <unistd.h>
#include <wait.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <semaphore.h>

#define BROJ_SEMAFORA 4
#define BROJ_DOLAZAKA 16
#define N 4

// semafor[0] --> signal da je slobodno mjesto u vrtuljku
// semafor[1] --> signal da je posjetitelj sjeo
// semafor[2] --> signal da posjetitelj smije izaći iz vrtuljka
// semafor[3] --> signal da je posjetitelj izasao iz vrtuljka

int Id;
sem_t *semafor[BROJ_SEMAFORA];

void posjetitelj(void)
{
    sem_wait(semafor[0]);
    printf("Dobrodošli, sjednite!\n");
    sem_post(semafor[1]);
    printf("Evo sjeo sam i čekam vožnju.\n");
    sem_wait(semafor[2]);
    printf("Vožnja je gotova, molim Vas izađite.\n");
    sem_post(semafor[3]);
    printf("Izlazim, vožnja je bila super!\n");
    exit(0);
}

void vrtuljak(void)
{
    while (1)
    {
        for (int i = 0; i < N; i++)
        {
            sem_post(semafor[0]);
        }
        for (int i = 0; i < N; i++)
        {
            sem_wait(semafor[1]);
        }
        printf("Vrtuljak pokrenut\n");
        sleep(5);
        printf("Vrtuljak zaustavljen\n");
        for (int i = 0; i < N; i++)
        {
            sem_post(semafor[2]);
        }
        for (int i = 0; i < N; i++)
        {
            sem_wait(semafor[3]);
        }
    }
}

int main()
{
    for(int i=0; i < BROJ_SEMAFORA; i++){
      int ID = shmget(IPC_PRIVATE, sizeof(sem_t), 0600); 
      semafor[i] = shmat(ID, NULL, 0);  
      shmctl(ID, IPC_RMID, NULL);
      sem_init(semafor[i], 1, 0); 
    }

    for (int i = 0; i < BROJ_DOLAZAKA; i++)
    {
        switch (fork())
        {
        case -1:
            printf("Greska\n");
            exit(1);
        case 0:
            posjetitelj();

        default:
            break;
        }
    }
     
    sleep(1);
    vrtuljak();#in
    sleep(1);
 
    for(int i=0; i<BROJ_SEMAFORA; i++){
        sem_destroy(semafor[i]);
    }
    shmdt(*semafor);
    return 0;

}



