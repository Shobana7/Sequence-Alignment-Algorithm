# Sequence Alignment Algorithm

Task Description
	
  The aim is to implement the sequence alignment problem using two approaches: dynamic programming, a hybrid of divide-and-conquer & dynamic programming. This document summarizes the implementation details and later compares the CPU time and memory usage of the two approaches.

Implementation
	
  Python is used to implement the two algorithms. Section A and B gives an overview of the modules used in each implementation.

 A. Dynamic Programming  
	
  The file consists of 8 function modules.
-> parse_input(): Reads the input test file

-> generate_string(): Generates the two strings str1 and str2 from the base string provided in the input file

-> check_string_length(): Validates the length of the input strings

-> compute_alignment(): Calls compute_memo() and track_memo()

-> compute_memo(): Builds the table for storing optimal substructure answers

-> track_memo(): Traces back and reconstructs the optimal alignment

-> generate_output(): Writes first 50 and last 50 elements of the alignment to the output file

-> main(): Calls the above mentioned functions and calculates the run time and memory usage

 B. Hybrid of divide-and-conquer & dynamic programming	

The file contains all the 8 modules as that of the basic approach but the only difference is in the functionality of the compute_alignment() module.

-> compute_alignment(): Recursively divides str1 into two substrings and computes the optimal break point in str2 by calling compute_memo(). 
When base case is reached, call track_memo() to construct the alignment.

Results 
	
 The two implementations were run with 5000 test cases which are permuted from the given two base strings. The base strings are each of size 4 so the string length varies between 8 and 4096. This makes the combined string length (str1.len + str2.len) to vary between 16 and 8192. 
          The plots in the zip file show the running time (in seconds) and memory usage (in MB) against the problem size. 

Insights
   
   We can see from the Time vs Size line plot that time taken by both the implementations is increasing in almost same fashion. But the increase in memory-efficient version is more than the basic approach; this stems from the fact that the basic approach runs in O(nm) and the memory-efficient version runs in O(2nm) where n and m are size of the input strings.

   The Memory vs Size plot speaks for the hybrid approach. However, we can see that for certain problem sizes there is a drop in the memory usage of the basic approach. This is because the memory depends on the matrix size. Let us consider one such point, say problem size =4102. When the size is 4096, each of the strings has a length of 2048 - a power of 2. When the size is 4102 (not a power of 2), one string is of size 4096 and the other 8. So, points immediately after powers of 2 experience a drop in the memory usage. But it should also be noted that this drop does not go below the value of the efficient solution’s value.

