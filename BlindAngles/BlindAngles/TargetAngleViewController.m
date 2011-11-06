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
static int soundPlayCounter = 0;
const int PLAY_SOUND_AT = 10;
const float ANGLE_THRESHOLD = 1.0f;
BOOL hitAngle = false;

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
        [self setupSounds];
    }
    return self;
}

- (void)setupSounds {
    NSBundle *mainBundle = [NSBundle mainBundle];
    farSound = [[SoundEffect alloc] initWithContentsOfFile:[mainBundle pathForResource:@"farSound" ofType:@"caf"]];
    nearSound = [[SoundEffect alloc] initWithContentsOfFile:[mainBundle pathForResource:@"nearSound" ofType:@"caf"]];
    levelSound = [[SoundEffect alloc] initWithContentsOfFile:[mainBundle pathForResource:@"levelSound" ofType:@"caf"]];
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
    MotionModelController *motionModel = [MotionModelController getInstance];
    [motionModel setZeroNow]; // TODO: is this an appropriate time to zero?
    [motionModel startAngleUpdatesWithHandler:^(float angle) {
        NSString *labelText = [NSString stringWithFormat:@"%.1f", angle];
        [self performSelectorOnMainThread:@selector(updateAngleLabel:) withObject:labelText waitUntilDone:YES];
        soundPlayCounter++;
        
        if (soundPlayCounter == PLAY_SOUND_AT) {
            [self updateSoundForAngle:angle end:[motionModel targetAngle]];
            soundPlayCounter = 0;
        }
    }];

}


- (void)updateAngleLabel:(NSString *)labelText {
    angleLabel.text = [@"Current: " stringByAppendingString:labelText];
    NSString *text = [NumberFormatter getAccessibilityLabelForAngleLabel:labelText];
    angleLabel.accessibilityLabel = [@"Current angle: " stringByAppendingString:text];
    
}

- (void)updateSoundForAngle:(float)angle end:(float)targetAngle {
    if (angle < targetAngle - ANGLE_THRESHOLD) {
        [farSound play];
        hitAngle = false;
    } else if (angle > targetAngle + ANGLE_THRESHOLD) {
        [nearSound play];
        hitAngle = false;
    } else if (!hitAngle) {
        [levelSound play];
        hitAngle = true;
    }
}

- (void)viewDidUnload
{
    [super viewDidUnload];
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
