/*----------------------------------------------------------------------------*/
/*                                                                            */
/*    Module:       main.cpp                                                  */
/*    Author:       C:\Users\FRC                                              */
/*    Created:      Tue Sep 27 2022                                           */
/*    Description:  V5 project                                                */
/*                                                                            */
/*----------------------------------------------------------------------------*/

// ---- START VEXCODE CONFIGURED DEVICES ----
// ---- END VEXCODE CONFIGURED DEVICES ----

#include "vex.h"

using namespace vex;

// A global instance of vex::brain used for printing to the V5 brain screen
vex::brain       Brain;

int main() {
  // Initializing Robot Configuration. DO NOT REMOVE!
  // vexcodeInit();
  Brain.Screen.printAt( 10, 50, "Hello V5" );
   
    while(1) {
        
        // Allow other tasks to run
        this_thread::sleep_for(10);
    }
  
}
