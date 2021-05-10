#include <cstdio>
#include <iostream>
#include <queue>

/**
 * \brief       Given a stream of integers and a window size, calculate the moving average of all integers in the sliding window.
 *              
 *              Example:
 *                  MovingAverage m = new MovingAverage(3);
 *                  m.next(1) = 1
 *                  m.next(10) = (1 + 10) / 2
 *                  m.next(3) = (1 + 10 + 3) / 3
 *                  m.next(5) = (10 + 3 + 5) / 3
 * 
 *              https://theaudioprogrammer.com/coding-challenge-moving-average-from-data-stream/
 *              https://leetcode.com/accounts/login/?next=/problems/moving-average-from-data-stream/
 *
 */
    

/**
 * \class    MovingAverage 
 * 
 * \brief    MAF using FIFO template. Add yny type to FIFO and return a filtered double.-
 */
template<typename T>
class MovingAverage {
public:
    /** Initialize your data structure here. */

    /**Constructor*/
    MovingAverage(uint32_t inputValue) {
        this->runningTotal = 0.0;
        this->windowSize = inputValue;
    }
    
    /*Next value*/
    double next(T inputValue) {
        /*Check if buffer is full*/
        if (buffer.size() == windowSize){
            /*Subtract front value from running total*/
            this->runningTotal -= this->buffer.front();
            /*Delete value from front of std::queue*/
            this->buffer.pop();
        }
        /*Add new value*/
        this->buffer.push(inputValue);
        /*update running total*/
        this->runningTotal += inputValue;
        /*Calculate average*/
        return static_cast<double>(this->runningTotal / this->buffer.size());
    }
private:
    /** Initialize your data structure here. */
    uint32_t windowSize;
    double runningTotal;
    std::queue<T> buffer;

};
/**
 *  Your MovingAverage object will be instantiated and called as such:
 * MovingAverage obj = new MovingAverage(size);
 * double param_1 = obj.next(val);
 */

/**
 * \fn       
 * 
 * \brief    
 */

/**
 * \fn main
 * 
 * \brief
 */
int main() {
    /*Say hi*/
    std::cout << "Moving Average Filter: " << std::endl;
    /**/
    MovingAverage<uint64_t> MyU64MAF{64};

    /*Test case*/
    // MovingAverage m = new MovingAverage(3);
    MovingAverage<int> m{3};
    std::cout << "int FIFO" << std::endl;
    std::cout << m.next(1) << std::endl;
    std::cout << m.next(10) << std::endl;
    std::cout << m.next(3) << std::endl;
    std::cout << m.next(5) << std::endl;
    std::cout << std::endl;

    /*uin32_t*/
    MovingAverage<uint32_t> MyU32MAF{4};
    std::cout << "uint32_t FIFO" << std::endl;
    std::cout << MyU32MAF.next(1123) << std::endl;
    std::cout << MyU32MAF.next(1234234) << std::endl;
    std::cout << MyU32MAF.next(6345) << std::endl;
    std::cout << MyU32MAF.next(123412) << std::endl;
    std::cout << std::endl;

    /*uin32_t*/
    MovingAverage<float> MyFltMAF{4};
    std::cout << "float FIFO" << std::endl;
    std::cout << MyFltMAF.next(4.12) << std::endl;
    std::cout << MyFltMAF.next(6.22) << std::endl;
    std::cout << MyFltMAF.next(-3.009) << std::endl;
    std::cout << MyFltMAF.next(2.908) << std::endl;
    std::cout << std::endl;


    return 0;
}