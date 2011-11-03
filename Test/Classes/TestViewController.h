//
//  TestViewController.h
//  Test
//
//  Created by Sauvik Das on 11/2/11.
//  Copyright 2011 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <CoreMotion/CoreMotion.h>
#import <Foundation/Foundation.h>

@interface TestViewController : UIViewController {
	IBOutlet UILabel *gyroActiveLabel;
	IBOutlet UILabel *accelActiveLabel;
	IBOutlet UIButton *gyroButton;
	IBOutlet UIButton *accelButton;
	CMMotionManager *motionManager;
	NSOperationQueue* gyroQueue;
	NSOperationQueue* accelQueue;
}

-(IBAction)toggleGyroUpdates;
-(IBAction)toggleAccelUpdates;
@end

