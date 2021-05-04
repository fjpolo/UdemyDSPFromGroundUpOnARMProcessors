#include <stdint.h>
#include <stdbool.h>
#include "arm_math.h"                   // ARM::CMSIS:DSP
#include "stm32f4xx_hal.h"              // Keil::Device:STM32Cube HAL:Common
#include "cmsis_os.h"                   // ARM::CMSIS:RTOS:Keil RTX
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
osThreadId sineId, noiseId, disturbedId, filteredId, syncId;

/**
* \brief sineThread
*/
uint32_t t;
void sineThread(void const *argument){
	while(true){
		osSignalWait(0x00001, osWaitForever);
		osDelay(t);
		sine = sine_calc_sample_q15(&Signal_set) / 2;
	}
}

/**
* \brief noiseThread
*/
void noiseThread(void const *argument){
	while(true){
		osSignalWait(0x00001, osWaitForever);
		osDelay(t);
		noise = sine_calc_sample_q15(&Noise_set) / 6;
	}
}

/**
* \brief disturbedThread
*/
void disturbedThread(void const *argument){
	while(true){
		osSignalWait(0x00001, osWaitForever);
		osDelay(t);
		disturbed = noise + sine;
	}
}

/**
* \brief filteredThread
*/
void filteredThread(void const *argument){
	while(true){
		osSignalWait(0x00001, osWaitForever);
		osDelay(t);
		filtered  = low_pass_filter(&disturbed);
	}
}

/**
* \brief syncThread
*/
void syncThread(void const *argument){
	while(true){
		osDelay(t);
		osSignalWait(0x00001, osWaitForever);
		osSignalSet(sineId, 0x00001);
		
	}
}


/**
* \brief Threads
*/
osThreadDef(sineThread, osPriorityNormal, 1, 0);
osThreadDef(noiseThread, osPriorityNormal, 1, 0);
osThreadDef(disturbedThread, osPriorityNormal, 1, 0);
osThreadDef(filteredThread, osPriorityNormal, 1, 0);
osThreadDef(syncThread, osPriorityNormal, 1, 0);

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
	
	/*OS*/
	sineId = osThreadCreate(osThread(sineThread), NULL);
	noiseId = osThreadCreate(osThread(noiseThread), NULL);
	disturbedId = osThreadCreate(osThread(disturbedThread), NULL);
	filteredId = osThreadCreate(osThread(filteredThread), NULL);
	syncId = osThreadCreate(osThread(syncThread), NULL);

	/*Superloop*/
	while(true){
		/*DSP*/
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

