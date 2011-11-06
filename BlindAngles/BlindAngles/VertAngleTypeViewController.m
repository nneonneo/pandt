//
//  VertAngleTypeViewController.m
//  BlindAngles
//
//  Created by Sauvik Das on 11/6/11.
//  Copyright (c) 2011 __MyCompanyName__. All rights reserved.
//

#import "VertAngleTypeViewController.h"
#import "MotionModelController.h"

@implementation VertAngleTypeViewController

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

/*
// Implement viewDidLoad to do additional setup after loading the view, typically from a nib.
- (void)viewDidLoad
{
    [super viewDidLoad];
}
*/

- (void)viewDidUnload
{
    bevelButton = nil;
    miterButton = nil;
    [super viewDidUnload];
    // Release any retained subviews of the main view.
    // e.g. self.myOutlet = nil;
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    // Return YES for supported orientations
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}

- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    NSLog(@"Entering prepareForSegue...");
    MotionModelController *motionModel = [MotionModelController getInstance];
    if(sender == bevelButton) {
        NSLog(@"Bevel button pressed");
        motionModel.angleType = MotionModelAngleTypeBezel;
    } else if(sender == miterButton) {
        NSLog(@"Miter button pressed");
        motionModel.angleType = MotionModelAngleTypeMiter;
    } else {
        motionModel.angleType = MotionModelAngleTypeUnknown;
    }
}

@end
