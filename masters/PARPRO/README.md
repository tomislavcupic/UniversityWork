# Parallel programming

###### Here are my laboratory exercises from class "Parallel programming" or in croatian "Paralelno programiranje" (PARPRO). There are three tasks, each in its folder, and inside every folder exists a pdf version of the instructions for the task. All programs are written in Python and can be ran by running the specific .py file.

---

## Lab 1

##### In the first exercise we had to solve the classic n philosopher problem in parallel programming. In the exercise we used the MPI to write the solution.

## Features:
   * n philosopher problem
   * MPI_Iprobe MPI_Recv
   * clean and dirty forks

---

## Lab 2

##### In the second exercise we had to write a parallel version of the widely known "Connect four" game. The AI that plays should have look into next x possible solutions to form the next move. The program should have the interface where a player can see the board and play against the PC.

## Features:
   * connect four
   * Recursive checks for victory and defeat
   * aglomerations

---

## Lab 3

##### Third exercise was split into three separate tasks which had to be done in OPENCL or CUDA. The first one was to determine how many prim numbers was in an array, with varying number of threads and groups. The second task was to write the calculation of the number PI with varying number of elements. The third task was to program the dynamic of fluids in 2D space and check the acceleration.

## Features:
   * kernels
   * OpenCL programs
   * prim numbers
   * calculating PI
   * dynamic of fluids