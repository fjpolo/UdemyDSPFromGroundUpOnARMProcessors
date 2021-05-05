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


/**
* \brief Imported variables
*/
osThreadId Thread1Id, Thread2Id, Thread3Id;
uint32_t counter1, counter2, counter3;

/**
* \brief Global variables
*/
uint32_t freq = 0;


/**
* \brief Thread1
*/
void Thread1(void const *argument){
	while(true){
		osDelay(1);
		counter1++;
	}
}

/**
* \brief Thread2
*/
void Thread2(void const *argument){
	while(true){
		osDelay(10);
		counter2++;
	}
}

/**
* \brief Thread3
*/
void Thread3(void const *argument){
	while(true){
		osDelay(100);
		counter3++;
	}
}



/**
* \brief Threads
*/
osThreadDef(Thread1, osPriorityNormal, 1, 0);
osThreadDef(Thread2, osPriorityNormal, 1, 0);
osThreadDef(Thread3, osPriorityNormal, 1, 0);


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
	
	/**/
	counter1 = 0; 
	counter2 = 0; 
	counter3 = 0;
	
	/*OS*/
	Thread1Id = osThreadCreate(osThread(Thread1), NULL);
	Thread2Id = osThreadCreate(osThread(Thread2), NULL);
	Thread3Id = osThreadCreate(osThread(Thread3), NULL);


	/*Superloop*/
	while(true){

	}
}



/**
* \fn SysTick_Handler
*
* \brief 
*/
//void SysTick_Handler(){
//	HAL_IncTick();
//	HAL_SYSTICK_IRQHandler();
//}

