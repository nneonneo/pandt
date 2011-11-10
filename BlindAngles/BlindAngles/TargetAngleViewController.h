//
//  TargetAngleViewController.h
//  BlindAngles
//
//  Created by Robert Xiao on 11/4/11.
//  Copyright (c) 2011 Human-Computer Interaction Institute. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "SoundEffect.h"

//horrible block of constants
const int STOP_HIT_SOUND_AT = 3;
const int MAX_SOUND_RATE = 10;
const int MIN_SOUND_RATE = 30;
const float ANGLE_THRESHOLD = 1.0f;
//END

@interface TargetAngleViewController : UIViewController {
    __weak IBOutlet UILabel *targetLabel;
    __weak IBOutlet UILabel *angleLabel;
    SoundEffect *overSound;
    SoundEffect *underSound;
    SoundEffect *hitSound;
}

@property (readwrite) BOOL hitAngle;
@property (readwrite) int soundPlayCounter;
@property (readwrite) int hitPlayCounter;

- (void)setupSounds;
- (int)calculateSoundRate:(float)angle dest:(float)targetAngle;
- (void)updateTargetLabel:(NSString *)labelText;
- (void)updateAngleLabel:(NSString *)labelText;
- (void)updateSoundForAngle:(float)angle end:(float)targetAngle;
- (IBAction)calibrateAction;
- (IBAction)goToMainMenu;
@end
