function [Pijnew]=closeToValues(Pij)
  
  values=[1/9 1/8 1/7 1/6 1/5 1/4 1/3 1/2 1 2 3 4 5 6 7 8 9];
  nv=length(values);
  
  for i=1:(nv-1)
    if Pij>values(i) && Pij<values(i+1)
      if abs(Pij-values(i))>abs(values(i+1)-Pij)
        Pijnew=values(i+1);
      elseif abs(Pij-values(i))<abs(values(i+1)-Pij)
        Pijnew=values(i);
      elseif abs(Pij-values(i))<abs(values(i+1)-Pij)
        Pijnew=values(i);
      endif
      
    elseif Pij==values(i)
      Pijnew=values(i);
    elseif Pij<=values(1)
      Pijnew=values(1);
    elseif Pij>=values(nv)
      Pijnew=values(nv);
      
      
    endif
    
    
    
  endfor
  
  
  
  
  
endfunction
