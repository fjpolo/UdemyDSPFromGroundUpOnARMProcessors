#include <stdint.h>
#include <stdbool.h>
#include "arm_math.h"                   // ARM::CMSIS:DSP
#include "stm32f4xx_hal.h"              // Keil::Device:STM32Cube HAL:Common
#include "clock.h"
#include "sine_generator.h"
#include "lowpassFilter.h"

/**
* \brief Constants
*/
#define 	SAMPLING_FREQ		1000
#define		SIGNAL_FREQ			10
#define		NOISE_FREQ			50

/**
* \brief Imported variables
*/


/**
* \brief Global variables
*/
uint32_t freq = 0;
sine_generator_q15_t Signal_set;
sine_generator_q15_t Noise_set;
q15_t filtered,noise,disturbed,sine;

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
	
	/*Signals*/
	sine_generator_init_q15(&Signal_set, SIGNAL_FREQ, SAMPLING_FREQ);
	sine_generator_init_q15(&Noise_set, NOISE_FREQ, SAMPLING_FREQ);
	low_pass_filter_init(); 

	/*Superloop*/
	while(true){
		/*DSP*/
//		sine = sine_calc_sample_q15(&Signal_set);
//		noise = sine_calc_sample_q15(&Noise_set);		
		sine = sine_calc_sample_q15(&Signal_set) / 2;
		noise = sine_calc_sample_q15(&Noise_set) / 6;
		disturbed = noise + sine;
		filtered  = low_pass_filter(&disturbed);
    HAL_Delay(1);

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

