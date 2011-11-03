//
//  TestViewController.m
//  Test
//
//  Created by Sauvik Das on 11/2/11.
//  Copyright 2011 __MyCompanyName__. All rights reserved.
//

#import "TestViewController.h"

@implementation TestViewController

- (IBAction)toggleUpdates:(UIButton *)button {
    if(isUpdating) {
        [motionManager stopGyroUpdates];
        [motionManager stopAccelerometerUpdates];
        [motionManager stopDeviceMotionUpdates];
        isUpdating = NO;
        [button setTitle:@"Start Motion Updates" forState:UIControlStateNormal];
    } else {
        motionManager.gyroUpdateInterval = 
        motionManager.accelerometerUpdateInterval = 
        motionManager.deviceMotionUpdateInterval = 
        0.020; // 20ms

        [motionManager startGyroUpdatesToQueue:motionQueue withHandler:^( CMGyroData* gyroData, NSError* error ) {
            CMRotationRate rate = gyroData.rotationRate;
            NSString *label = [NSString stringWithFormat:@"%0.1f, %0.1f, %0.1f", rate.x, rate.y, rate.z];
            [gyroActiveLabel performSelectorOnMainThread: @selector(setText:) withObject:label waitUntilDone:YES];
		}];

        [motionManager startAccelerometerUpdatesToQueue:motionQueue withHandler:^( CMAccelerometerData* accelerometerData, NSError* error) {
            CMAcceleration accel = accelerometerData.acceleration;
			NSString *label = [NSString stringWithFormat:@"%0.1f, %0.1f, %0.1f", accel.x, accel.y, accel.z];
            [accelActiveLabel performSelectorOnMainThread: @selector(setText:) withObject:label waitUntilDone:YES];
		}];

        [motionManager startDeviceMotionUpdatesUsingReferenceFrame:CMAttitudeReferenceFrameXArbitraryZVertical toQueue:motionQueue withHandler:^(CMDeviceMotion* motionData, NSError* error) {
            CMAttitude *attitude = motionData.attitude;
            NSString *label = [NSString stringWithFormat:@"%0.1f, %0.1f, %0.1f", attitude.roll, attitude.pitch, attitude.yaw];
            [deviceActiveLabel performSelectorOnMainThread: @selector(setText:) withObject:label waitUntilDone:YES];
        }];

        isUpdating = YES;
        [button setTitle:@"Stop Motion Updates" forState:UIControlStateNormal];
    }
}

/*
// The designated initializer. Override to perform setup that is required before the view is loaded.
- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil {
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}
*/

/*
// Implement loadView to create a view hierarchy programmatically, without using a nib.
- (void)loadView {
}
*/



// Implement viewDidLoad to do additional setup after loading the view, typically from a nib.
- (void)viewDidLoad {
	motionManager = [[CMMotionManager alloc] init];
    motionQueue = [[NSOperationQueue alloc] init];
    isUpdating = NO;

    [super viewDidLoad];
}



/*
// Override to allow orientations other than the default portrait orientation.
- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation {
    // Return YES for supported orientations
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}
*/

- (void)didReceiveMemoryWarning {
	// Releases the view if it doesn't have a superview.
    [super didReceiveMemoryWarning];
	
	// Release any cached data, images, etc that aren't in use.
}

- (void)viewDidUnload {
    [gyroActiveLabel release];
    gyroActiveLabel = nil;
    [accelActiveLabel release];
    accelActiveLabel = nil;
    [deviceActiveLabel release];
    deviceActiveLabel = nil;
	// Release any retained subviews of the main view.
	// e.g. self.myOutlet = nil;
}


- (void)dealloc {
	[motionManager release];
    [motionQueue release];

    [gyroActiveLabel release];
    [accelActiveLabel release];
    [deviceActiveLabel release];

    [super dealloc];
}
@end
