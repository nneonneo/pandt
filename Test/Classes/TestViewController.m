//
//  TestViewController.m
//  Test
//
//  Created by Sauvik Das on 11/2/11.
//  Copyright 2011 __MyCompanyName__. All rights reserved.
//

#import "TestViewController.h"

@implementation TestViewController

-(IBAction)toggleGyroUpdates {
	if (![motionManager isGyroActive]) {
		[motionManager startGyroUpdatesToQueue: gyroQueue withHandler:^( CMGyroData* gyroData, NSError* error ) {
			gyroActiveLabel.text = [NSString stringWithFormat:@"%0.1f,%0.1f,%0.1f",gyroData.rotationRate.x,gyroData.rotationRate.y,gyroData.rotationRate.z];
		}];
		[gyroButton setTitle:@"Stop Gyro" forState:UIControlStateNormal];
	} else {
		[motionManager stopGyroUpdates];
		[gyroButton setTitle:@"Start Gyro" forState:UIControlStateNormal];
	}
}

-(IBAction)toggleAccelUpdates {
	if (![motionManager isAccelerometerActive]) {
		[motionManager startAccelerometerUpdatesToQueue: accelQueue withHandler:^( CMAccelerometerData* accelerometerData, NSError* error) {
			accelActiveLabel.text = [NSString stringWithFormat:@"%0.1f,%0.1f,%0.1f",accelerometerData.acceleration.x,accelerometerData.acceleration.y,accelerometerData.acceleration.z];
		}];
		[accelButton setTitle:@"Stop Accel" forState:UIControlStateNormal];
	} else {
		[motionManager stopAccelerometerUpdates];
		[accelButton setTitle:@"Start Accel" forState:UIControlStateNormal];
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
	gyroQueue = [[NSOperationQueue alloc] init];
	accelQueue = [[NSOperationQueue	alloc] init];
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
	// Release any retained subviews of the main view.
	// e.g. self.myOutlet = nil;
}


- (void)dealloc {
	[motionManager release];
	[gyroQueue release];
	[accelQueue release];
    [super dealloc];
}

@end
