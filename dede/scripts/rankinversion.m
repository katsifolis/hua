function [N]=rankinversion(T)  %Ti priority of Alternative i, i.e. ScenarioValue_i
                               % T1<T2<T3
  
  [n]=length(T);
  
  for i=1:n-1
    if T(i)>T(i+1) || T(i)==T(i+1)  
      N=1;
    else
      N=0;
    end %eof if
  
  
end %eof i


  
endfunction
