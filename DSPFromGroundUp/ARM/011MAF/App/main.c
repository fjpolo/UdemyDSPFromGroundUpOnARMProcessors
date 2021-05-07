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
volatile float32_t inputSample, outputSample;
/*fc = 6kHz*/
//const float32_t firCoeffs32[NUM_TAPS] = {
//  -0.0018225230f, -0.0015879294f, +0.0000000000f, +0.0036977508f, +0.0080754303f, +0.0085302217f, -0.0000000000f, -0.0173976984f,
//  -0.0341458607f, -0.0333591565f, +0.0000000000f, +0.0676308395f, +0.1522061835f, +0.2229246956f, +0.2504960933f, +0.2229246956f,
//  +0.1522061835f, +0.0676308395f, +0.0000000000f, -0.0333591565f, -0.0341458607f, -0.0173976984f, -0.0000000000f, +0.0085302217f,
//  +0.0080754303f, +0.0036977508f, +0.0000000000f, -0.0015879294f, -0.0018225230f
//};
//static float32_t FIRState_f32[BLOCK_SIZE + NUM_TAPS - 1];
float32_t OutputSignal_f32[SIGNAL_SIZE];
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
* \fn filterMAF
*
* \brief 
*/
void filterMAF(float32_t* inputArr, float32_t* outputArr, uint32_t signalLen, uint32_t filterPts){
	uint32_t i, j;
	for(i=floor(filterPts/2);i<((signalLen - (filterPts/2))-1); ++i ){
		outputArr[i] = 0;
		for(j=-floor(filterPts/2);j<floor(filterPts/2);++j){
			outputArr[i] +=  inputArr[i+j];
		}
		outputArr[i] /= filterPts;
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
	
	/*MAF*/
//	filterMAF(inputSignal_f32_1kHz_15kHz, OutputSignal_f32, SIGNAL_SIZE, 8);
	filterMAF(inputSignal_f32_1kHz_15kHz, OutputSignal_f32, SIGNAL_SIZE, 16);
//	filterMAF(inputSignal_f32_1kHz_15kHz, OutputSignal_f32, SIGNAL_SIZE, 32);
//	filterMAF(inputSignal_f32_1kHz_15kHz, OutputSignal_f32, SIGNAL_SIZE, 64);

	
	/*Superloop*/
	while(true){
		/*Input signal*/
//		PlotInputSignal(inputSignal_f32_1kHz_15kHz, SIGNAL_SIZE);
//		PlotOutputSignal(OutputSignal_f32, SIGNAL_SIZE);
		PlotInputOutputSignal(inputSignal_f32_1kHz_15kHz, OutputSignal_f32, SIGNAL_SIZE);
		
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



