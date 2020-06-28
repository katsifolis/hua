function P=pairwise_matrix(S,n)
  
  P=zeros(n,n);
  
  for i=1:n
    for j=1:n
      if (i==j)
        P(i,i)=1; % fill in the diag
      elseif j>i  % fill in the upper triangular array
        P(i,j)=S(ceil(length(S).*rand(1,1)));
      end %eof if
      
     end % eof for j
   end %eof for i
        
   %fill in the lower triangular array
   for k=2:n
     for m=1:(k-1)
       P(k,m)=1/P(m,k); %otherwise P(k,m)=inv(P(m,k));       
     end %eof k
   end %eof m
   
        
 
  
endfunction
