//
//  TargetAngleViewController.m
//  BlindAngles
//
//  Created by Robert Xiao on 11/4/11.
//  Copyright (c) 2011 Human-Computer Interaction Institute. All rights reserved.
//

#import "TargetAngleViewController.h"
#import "NumberFormatter.h"
#import "MotionModelController.h"

@implementation TargetAngleViewController

@synthesize hitPlayCounter,hitAngle,soundPlayCounter;

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}

- (void)setupSounds {
    NSBundle *mainBundle = [NSBundle mainBundle];
    overSound = [[SoundEffect alloc] initWithContentsOfFile:[mainBundle pathForResource:@"farSound" ofType:@"caf"]];
    underSound = [[SoundEffect alloc] initWithContentsOfFile:[mainBundle pathForResource:@"nearSound" ofType:@"caf"]];
    hitSound = [[SoundEffect alloc] initWithContentsOfFile:[mainBundle pathForResource:@"levelSound" ofType:@"caf"]];
}


- (void)didReceiveMemoryWarning
{
    // Releases the view if it doesn't have a superview.
    [super didReceiveMemoryWarning];
    
    // Release any cached data, images, etc that aren't in use.
}

#pragma mark - View lifecycle

/*
// Implement loadView to create a view hierarchy programmatically, without using a nib.
- (void)loadView
{
}
*/


// Implement viewDidLoad to do additional setup after loading the view, typically from a nib.
- (void)viewDidLoad
{    
    [super viewDidLoad];
    [self setupSounds];
    MotionModelController *motionModel = [MotionModelController getInstance];
    soundPlayCounter = 0;
    hitAngle = false;
    hitPlayCounter = 0;
    [self updateTargetLabel:[NSString stringWithFormat:@"%.1f", motionModel.targetAngle]];
    [motionModel setZeroNow]; // TODO: is this an appropriate time to zero?
    [motionModel startAngleUpdatesWithHandler:^(float angle) {
        NSString *labelText = [NSString stringWithFormat:@"%.1f", angle];
        [self performSelectorOnMainThread:@selector(updateAngleLabel:) withObject:labelText waitUntilDone:YES];
        soundPlayCounter++;
        
        if (soundPlayCounter == [self calculateSoundRate:angle dest:[motionModel targetAngle]]) {
            //NSLog([@"Sound rate is:" stringByAppendingString:[NSString stringWithFormat:@"%i",[self calculateSoundRate:angle dest:[motionModel targetAngle]]]]);
            [self updateSoundForAngle:angle end:[motionModel targetAngle]];
            soundPlayCounter = 0;
        }
    }];
}

/*
 Calculates sound rate by linearly interpolating between MAX_SOUND_RATE and MIN_SOUND_RATE.
 The interpolation parameter reduces to (MAX-MIN)*threshold/distance so that the sound rate is lowest
 when the angle is right at the threshold
 */
- (int)calculateSoundRate:(float)angle dest:(float)targetAngle {
    float dist = targetAngle - angle;
    float denom = (ANGLE_THRESHOLD == 0.0)? 1.0f : ANGLE_THRESHOLD;
    return round(MAX_SOUND_RATE + ((MIN_SOUND_RATE-MAX_SOUND_RATE)/(dist/denom)));
}

- (void)updateTargetLabel:(NSString *)labelText {
    targetLabel.text = [@"Target: " stringByAppendingString:labelText];
    NSString *text = [NumberFormatter getAccessibilityLabelForAngleLabel:labelText];
    targetLabel.accessibilityLabel = [@"Target angle: " stringByAppendingString:text];
}

- (void)updateAngleLabel:(NSString *)labelText {
    angleLabel.text = [@"Current: " stringByAppendingString:labelText];
    NSString *text = [NumberFormatter getAccessibilityLabelForAngleLabel:labelText];
    angleLabel.accessibilityLabel = [@"Current angle: " stringByAppendingString:text];
}

- (void)updateSoundForAngle:(float)angle end:(float)targetAngle {
    if (angle < targetAngle - ANGLE_THRESHOLD) {
        [underSound play];
        hitAngle = false;
        hitPlayCounter = 0;
    } else if (angle > targetAngle + ANGLE_THRESHOLD) {
        [overSound play];
        hitAngle = false;
        hitPlayCounter = 0;
    } else if (!hitAngle) {
        [hitSound play];
        hitAngle = (++hitPlayCounter >= STOP_HIT_SOUND_AT);
    }
}

- (void)viewDidUnload
{
    angleLabel = nil;
    targetLabel = nil;
    [super viewDidUnload];
    MotionModelController *motionModel = [MotionModelController getInstance];
    [motionModel stopAngleUpdates];
    // Release any retained subviews of the main view.
    // e.g. self.myOutlet = nil;
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    // Return YES for supported orientations
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}

- (IBAction)goToMainMenu {
    UIWindow *window = [[self view] window];
    /* XXX This will crash if you don't have a navigation controller at the root! */
    UINavigationController *root_controller = (UINavigationController *)[window rootViewController];
    [root_controller popToRootViewControllerAnimated:YES];
}

@end
