#include <stdio.h>

int main(int argc, char *argv[])
{
	FILE *fp_in, *fp_out;
	int input;
	int count=0;
	double data[200][2];// the number of data is 200
	int label[200];
	int i=0;
	
	
	//Input//
	fp_in = fopen(argv[1],"r");
	if(fp_in==NULL){
		printf("fail: cannot open the input-file. Change the name of input-file. \n");
		return -1;
	}
	
	while( (input=fscanf(fp_in, "%lf,%lf", &data[count][0], &data[count][1])) != EOF){
		//printf("%lf %lf\n", data[count][0], data[count][1]);
		count++;
	}
	
	//k-means//
	//
	
	///////////
	
	//Output//
	fp_out = fopen(argv[2],"w");
	if(fp_out==NULL){
		printf("fail: cannot open the output-file. Change the name of output-file.  \n");
		return -1;
	}


	for(i=0;i<200;i++){
		fprintf(fp_out, "%lf,%lf,%d\n", data[i][0], data[i][1], label[i]);
	}
	return 0;
}
