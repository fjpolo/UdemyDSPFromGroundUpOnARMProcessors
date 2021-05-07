#include <stdint.h>
#include <stdbool.h>
#include "arm_math.h"                   // ARM::CMSIS:DSP
#include "stm32f4xx_hal.h"              // Keil::Device:STM32Cube HAL:Common
#include "clock.h"

/**
* \brief Constants
*/
#define SIGNAL_SIZE 		320
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
const float32_t firCoeffs32[NUM_TAPS] = {
  -0.0018225230f, -0.0015879294f, +0.0000000000f, +0.0036977508f, +0.0080754303f, +0.0085302217f, -0.0000000000f, -0.0173976984f,
  -0.0341458607f, -0.0333591565f, +0.0000000000f, +0.0676308395f, +0.1522061835f, +0.2229246956f, +0.2504960933f, +0.2229246956f,
  +0.1522061835f, +0.0676308395f, +0.0000000000f, -0.0333591565f, -0.0341458607f, -0.0173976984f, -0.0000000000f, +0.0085302217f,
  +0.0080754303f, +0.0036977508f, +0.0000000000f, -0.0015879294f, -0.0018225230f
};
static float32_t FIRState_f32[BLOCK_SIZE + NUM_TAPS - 1];
static float32_t OutputSignal_f32[SIGNAL_SIZE];


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
	/*FIR instantiation and declaration*/
	arm_fir_instance_f32 _1kHz_15kHz_sig;
	arm_fir_init_f32(
										&_1kHz_15kHz_sig,
										NUM_TAPS,
										(float32_t *)&firCoeffs32[0],
										&FIRState_f32[0],
										BLOCK_SIZE
									);
	/*Filter*/
	for(uint32_t i=0; i<numBlocks; ++i){
		/*Call FIR function*/
		arm_fir_f32(
									&_1kHz_15kHz_sig,
									&inputSignal_f32_1kHz_15kHz[0] + (i * BLOCK_SIZE),
									&OutputSignal_f32[0] + (i * BLOCK_SIZE),
									BLOCK_SIZE
							  );
	}
	
	
	/*Superloop*/
	while(true){
//		/*Counter*/
//		++counter;
//		counter %= 100;
//		/*Pseudodelay*/
//		for(int i=0;i<3000;++i){}
		
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