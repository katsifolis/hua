function [wnew,CR]=pertub_matrix(P,s)
  
  [nx,ny]=size(P);
  DP=zeros(nx,ny); %perturbation ?P

  Pnew=ones(nx,ny);
  
  for i=1:nx
    for j=i+1:ny %upper triangular array
      DP(i,j)=s*(rand-0.5); %?P inside [-s/2 s/2]
      P(i,j)=P(i,j)*DP(i,j)+P(i,j); %Perturb the Pij elements
      Pnew(i,j)=closeToValues(P(i,j));%Pij perturbed fit to the closer integer or reciprocal of the nine level scale
    end 
    
    for j=1:ny-1%lower triangular array
      Pnew(i,j)=1/Pnew(j,i);  
    end      
    
  end %of i
  
  [wnew,CR]=eigenmethod(Pnew);
  
  
endfunction
