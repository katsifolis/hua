load hoho.f;

s=0.2; %perturbations +-10%;
ntimes=10^4;

NPRR=zeros(ntimes,1); %initialization of the matrix of RR for each iteration

%initialization of the new weights.We initialize the weights with old ones
wn=w; %initialization of weights criteria
wf1n=wf1; %initialization of factor weights under C1
wf2n=wf2;%initialization of factor weights under C2
wf3n=wf3;%initialization of factor weights under C3
RAfn=RAf;%initialization of alternatives relative importance for each factor

ScenarioValue_ntimes=zeros(ntimes,Nalter); %initialization of alternatives priorities for each iteration


%MC simulation for ntimes iterations

for iter=1:ntimes
  
   
  %PWC matrix pertutbation 
  for m=1:M
    wn(:,m)=pertub_matrix(Pc(:,:,m),s); %perturbed matrix of criteria
    wf1n(:,m)=pertub_matrix(Pfc1(:,:,m),s); %perturbed matrix of criteria
    wf2n(:,m)=pertub_matrix(Pfc2(:,:,m),s); %perturbed matrix of criteria
    wf3n(:,m)=pertub_matrix(Pfc3(:,:,m),s); %perturbed matrix of criteria
    
    for i=1:Nfactors
      RAfn(:,i,m)=pertub_matrix(PAf(:,:,i,m),s); %perturbed matrix of criteria
      
    end %eofi
      
    
  end %eof m
  
  %Estimate average weights and relative scores for the M experts
  Wn=mean(wn,2);
  F1n=mean(wf1n,2);
  F2n=mean(wf2n,2);
  F3n=mean(wf3n,2);
  Rn=mean(RAfn,3);
  Fn=[F1n;F2n;F3n];
  

  %Estimation of Alternatives Priorities
  
  for i=1:Nalter %alternatives
  j=0;
  Nfcur=0;
  
    for k=1:N %criteria
      Nfcur=Nfcur+Nf(k); %Nfcur shows the maximum j for each k
    
      for j=j+1:Nfcur %Factors
        ScenarioValue_ntimes(iter,i)=ScenarioValue_ntimes(iter,i)+Wn(k)*Fn(j)*Rn(i,j);
      end %eof j
    
    
    end %eof k
  
  
  
  
  end %eof i

  
  NPRR(iter)=rankinversion(ScenarioValue_ntimes(iter,:)); %RR of alternatives priorities for each iteation
 
 
end %eof ntimes (MC)

PRR=sum(NPRR)/ntimes;

