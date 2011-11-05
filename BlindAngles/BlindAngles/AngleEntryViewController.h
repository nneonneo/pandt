//
//  AngleEntryViewController.h
//  BlindAngles
//
//  Created by Robert Xiao on 11/4/11.
//  Copyright (c) 2011 Human-Computer Interaction Institute. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface AngleEntryViewController : UIViewController {
    __weak IBOutlet UILabel *inputLabel;
}

- (void)updateLabel:(NSString *)labelText;
- (IBAction)pressDigitKey:(UIButton *)sender;
- (IBAction)pressDotKey:(UIButton *)sender;
- (IBAction)pressDeleteKey:(UIButton *)sender;
@end
