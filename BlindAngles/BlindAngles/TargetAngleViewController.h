//
//  TargetAngleViewController.h
//  BlindAngles
//
//  Created by Robert Xiao on 11/4/11.
//  Copyright (c) 2011 Human-Computer Interaction Institute. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "SoundEffect.h"

@interface TargetAngleViewController : UIViewController {
    __weak IBOutlet UILabel *targetLabel;
    __weak IBOutlet UILabel *angleLabel;
    SoundEffect *farSound;
    SoundEffect *nearSound;
    SoundEffect *levelSound;
}

- (void)setupSounds;
- (void)updateTargetLabel:(NSString *)labelText;
- (void)updateAngleLabel:(NSString *)labelText;
- (void)updateSoundForAngle:(float)angle end:(float)targetAngle;
- (IBAction)goToMainMenu;

@end
