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
#import "VoiceServices.h"

@interface TestViewController : UIViewController {
    IBOutlet UILabel *gyroActiveLabel;
    IBOutlet UILabel *accelActiveLabel;
    IBOutlet UILabel *deviceActiveLabel;

	CMMotionManager *motionManager;
	NSOperationQueue* motionQueue;
    VSSpeechSynthesizer *speechSynth;

    BOOL isUpdating;
}

- (IBAction)toggleUpdates:(UIButton *)button;

@end
