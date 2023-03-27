clear;
addpath(genpath('C:\Users\Luka\Desktop\FER\OBRADAINFO\treci lab\HMM\HMMall')); % Dodaj put na biblioteku funkcija
% Imamo tri pristrane kocke od kojih uvijek bacamo jednu odabranu
prior0=[
 1 % Prva kocka 
 2 % Druga kocka 
 3 % Treca kocka
]/6;
% Broj stanja HMM modela
Q=size(prior0,1);
% ---------------------------------------------------------------
M=5;
% Matrica vjerojatnosti promjena stanja
transmat0=[
M-1 1 0 % P(1|1) P(2|1) P(3|1)
0 M-1 1 % P(1|2) P(2|2) P(3|2)
1 0 M-1 % P(1|3) P(2|3) P(3|3)
]/M;
% Matrica vjerojatnosti osmatranja izlaznih simbola
obsmat0 = [20 5 6 3 4 2
           4 1 20 3 6 6
           5 6 2 5 20 2]/40;          

sample1 = [3 5 4 3 3 1 3 5 3 6 1 4 5 5 2 1 4 5 4 5 6 5 2 3 2 5 5 2 1 1 1 1 3 5 4 4 1 1 1 1 2]; %prvi uzorak
sample2 = [5 3 1 4 4 2 6 5 6 2 5 3 4 4 2 3 5 2 3 2 3 5 6 2 6 4 4 4 2 4 4 4 4 6 6 6 4 4 2 5 2]; %drugi uzorak
ll1 = dhmm_logprob(sample1, prior0, transmat0, obsmat0); %izračunavanje log-izvjesnosti 
ll2 = dhmm_logprob(sample2, prior0, transmat0, obsmat0);

llDiff = exp(ll1)/exp((ll2)); %razlika u izvjesnosti u eksponencijalnom zapisu

obslik0 = multinomial_prob(sample1, obsmat0); %funkcija uzima iz obsmat polja vrijednosti ovisno koji indeks tj. stupac
%nam je zadan u 1D polju sample1 

[alpha, beta, gamma, ll] = ...           %funkcija za izračunavanje više parametara skrivenog markovljevog modela
 fwdback(prior0, transmat0, obslik0, 'scaled', 0); %ne dopuštamo skaliranje
 
fwdvalue15 = (alpha(1,15));   %unaprijedna vrijednost u trenutku 15 za dolazak u prvo stanje tj. na prvu kocku
bwdvalue23 = (beta(1,23));    %unazadna vrijednost za trenutak 1 

vpath = viterbi_path(prior0, transmat0, obslik0); %najizvjesniji put

firstThree = vpath(1:3);
vpathR = flip(vpath);
lastThree = flip(vpathR(1:3));

obslik2 = multinomial_prob(sample2, obsmat0); %izracunavanje vrijednosti osmatranja odabranog niza
vpath2 = viterbi_path(prior0, transmat0, obslik2); %najizvjesniji put za drugi niz

% vjerojatnost uzduz najizvjesnijeg puta, slicna funkcija kao za sve puteve
% samo jos dodajemo određen viterbi put kao parametar
[ll1V, p1] = dhmm_logprob_path(prior0, transmat0, obslik0, vpath);
[ll2V, p2] = dhmm_logprob_path(prior0, transmat0, obslik2, vpath2);

diff1 = ll1 - ll1V; %razlika log izvjesnosti za sve puteve i log izvjesnosti preko određenog viterbi puta
diff2 = ll2 - ll2V;

%izracunavanje skracenog niza, ali putem alphe tako da ćemo sumirat cijeli
%četvrti stupac i tako saznat ukupnu izvjesnost

lR = sum(alpha(:,4)); % l - likelihood (izvjesnost) za R - reducirani niz

obslikR = multinomial_prob(sample1(1:4), obsmat0); %izracunavamo obslik polje za reducirani niz, potreban nam je za 
%izracun viterbi puta

vpathR = viterbi_path(prior0, transmat0, obslikR);
[llRV, p3] = dhmm_logprob_path(prior0, transmat0, obslikR, vpathR); %izracun izvjesnosti osmatranja uzduz Viterbi puta

likelihoodStake = exp(llRV)/lR;   %udio izvjesnosti 

firstFour = vpathR(1:4);  %izracun prva četiri stanja Viterbi puta reduciranog niza

%ukupno imamo 3 kocke i trazimo broj svih mogucih puteva za niz od 4
%izlazna simbola 
numPaths = 3^4; 
v=[1 2 3];
%treba nam funkcija koja ce nam naci sve varijacije s ponavljanjem za polje
%"v"
llm=zeros(numPaths,1); % Stupac za log-izvjesnosti
mpath = [];
for i = 1:3                   %dodavanje svih varijacija u polje mpath
    for j = 1:3
        for k = 1:3 
            for l = 1:3
              mpath = [mpath; [i j k l]];
            end
        end
    end
end
%broj kombinacija za 4 znaka
num_of_combinations = length(mpath);

%sve permutacije izvjesnost pojavljivanja za prva 4 simbola
ll_R=zeros(81,1);
for i=1:81,
 [ll_R(i), p] = dhmm_logprob_path(prior0, transmat0, ...
     obslikR, mpath(i,:));
end;

%nadi sve nemoguce pojave
num_of_false_combinatons = 0;
for i=1:81,
    if ll_R(i) == -inf
        num_of_false_combinatons = num_of_false_combinatons + 1; 
    end;
end;

%sortiraj po izvjesnosti
[sorted_ll_R,illm]=sort(-ll_R);

%vjerojatnost prvih pet najizvjesnijih pojavljivanja
l5 = sum(exp(-sorted_ll_R(1:5)));

%Omjer vjerojatnosti svih pojavljivanja sa prvih 5 pojavlivanja
 omjer = l5 / lR;

% generiraj visestruki opservacijski niz:
T = 100; % duljina svakog niza
nex = 14; % broj opservacijskih nizova
rng('default'); %resetiranje generatora slucajnih brojeva
data = dhmm_sample(prior0, transmat0, obsmat0, nex, T); %poziv funkcije

hm=hist(data(1,:), [1 2 3 4 5 6]); %funkcija koja broji broj izlaznih simbola

pi_stac=transmat0;
for i=1:T
    pi_stac=pi_stac*transmat0;
end
%dobili smo matricu koja iskazuje da je vjerojatnost svakog stanja 1/3

stac = pi_stac(1,:)*obsmat0*6; %množenjem stacionarne distribucije stanja sa 
%vjerovatnostima obzervacija i veličinom uzorka koji promatramo dobivamo
%stacionirane vjerojatnosti izlaznih simbola u nekom uzorku opisanom našim modelom

%izracunavamo empirijske dugotrajne vjerojatnosti koje cemo usporedivat s 
%prethodno dobivenim teorijskima
hmEmp=hist(data',[1 2 3 4 5 6]);
empStac = mean(hmEmp')/T;
%trazenje maksimalne razlike
teorStac = stac/6; %izracun teorijskih vjerojatnosti

maxDiff = 0;
for i=1:6
    if abs(teorStac(i) - empStac(i)) > maxDiff
        maxDiff = abs(teorStac(i) - empStac(i));
    end
end

% izracun log-izvjesnosti svakog niza u polju "data"
llm2=zeros(nex,1); % Stupac log-izvjesnosti
for i=1:nex
 llm2(i)=dhmm_logprob(data(i,:), prior0, transmat0, obsmat0);
end

maxll = max(llm2);
minll = min(llm2);
avgll = mean(llm2); 

Q = 3;
O = 6;

rng('default'); %resetiranje generatora slucajnih brojeva
%randomizirane vrijednosti za navedene matrice
prior1 = normalise(rand(Q,1));
transmat1 = mk_stochastic(rand(Q,Q));
obsmat1 = mk_stochastic(rand(Q,O));
% treniranje modela
[LL2, prior2, transmat2, obsmat2] = dhmm_em(data, prior1, transmat1, obsmat1, 'max_iter', 200, 'thresh', 1E-6);

[LL3, prior3, transmat3, obsmat3] = dhmm_em(data, prior0, transmat0, obsmat0, 'max_iter', 200, 'thresh', 1E-6);

%racunanje log-izvjesnosti osmatranja niza "data" za razlicite modele
llf1 = dhmm_logprob(data, prior0, transmat0, obsmat0); %model zadan u zadataku
llf2 = dhmm_logprob(data, prior1, transmat1, obsmat1); %model za "los" slucaj
llf3 = dhmm_logprob(data, prior2, transmat2, obsmat2); %model nakon prvog treniranja
llf4 = dhmm_logprob(data, prior3, transmat3, obsmat3); %model nakon drugog treniranja