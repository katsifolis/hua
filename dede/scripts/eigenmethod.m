function [W,CR]=eigenmethod(P)
  
  [V,lamda]=eig(P);
  [nx,ny]=size(lamda);
  
  L=zeros(nx,1);
  
  for i=1:nx
    if imag(lamda(i,i))==0
      L(i)=lamda(i,i);
    end
  end
  
  [Lmax,ind]=max(L);
  
  W=abs(V(:,ind)/sum(V(:,ind)));
  
  n=nx;
  
  CI=(Lmax-n)/(n-1);
  
  N=[3 4 5 6 7 8 9 10];
  RI=[0.52 0.89 1.11 1.25 1.25 1.4 1.45 1.49];
  
  for i=1:length(N)
    if n==N(i)
      CR=CI/RI(i);
    elseif n==1 || n==2
      CR=0;
    end
    
  end %eof for
  
endfunction
