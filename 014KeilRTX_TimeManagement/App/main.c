#include <stdint.h>
#include <stdbool.h>
#include "arm_math.h"                   // ARM::CMSIS:DSP
#include "stm32f4xx_hal.h"              // Keil::Device:STM32Cube HAL:Common
#include "cmsis_os.h"                   // ARM::CMSIS:RTOS:Keil RTX
#include "clock.h"
#include "sine_generator.h"
#include "lowpassFilter.h"
#include "leds.h"

/**
* \brief Constants
*/


/**
* \brief Imported variables
*/
osThreadId Red_ThreadId, Green_ThreadId, Blue_ThreadId;
uint32_t counter1, counter2, counter3;

/**
* \brief Global variables
*/
uint32_t freq = 0;


/**
* \brief Red_Thread
*/
void Red_Thread(void const *argument){
	while(true){
		osDelay(125);
		counter1++;
		RED_toggle();
	}
}

/**
* \brief Green_Thread
*/
void Green_Thread(void const *argument){
	while(true){
		osDelay(250);
		counter2++;
		GREEN_toggle();
	}
}

/**
* \brief BlueThread
*/
void BlueThread(void const *argument){
	while(true){
		osDelay(500);
		counter3++;
		BLUE_toggle();
	}
}



/**
* \brief Threads
*/
osThreadDef(Red_Thread, osPriorityNormal, 1, 0);
osThreadDef(Green_Thread, osPriorityNormal, 1, 0);
osThreadDef(BlueThread, osPriorityNormal, 1, 0);


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
	LEDS_init();
	
	/**/
	counter1 = 0; 
	counter2 = 0; 
	counter3 = 0;
	
	/*OS*/
	Red_ThreadId = osThreadCreate(osThread(Red_Thread), NULL);
	Green_ThreadId = osThreadCreate(osThread(Green_Thread), NULL);
	Blue_ThreadId = osThreadCreate(osThread(BlueThread), NULL);


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

