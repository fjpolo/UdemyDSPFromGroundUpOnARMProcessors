#ifndef _LOWPASSFILTER_H
#define _LOWPASSFILTER_H

/**
* \brief Includes
*/
#include "arm_math.h"                   // ARM::CMSIS:DSP


/**
* \fn low_pass_filter_init
*
* \brief 
*/
void low_pass_filter_init(void);

/**
* \fn low_pass_filter
*
* \brief 
*/
q15_t low_pass_filter(q15_t *input);



#endif // _LOWPASSFILTER_H

