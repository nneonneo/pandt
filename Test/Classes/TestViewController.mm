//
//  TestViewController.m
//  Test
//
//  Created by Sauvik Das on 11/2/11.
//  Copyright 2011 __MyCompanyName__. All rights reserved.
//

#import "TestViewController.h"
#import "VoiceServices.h"
#import "AudioSessionManager.h"
#import "PocketsphinxController.h"
#import "FliteController.h"
#import "OpenEarsEventsObserver.h"
#import "LanguageModelGenerator.h"

@implementation TestViewController

- (IBAction)toggleUpdates:(UIButton *)button {
    if(isUpdating) {
        [motionManager stopGyroUpdates];
        [motionManager stopAccelerometerUpdates];
        [motionManager stopDeviceMotionUpdates];
        isUpdating = NO;
        [button setTitle:@"Start Motion Updates" forState:UIControlStateNormal];
    } else {
        [speechSynth startSpeakingString:@"3.141592653"]; 

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

- (void) speechSynthesizer:(NSObject *)synth didFinishSpeaking:(BOOL)didFinish withError:(NSError *) error {
    NSLog(@"Finished speaking %d %@", didFinish, error);
}

// Implement viewDidLoad to do additional setup after loading the view, typically from a nib.
- (void)viewDidLoad {
	motionManager = [[CMMotionManager alloc] init];
    motionQueue = [[NSOperationQueue alloc] init];
    speechSynth = [[VSSpeechSynthesizer alloc] init];
    [speechSynth setDelegate:self];

    isUpdating = NO;
    
    AudioSessionManager *audioSessionManager = [[AudioSessionManager alloc]init];
    [audioSessionManager release];
    PocketsphinxController *pocketsphinxController = [[PocketsphinxController alloc]init];
    [pocketsphinxController release];
    FliteController *fliteController = [[FliteController alloc]init];
    [fliteController release];
    LanguageModelGenerator *languageModelGenerator = [[LanguageModelGenerator alloc]init];
    [languageModelGenerator release];

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
    [speechSynth release];

    [gyroActiveLabel release];
    [accelActiveLabel release];
    [deviceActiveLabel release];

    [super dealloc];
}
@end
