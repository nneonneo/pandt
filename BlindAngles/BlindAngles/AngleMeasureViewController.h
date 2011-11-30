//
//  AngleMeasureViewController.h
//  BlindAngles
//
//  Created by Robert Xiao on 11/4/11.
//  Copyright (c) 2011 Human-Computer Interaction Institute. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "SoundEffect.h"

@interface AngleMeasureViewController : UIViewController {
    __weak IBOutlet UILabel *angleLabel;
}

- (void)updateAngleLabel:(NSString *)labelText;

- (IBAction)calibrateAction;
- (IBAction)goToMainMenu;

@end
