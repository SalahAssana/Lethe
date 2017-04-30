#include <stdio.h>
#include <time.h>
#include <iostream>
#include <fstream>
#include <string>
#include <stdint.h>

using namespace std;

int main()
{
   time_t x;
   long ms;
   unsigned short y;
   ifstream infile;
   infile.open("pixelValues.txt", ios::binary | ios::in);
   int frame = 0;
   bool humanDetected = false;
   int maxValue = 0;
   bool hotPixelA = false;
   bool hotPixelB = false;
   bool heightFound = true;
   int totalpixels = 0;
   int height = 0;

   //Process Frames
   while(infile.good())
   {

     //Process a single frame
     for(int i = 0; i <= 4800; i++)
     {
       //First value will be a timestamp
       if(i == 0)
       {
         infile.read((char *) &x, sizeof(x));
	 infile.read((char *) &ms, sizeof(ms));
       }
       //Read the remaining values
       else
       {
         infile.read((char *) &y, sizeof(y));
       }

       //Measuring the height of person in the frame
       if(y > 8400 && heightFound)
       {
	 height = 60 - (i/80);
       }

       //Checking to see if there is a person in the frame
       //if(y > 8400) humanDetected = true;

       //Checking for the max value in the frame
       if(y > maxValue) maxValue = y;

       //Checking which hot pixels are activated
       if(i == 2401)
       {
	if(y > 8100)
	{
	  hotPixelA = true;
	}
       }

       if(i == 2480)
       {
	if(y > 8100)
	{
	  hotPixelB = true;
	}
       }

     }

     //cout << x << "." << ms << endl;

     //cout << "Max Temp: " << maxValue << " ";
     maxValue = 0;

     cout << "The max height found is: " << height << endl;
     height = 0;

     //cout << "State: ";
/*
     if(!hotPixelA && !hotPixelB) cout << "HO" << endl;
     else if(hotPixelA && !hotPixelB) cout << "HA" << endl;
     else if(!hotPixelA && hotPixelB) cout << "HB" << endl;
     else if(hotPixelA && hotPixelB) cout << "HAB" << endl;
     hotPixelA = false;
     hotPixelB = false;
*/
     //if(humanDetected) cout << "A Human Heat Signature Was Detected" << endl;
     //else cout << "No Human Heat Signature Detected" << endl;
     //humanDetected = false;
     
   }

   infile.close();
   return 0;
}
