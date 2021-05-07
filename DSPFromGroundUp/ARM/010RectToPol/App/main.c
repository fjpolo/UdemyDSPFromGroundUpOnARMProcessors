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
#define ECG_SIZE 				640
#define NUM_TAPS 				29
#define IMP_RESP_LEN		29
#define BLOCK_SIZE			32
/**
* \brief Imported variables
*/
extern float32_t inputSignal_f32_1kHz_15kHz[SIGNAL_SIZE];
extern float32_t _640_points_ecg_[ECG_SIZE];


/**
* \brief Global variables
*/
const uint32_t numBlocks = SIGNAL_SIZE/BLOCK_SIZE;
uint32_t freq = 0;
volatile uint32_t counter = 0;
volatile float32_t inputSample, impulseSample, outputSample, ReXSample, ImXSample;

float32_t impulseResponse[IMP_RESP_LEN] = {
  -0.0018225230f, -0.0015879294f, +0.0000000000f, +0.0036977508f, +0.0080754303f, +0.0085302217f, -0.0000000000f, -0.0173976984f,
  -0.0341458607f, -0.0333591565f, +0.0000000000f, +0.0676308395f, +0.1522061835f, +0.2229246956f, +0.2504960933f, +0.2229246956f,
  +0.1522061835f, +0.0676308395f, +0.0000000000f, -0.0333591565f, -0.0341458607f, -0.0173976984f, -0.0000000000f, +0.0085302217f,
  +0.0080754303f, +0.0036977508f, +0.0000000000f, -0.0015879294f, -0.0018225230f
};
float32_t OutputSignal_f32[IMP_RESP_LEN + SIGNAL_SIZE];
float32_t ReX[SIGNAL_SIZE/2];
float32_t ImX[SIGNAL_SIZE/2];
float32_t ECGOutputSignal_f32[ECG_SIZE];
float32_t ECGReX[ECG_SIZE/2];
float32_t ECGImX[ECG_SIZE/2];
float32_t inputMean = 0;
float32_t inputVariance = 0;
float32_t inputSTD = 0;
float32_t signalMag[SIGNAL_SIZE/2];
float32_t signalPhase[SIGNAL_SIZE/2];

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
* \fn PlotReXSignal
*
* \brief 
*/
void PlotReXSignal(float32_t* Signal, uint32_t size){
	/*Counter vars*/
	uint32_t i,j;
	/*Sample loop*/
	for(i=0;i<size;++i){
		/*Sample*/
		ReXSample = Signal[i];
		/*Pseudodelay*/
		for(j=0;j<3000;++j){
			i %= size;
		}
	}
}

/**
* \fn PlotImXSignal
*
* \brief 
*/
void PlotImXSignal(float32_t* Signal, uint32_t size){
	/*Counter vars*/
	uint32_t i,j;
	/*Sample loop*/
	for(i=0;i<size;++i){
		/*Sample*/
		ImXSample = Signal[i];
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
* \fn RunningSum
*
* \brief 
*/
void RunningSum(float32_t* inputArr, float32_t* outputArr, uint32_t inputLen){
	uint32_t i;
	inputArr[0] = outputArr[0];
	for(i=0;i<inputLen;++i){
		outputArr[i] = outputArr[i-1] + inputArr[i];
	}
}

/**
* \fn FirstDifference
*
* \brief 
*/
void FirstDifference(float32_t* inputArr, float32_t* outputArr, uint32_t inputLen){
	uint32_t i;
	outputArr[0] = 0;
	for(i=0;i<inputLen;++i){
		outputArr[i] = inputArr[i] - inputArr[i-1];
	}
}



/**
* \fn DFT
*
* \brief 
*/
void DFT(
					float32_t* inputArr,
					float32_t* RexArr,
					float32_t* ImxArr,
					uint32_t inputLen
){
	uint32_t i,j,k;
	for(j=0;j<(inputLen/2);++j){
		RexArr[j] = 0;
		ImxArr[j] = 0;
	}
	/*Algorithm*/
	for(k=0;k<(inputLen/2);++k){
		for(i=0;i<inputLen;++i){
			RexArr[k] += inputArr[i] * cos(2*PI*k*i / inputLen);
			ImxArr[k] -= inputArr[i] * sin(2*PI*k*i / inputLen);
		}
	}
}

/**
* \fn IDFT
*
* \brief 
*/
void IDFT(
					float32_t* outputArr,
					float32_t* RexArr,
					float32_t* ImxArr,
					uint32_t outputLen
){
	uint32_t i, j, k;
	/*Init out arr*/
	for(i=0;i<outputLen;++i){
		outputArr[i] = 0;
	}
	/*Algorithm*/
	for(k=0;k<(outputLen/2);++k){
		RexArr[k] = RexArr[k]/(outputLen/2);
		ImxArr[k] = -ImxArr[k]/(outputLen/2);
	}
	RexArr[0] = RexArr[0]/(outputLen);
	ImxArr[0] = -ImxArr[0]/(outputLen);
	for(k=0;k<(outputLen/2);++k){
		for(i=0;i<outputLen;++i){
			outputArr[i] += RexArr[k] * cos(2*PI*k*i / outputLen);
			outputArr[i] += ImxArr[k] * sin(2*PI*k*i / outputLen);
		}
	}
}

/**
* \fn DFToutputMagnitude
*
* \brief 
*/
void DFToutputMagnitude(float32_t* RexArr, uint32_t inputLen){
	uint32_t k;
	for(k=0;k<inputLen;++k){
			RexArr[k] = fabs(RexArr[k]);
	}
}

/**
* \fn RectToPol
*
* \brief 
*/
void RectToPol(
	float32_t* RexArr,
	float32_t* ImXArr,
	float32_t* outputMagnitudeArr,
	float32_t* outputPhaseArr,
	uint32_t signalLen
){
	uint32_t k;
	for(k=0;k<signalLen;++k){
		outputMagnitudeArr[k] = sqrt( powf(RexArr[k], 2) + powf(ImXArr[k], 2) );
		if(outputMagnitudeArr[k] == 0){
			outputMagnitudeArr[k] = pow(10, -20);
		}
		outputPhaseArr[k] = atan(ImXArr[k] / RexArr[k]);
		if( (RexArr[k] < 0) && (ImXArr[k] < 0) ){
			outputPhaseArr[k] -= PI;
		}
		if( (RexArr[k] < 0) && (ImXArr[k] >= 0) ){
			outputPhaseArr[k] += PI;
		}
	}
}

/**
* \fn RectToPol
*
* \brief 
*/
void PolToRect(
	float32_t* RexArr,
	float32_t* ImXArr,
	float32_t* MagnitudeArr,
	float32_t* PhaseArr,
	uint32_t signalLen
){
	uint32_t k;
	for(k=0;k<signalLen;++k){
		RexArr[k] = MagnitudeArr[k] * cosf(PhaseArr[k]);
		ImXArr[k] = MagnitudeArr[k] * sinf(PhaseArr[k]);
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
	
	/*DFT*/
//	DFT(inputSignal_f32_1kHz_15kHz, ReX, ImX, SIGNAL_SIZE);
//	DFToutputMagnitude(ReX, SIGNAL_SIZE/2);
	
	/*ECG DFT*/
//	DFT(inputSignal_f32_1kHz_15kHz, ECGReX, ECGImX, ECG_SIZE);
//	DFToutputMagnitude(ReX, SIGNAL_SIZE/2);
	/*IDFT*/
//	IDFT(ECGOutputSignal_f32, ECGReX, ECGImX, ECG_SIZE);
	
	/*Rect to Pol*/
	DFT(inputSignal_f32_1kHz_15kHz, ReX, ImX, SIGNAL_SIZE);
	RectToPol(ReX, ImX, signalMag, signalPhase, SIGNAL_SIZE);
	PolToRect(ReX, ImX, signalMag, signalPhase, SIGNAL_SIZE);
	
	/*Superloop*/
	while(true){
		/*Input signal*/
//		PlotInputSignal(inputSignal_f32_1kHz_15kHz, SIGNAL_SIZE);
//		PlotOutputSignal(OutputSignal_f32, SIGNAL_SIZE);
//		PlotInputOutputSignal(inputSignal_f32_1kHz_15kHz, OutputSignal_f32, SIGNAL_SIZE);
//		PlotInpulseResponse(impulseResponse, IMP_RESP_LEN);
//		PlotAll(inputSignal_f32_1kHz_15kHz, OutputSignal_f32, impulseResponse, SIGNAL_SIZE, IMP_RESP_LEN);
//		PlotReXSignal(ReX, SIGNAL_SIZE/2);
//		PlotImXSignal(ImX, SIGNAL_SIZE/2);
		
		/*ECG*/
//		PlotInputSignal(_640_points_ecg_, ECG_SIZE);
//		PlotReXSignal(ECGReX, ECG_SIZE/2);
//		PlotOutputSignal(ECGOutputSignal_f32, ECG_SIZE);
//		PlotInputOutputSignal(_640_points_ecg_, ECGOutputSignal_f32, ECG_SIZE);
		
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



