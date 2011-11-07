//
//  AngleEntryViewController.m
//  BlindAngles
//
//  Created by Robert Xiao on 11/4/11.
//  Copyright (c) 2011 Human-Computer Interaction Institute. All rights reserved.
//

#import "AngleEntryViewController.h"
#import "MotionModelController.h"
#import "NumberFormatter.h"

@implementation AngleEntryViewController

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
    [self updateLabel:@"0"];
}

- (void)viewDidUnload
{
    inputLabel = nil;
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
    [MotionModelController getInstance].targetAngle = inputLabel.text.floatValue;
}

/* TODO: localize decimal formatting for non-English locales */
- (void)updateLabel:(NSString *)labelText {
    inputLabel.text = labelText;
    NSString *text = [NumberFormatter getAccessibilityLabelForAngleLabel:labelText];
    inputLabel.accessibilityLabel = [@"Entered angle: " stringByAppendingString:text];
}

- (IBAction)pressDigitKey:(UIButton *)sender {
    NSString *digit = [sender titleForState:UIControlStateNormal];
    UIAccessibilityPostNotification(UIAccessibilityAnnouncementNotification, digit);
    if(0 == [inputLabel.text compare:@"0"]) {
        [self updateLabel:digit];
    } else {
        [self updateLabel:[inputLabel.text stringByAppendingString:digit]];
    }
}

- (IBAction)pressDotKey:(UIButton *)sender {
    if([inputLabel.text rangeOfString:@"."].location == NSNotFound) {
        UIAccessibilityPostNotification(UIAccessibilityAnnouncementNotification, @"dot");
        [self updateLabel:[inputLabel.text stringByAppendingString:@"."]];
    }
}

- (IBAction)pressDeleteKey:(UIButton *)sender {
    UIAccessibilityPostNotification(UIAccessibilityAnnouncementNotification, @"delete");
    if([inputLabel.text length] == 1) {
        [self updateLabel:@"0"];
    } else {
        [self updateLabel:[inputLabel.text substringToIndex:[inputLabel.text length] - 1]];
    }
}
@end
