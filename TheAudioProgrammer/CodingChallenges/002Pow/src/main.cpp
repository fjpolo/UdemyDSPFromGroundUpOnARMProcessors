#include <cstdio>
#include <iostream>
#include <vector>

/**
 * \brief    Implement pow(x, n), which calculates x raised to the power n (i.e., xn). 
 *            
 *           Example 1:  
 *              Input: x = 2.00000, n = 10
 *              Output: 1024.00000
 *           
 *           Example 2:
 *              Input: x = 2.10000, n = 3
 *              Output: 9.26100
 *              
 *           Example 3:
 *              Input: x = 2.00000, n = -2
 *              Output: 0.25000
 *              Explanation: 2-2 = 1/22 = 1/4 = 0.25
 *           
 *           
 *           Constraints:
 *              -100.0 < x < 100.0
 *              -231 <= n <= 231-1
 *              -104 <= xn <= 104
 * 
 *           References:
 *              - https://leetcode.com/problems/powx-n/
 *              - https://theaudioprogrammer.com/coding-challenge-powxn/
 */
    

/**
 * \fn       myPowBruteForce(double x, long long n)
 * 
 * \brief    We could make a simple solution where we simply loop the number of times of n and directly 
 *          simulate the multiplication process.
 *           This solution runs in O(n) . In other words as power gets larger then the for loop gets longer 
 *          in a linear fashion. On the bright side the space complexity (memory requirements) are constant 
 *          so O(1).  
 */
double myPowBruteForce(double x, long long n) {
    /*if n < 0 we need to calculate a fraction...*/
    if (n<0){
        /*make fraction of x...*/
        x = 1/x;
    }
    /*initialize output...*/
    double outputValue = 1;
    /*loop through the multiplication process...*/
    for (long long i=0; i<abs(n); i++){
        outputValue = outputValue*x;
    }
    return outputValue;
}

/**
 * \fn      recPow(double x, long long n)
 * 
 * \brief
 */
double recPow(double x, long long n){
        double outValue;
        /*base case...*/
        if(n == 0){
            /*no recursion return 1...
            anything to the 0 is 1...*/
            return 1.0;
        }
        else{
            /*call recursive method...*/
            outValue = recPow(x, n/2);
            if(n%2 == 0){
                /*if the exponent is even...
                x^2*/
                return outValue * outValue;
            }
            else{
                /*if the exponent is odd...
                we need x^(2)*x ...*/
                return outValue * outValue * x;
            }
        }
    }

/**
 * \fn      myPowRecursive(double x, long long n)
 * 
 * \brief
 */
double myPowRecursive(double x, long long n) {
    /**
     *  If we think about it, exponents have this characteristic where x^6 is equal to x^(2*3). Here is another example: x^(5) 
     * … is the same as … (x^4)*x … which is the same as … (x^2)*(x^2)*x. So if A=x^n and B=x^(n/2) then A=B*B. If n is odd then 
     * B*B must be x^(n-1).
     * 
     *  There is this pattern where we can break down exponents. By doing this we can create a method that reduces the number of 
     * calculations by steering calculations between even and odd numbers. 
     * 
     *  This has reduced the time complexity to O(log(n)). No matter how large n gets there is an upper limit on the time this function 
     * will take. This is because each time the recursive function is called, n is halved.
     * 
     *  Space complexity (memory requirements) on the other hand has suffered. For each computation we need to store the result of x^(n/2). 
     * We need to do the computation O(log(n)) times and sore the result. Therefore, the space complexity is also O(log(n)).
     */


    /*if n < 0 we need to calculate a fraction...*/
    if(n < 0){
        /*make fraction of x...*/
        x = 1/x;
    }
    return recPow(x,abs(n));
}

/**
 * \fn      myPowIterative(double x, long long n)
 * 
 * \brief
 */
double myPowIterative(double x, long long n) {
    /**
     *  Recursive functions are easy to implement. Coding and syntax wise, they are easy to manage and type out quickly. 
     * The reality of recursive calls is that your computer can only make so many of them. You need to establish a base 
     * case that is checked first in the recursive function. But even if you do, what happens if you need to make a lot 
     * of recursive calls? Well you could hit the recursion stack limit of your computer or language. To address this 
     * people will often make an iterative solution.
     * 
     *  An iterative solution will employ a loop just like all our other solutions. Unlike a recursive approach, it will 
     * not employ a function that calls itself. However, it will still use a complementary theory that we used in the 
     * recursive solution.
     *  
     *  Another way to understand exponents is as follows:
     *      - If we have x^4 then this is the same as x^(2^2).
     *      - If we have x^5 then this is the same as (x^(2^2))*x.
     *      - If we have x^16 then this is the same as x^(2^4) which is the same as (x^(2^(2^2))). 16 is 2^4 .
     *      - If we have x^17 then this is the same as (x^(2^4))*x which is the same as (x^(2^(2^2)))*x.
     * 
     *  Here is what is happening for every iteration of the loop. The loop will run from abs(n) towards the int value that 
     * is greater than 0. Of course this value is 1 but before it reaches 1 the loop will attempt to divide the loop count 
     * by 2
     * 
     *      myPow(2,4)
     *      i:4	productVal 4	
     *      i:2	productVal 16	
     *      i:1	outputValue 16	productVal 256	
     * 
     *  We know that 2^4 is the same as 2^(2^2). Therefore, the exponential term is always even until i=1.
     * 
     *  Let’s consider the case of 3^5 is the same as (3^(2^2)) * 3. Therefore, the exponential term is initially odd, and we 
     * perform outputValue = 1*3 and then productVal = 3^2. The loop then performs an integer division. This means that 5/2 != 2.5. 
     * Instead the fractional term is truncated and we get 5/2 == 2. This loop is even and so we square the productVal again. The 
     * final term is odd and so the outputValue is redefined. Note that the productVal is redefined in the loop but does not figure 
     * in to the calculation.
     * 
     *      myPow(3,5)
     *      i:5	outputValue 3		productVal 9	
     *      i:2				productVal 81	
     *      i:1	outputValue 243		productVal 6561
     */

    /*if n < 0 we need to calculate a fraction...*/
    if (n < 0)
    {
        /*make fraction of x...*/
        x = 1 / x;
    }
    /*initialize output...*/
    double outputValue = 1;
    /*start product must be x at least...*/
    double productVal = x;
    
    /*we only need to calculate for half of n
    and then half of the next so decrement
    by divide by 2...*/
    for (long long i = abs(n); i > 0 ; i /= 2) {
        //std::cout << "\ni:" << i << '\t';
        /*check if i is odd...*/
        if ((i % 2) == 1)
        {   
            /*do the multiplication...*/
            outputValue = outputValue * productVal;
            //std::cout << "outputValue " << outputValue << '\t';
        }
        /*square the value...*/
        productVal = productVal * productVal;
        //std::cout << "productVal " << productVal << '\t';
    }
    return outputValue;
}

/**
 * \fn main
 * 
 * \brief
 */
int main() {
    /*Say hi*/
    std::cout << "Pow(x, n): " << std::endl;



    return 0;
}