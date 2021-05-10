#include <cstdio>
#include <iostream>
#include <vector>

/**
 * \brief    Given an integer array nums, move all 0's to the end of it 
 *          while maintaining the relative order of the non-zero elements.
 *          
 *          Example
 *              Input: [0,1,0,3,12]
 *              Output: [1,3,12,0,0]
 * 
 *          Constraints:
 *              1 <= nums.length <= 104
 *              -231 <= nums[i] <= 231 - 1
 * 
 *          Note
 *              You must do this in-place without making a copy of the array.
 *              Minimize the total number of operations.
 *          
 *          References:
 *              - https://leetcode.com/problems/move-zeroes/
 *              - https://theaudioprogrammer.com/code-challenge-move-zeroes/
 * 
 */
    

/**
 * \fn moveZeroes
 * 
 * \brief
 */
void moveZeroes(std::vector<int>& nums){
    /**
     * All STL containers have some standard functions that behave similarly. In the code below, I have used a few of these standard container functions on the vector nums:
     *  
     *      - nums.size() returns the size of the vector.
     *      - nums.erase() erases a value from a position. However, this position is not an index like nums[i]. This is given in the form of an iterator.
     *      - nums.begin() is an iterator that points to the beginning of the vector.
     *      - nums.insert() takes an iterator and a value to insert into the vector.
     *      - nums.end() is an iterator that points to the end of the vector.
     */

    /*loop through vector like normal...*/
        for (int i=0, j=0; i<nums.size(); ++i){
            /*j is a slower index that advances
            only when we find a non-zero element...*/
            /*if the current element is not a 0...*/
            if (nums[i] != 0){
                /**
                 * swap the values...
                 * increment the index of j...
                 * continue with loop...
                 */
                std::swap(nums[j++], nums[i]);
            }
        }   
}



/**
 * \fn main
 * 
 * \brief
 */
int main() {
    /*Say hi*/
    std::cout << "Move Zeros: " << std::endl;

    /*Test array*/
    std::vector<int> test{0, 0, 0,1,2,3,4};
    /*Print*/
    for(auto itr : test){
		std::cout << itr << " ";
	}
	std::cout << std::endl;
    
    /*Call function*/
    moveZeroes(test);
    /*Print*/
    for(auto itr : test){
		std::cout << itr << " ";
	}
	std::cout << std::endl;

    return 0;
}