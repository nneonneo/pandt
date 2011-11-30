//
//  AngleMeasureViewController.m
//  BlindAngles
//
//  Created by Robert Xiao on 11/4/11.
//  Copyright (c) 2011 Human-Computer Interaction Institute. All rights reserved.
//

#import "AngleMeasureViewController.h"
#import "MotionModelController.h"
#import "NumberFormatter.h"

@implementation AngleMeasureViewController

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
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
    }];
}

- (void)viewDidUnload
{
    angleLabel = nil;
    [super viewDidUnload];
    // Release any retained subviews of the main view.
    // e.g. self.myOutlet = nil;
}

- (void)viewDidDisappear:(BOOL)animated
{
    MotionModelController *motionModel = [MotionModelController getInstance];
    [motionModel stopAngleUpdates];
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    // Return YES for supported orientations
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}

- (void)updateAngleLabel:(NSString *)labelText {
    angleLabel.text = [@"Current: " stringByAppendingString:labelText];
    NSString *text = [NumberFormatter getAccessibilityLabelForAngleLabel:labelText];
    angleLabel.accessibilityLabel = [@"Current angle: " stringByAppendingString:text];
    
}

- (IBAction)calibrateAction {
    MotionModelController *motionModel = [MotionModelController getInstance];
    [motionModel setZeroNow];
}

- (IBAction)goToMainMenu {
    UIWindow *window = [[self view] window];
    /* XXX This will crash if you don't have a navigation controller at the root! */
    UINavigationController *root_controller = (UINavigationController *)[window rootViewController];
    [root_controller popToRootViewControllerAnimated:YES];
}
@end
