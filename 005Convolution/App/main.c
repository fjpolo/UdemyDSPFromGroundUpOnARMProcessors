#include <stdint.h>
#include <stdbool.h>
#include "arm_math.h"                   // ARM::CMSIS:DSP
#include "stm32f4xx_hal.h"              // Keil::Device:STM32Cube HAL:Common
#include "clock.h"

/**
* \brief Constants
*/
#define SIGNAL_SIZE 		320
//#define SIGNAL_SIZE 		100
#define NUM_TAPS 				29
#define IMP_RESP_LEN		29
#define BLOCK_SIZE			32
/**
* \brief Imported variables
*/
extern float32_t inputSignal_f32_1kHz_15kHz[SIGNAL_SIZE];



/**
* \brief Global variables
*/
const uint32_t numBlocks = SIGNAL_SIZE/BLOCK_SIZE;
uint32_t freq = 0;
volatile uint32_t counter = 0;
volatile float32_t inputSample, impulseSample, outputSample;

float32_t impulseResponse[IMP_RESP_LEN] = {
  -0.0018225230f, -0.0015879294f, +0.0000000000f, +0.0036977508f, +0.0080754303f, +0.0085302217f, -0.0000000000f, -0.0173976984f,
  -0.0341458607f, -0.0333591565f, +0.0000000000f, +0.0676308395f, +0.1522061835f, +0.2229246956f, +0.2504960933f, +0.2229246956f,
  +0.1522061835f, +0.0676308395f, +0.0000000000f, -0.0333591565f, -0.0341458607f, -0.0173976984f, -0.0000000000f, +0.0085302217f,
  +0.0080754303f, +0.0036977508f, +0.0000000000f, -0.0015879294f, -0.0018225230f
};
float32_t OutputSignal_f32[IMP_RESP_LEN + SIGNAL_SIZE];
float32_t inputMean = 0;
float32_t inputVariance = 0;
float32_t inputSTD = 0;

/**
* \fn PlotInputSignal
*
* \brief 
*/
void PlotInputSignal(float32_t* Signal, uint32_t size){
	/*Counter vars*/
	uint32_t i,j;
	/*Sample loop*/
	for(i=0;i<size;++i){
		/*Sample*/
		inputSample = Signal[i];
		/*Pseudodelay*/
		for(j=0;j<3000;++j){
			i %= size;
		}
	}
}
	
/**
* \fn PlotOutputSignal
*
* \brief 
*/
void PlotOutputSignal(float32_t* Signal, uint32_t size){
	/*Counter vars*/
	uint32_t i,j;
	/*Sample loop*/
	for(i=0;i<size;++i){
		/*Sample*/
		outputSample = Signal[i];
		/*Pseudodelay*/
		for(j=0;j<3000;++j){
			i %= size;
		}
	}
}

/**
* \fn PlotInputOutputSignal
*
* \brief 
*/
void PlotInputOutputSignal(float32_t* InputSignal, float32_t* OutputSignal, uint32_t size){
	/*Counter vars*/
	uint32_t i,j;
	/*Sample loop*/
	for(i=0;i<size;++i){
		/*Sample*/
		inputSample = InputSignal[i];
		outputSample = OutputSignal[i];
		/*Pseudodelay*/
		for(j=0;j<10000;++j){
			i %= size;
		}
	}
}

/**
* \fn PlotInpulseResponse
*
* \brief 
*/
void PlotInpulseResponse(float32_t* Signal, uint32_t size){
	/*Counter vars*/
	uint32_t i,j;
	/*Sample loop*/
	for(i=0;i<size;++i){
		/*Sample*/
		impulseSample = Signal[i];
		/*Pseudodelay*/
		for(j=0;j<3000;++j){
			i %= size;
		}
	}
}


/**
* \fn PlotAll
*
* \brief 
*/
void PlotAll(
							float32_t* InputSignal, 
							float32_t* OutputSignal, 
							float32_t* impulseSignal, 
							uint32_t inputSize, 
							uint32_t impulseSize
						){
	/*Counter vars*/
	uint32_t i,j,k,l;
	/*Sample loop*/
	for(k=0;k<(inputSize+impulseSize);++k){
		
		i++;
		i %= inputSize;
		j++;
		j %= impulseSize;
		k %= (inputSize+impulseSize-1);
		/*Sample*/
		inputSample = InputSignal[i];
		outputSample = OutputSignal[k];
		impulseSample = impulseSignal[j];
		
		/*Pseudodelay*/
		for(l=0;l<10000;++l){}
	}
}

/**
* \fn signalMean
*
* \brief 
*/
float32_t signalMean_baddie(float32_t* sign_src_arr, uint32_t sig_len){
	float32_t mean = 0.0f;
	uint32_t it;
	/*Loop*/
	for(it=0;it<sig_len;++it){
		mean += sign_src_arr[it];
	}
	mean /= (float32_t)sig_len;
	return mean;
}

/**
* \fn signalVariance
*
* \brief 
*/
float32_t signalVariance_baddie(float32_t* sign_src_arr, float32_t sig_mean, uint32_t sig_len){
	float32_t variance = 0.0f;
	uint32_t it;
	/*Loop*/
	for(it=0;it<sig_len;++it){
		variance += powf((sign_src_arr[it] - sig_mean), 2);
	}
	variance /= (sig_len - 1);
	return variance;
}

/**
* \fn signalSTD
*
* \brief 
*/
float32_t signalSTD_baddie(float32_t sig_var){
	float32_t std = sqrtf(sig_var);
	return std;
}



/**
* \fn convolveSignal
*
* \brief 
*/
void convolveSignal(float32_t* inputArr, float32_t* outputArr, float32_t* impulseArr, uint32_t inputLen, uint32_t impulseLen){
	uint32_t i,j;
	/*Init outputArr*/
	for(i=0;i<(inputLen+impulseLen);++i){
		outputArr[i] = 0;
	}
	/*Convolve!!!*/
	for(i=0;i<inputLen;++i){
		for(j=0;j<impulseLen;++j){
			outputArr[i+j] += inputArr[i]*impulseArr[i];
		}
	}
}


/**
* \fn main
*
* \brief 
*/
int main(void){
	/*Init HAL*/
	HAL_Init();
	/*Configure clock at 100MHz*/
	SystemClock_Config();
	/*Read frequency*/
	freq = HAL_RCC_GetHCLKFreq();
	
	/*Convolve*/
//	convolveSignal(
//									(float32_t *)inputSignal_f32_1kHz_15kHz,
//									(float32_t *)OutputSignal_f32,
//									(float32_t *)impulseResponse,
//									SIGNAL_SIZE,
//									IMP_RESP_LEN
//								);
	arm_conv_f32(
								&inputSignal_f32_1kHz_15kHz[0],
								SIGNAL_SIZE,
								&impulseResponse[0],
								IMP_RESP_LEN,
								&OutputSignal_f32[0]
							);
	
	
	
	/*Superloop*/
	while(true){
		/*Input signal*/
//		PlotInputSignal(inputSignal_f32_1kHz_15kHz, SIGNAL_SIZE);
//		PlotOutputSignal(OutputSignal_f32, SIGNAL_SIZE);
//		PlotInputOutputSignal(inputSignal_f32_1kHz_15kHz, OutputSignal_f32, SIGNAL_SIZE);
//		PlotInpulseResponse(impulseResponse, IMP_RESP_LEN);
		PlotAll(inputSignal_f32_1kHz_15kHz, OutputSignal_f32, impulseResponse, SIGNAL_SIZE, IMP_RESP_LEN);
		
	}
}



/**
* \fn SysTick_Handler
*
* \brief 
*/
void SysTick_Handler(){
	HAL_IncTick();
	HAL_SYSTICK_IRQHandler();
}



