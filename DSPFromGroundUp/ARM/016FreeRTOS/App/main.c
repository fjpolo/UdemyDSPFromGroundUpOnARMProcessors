#include <stdint.h>
#include <stdbool.h>
#include "arm_math.h"                   // ARM::CMSIS:DSP
#include "stm32f4xx_hal.h"              // Keil::Device:STM32Cube HAL:Common
#include "clock.h"
#include "sine_generator.h"
#include "lowpassFilter.h"
#include "leds.h"
#include "FreeRTOSConfig.h"             // ARM.FreeRTOS::RTOS:Config
#include "FreeRTOS.h"                   // ARM.FreeRTOS::RTOS:Core
#include "task.h"                       // ARM.FreeRTOS::RTOS:Core
#include "timers.h"                     // ARM.FreeRTOS::RTOS:Timers
#include "queue.h"                      // ARM.FreeRTOS::RTOS:Core
#include "semphr.h"                     // ARM.FreeRTOS::RTOS:Core



/**
* \brief Constants
*/


/**
* \brief Imported variables
*/

uint32_t counter1, counter2, counter3;

/**
* \brief Global variables
*/
uint32_t freq = 0;


/**
* \brief vRed_Thread
*/
void vRed_Thread(void *pvParameters){
	while(true){
		counter1++;
		RED_toggle();
		vTaskDelay(pdMS_TO_TICKS(500));
	}
}

/**
* \brief vGreen_Thread
*/
void vGreen_Thread(void *pvParameters){
	while(true){
		counter2++;
		GREEN_toggle();
		vTaskDelay(pdMS_TO_TICKS(125));
	}
}

/**
* \brief vBlue_Thread
*/
void vBlue_Thread(void *pvParameters){
	while(true){
		counter3++;
		BLUE_toggle();
		vTaskDelay(pdMS_TO_TICKS(250));
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
	/*INit LEDs*/
	LEDS_init();
	
	/*INit counters*/
	counter1 = 0; 
	counter2 = 0; 
	counter3 = 0;
	
	/*OS*/
	xTaskCreate(
								vRed_Thread,
								"Red Led Task",
								100,
								NULL,
								1,
								NULL							
							);
//	xTaskCreate(
//								vGreen_Thread,
//								"Green Led Task",
//								100,
//								NULL,
//								1,
//								NULL							
//							);
//	xTaskCreate(
//								vBlue_Thread,
//								"Blue Led Task",
//								100,
//								NULL,
//								1,
//								NULL							
//							);
							
	/*Init scheduler*/
	vTaskStartScheduler();

	/*Superloop - Unreachable*/
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

