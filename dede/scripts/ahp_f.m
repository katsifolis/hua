% Μέρος β 1 ερώτημα %

% Algorithms %
source('scripts/pairwise_matrix.m');
source('scripts/eigenmethod.m');

M=10; %number of experts
N=4; %number of criteria
Nalter=4; %number of alternatives
Nf=[2 3 4 5];% number of factors per criterion
Nfactors=sum(Nf, 2);
S=[1/9,1/8,1/7,1/6,1/5,1/4,1/3,1/2,1,2,3,4,5,6,7,8,9]; %nine level scale


Pc=ones(N,N,M); %initialize the PWC matrix of criteria
PAf=ones(Nalter,Nalter,Nfactors,M); %initialize PWC of alternatives relative importance for each factor

w=zeros(N,M);% initialize the matrix of criteria weights - wk (m)
RAf=zeros(Nalter,Nfactors,M); %initialize the matrix of alternatives relative importance for each factor - Rijk (m)

% Cell arrays for storing 
criteria_arr		 = cell(N, M);
factor_weights_arr	 = cell(N, M);


for m=1:M 
	Pc(:,:,m)=pairwise_matrix(S, N); 
	w(:,m)=eigenmethod(Pc(:,:,m));
end

% Dynamic Criteria and Weight allocation
for i=1:N
	criteria_arr(i) = {eval(['Pfc' num2str(i)      '=ones(Nf(i),Nf(i),M)'])}; 
	factor_weights_arr(i) = {eval(['wf' num2str(i) '=zeros(Nf(i),M)'])}; %matrix of factor weights
end


% PWC matrix generation
%Evaluation of weights and relative scores from PWCs
for i=1:N
	for m=1:M
		criteria_arr(i, m)=pairwise_matrix(S, Nf(i));
		factor_weights_arr(i, m)=eigenmethod(criteria_arr{i, m});

		if i < 2 
			Pc(:,:,m)=pairwise_matrix(S,N); 
			for j=1:Nfactors
				PAf(:,:,j,m)=pairwise_matrix(S,Nalter);
				RAf(:,j,m)=eigenmethod(PAf(:,:,j,m));
			end 
		end
	end
	Factors{i} = mean(factor_weights_arr{i}, 2)
end

% Constructing the weights of all factors
F = [];
for i=1:N
	tmp = Factors{i};
	F = [F;tmp];
end


W = mean(w, 2);
R = mean(RAf, 3);

% Estimate average values of weights and relative scores for the M experts
ScenarioValue=zeros(Nalter,1);

for i=1:Nalter %alternatives
	j=0;
	Nfcur=0;
	for k=1:N % criteria
		Nfcur=Nf(k); % Nfcur shows the maximum j for each k
			for j=j+1:Nfcur %Factors
				ScenarioValue(i)=ScenarioValue(i)+W(k)*F(j)*R(i,j);
			end 
	end
end

ScenarioValue
