//
//  NumberFormatter.m
//  BlindAngles
//
//  Created by Robert Xiao on 11/5/11.
//  Copyright (c) 2011 Human-Computer Interaction Institute. All rights reserved.
//

#import "NumberFormatter.h"

@implementation NumberFormatter

+ (NSString *)getAccessibilityLabelForAngleLabel:(NSString *)labelText {
    if(labelText.floatValue == 1.0) {
        return @"1 degree";
    } else {
        if([labelText length] == 0) {
            NSLog(@"Invalid label text received...");
            return @"0 degrees";
        }
        if([labelText characterAtIndex:[labelText length] - 1] == '.') {
            /* Strip off trailing dot for accessibility label */
            labelText = [labelText substringToIndex:[labelText length] - 1];
        }
        /* Replace "." (spoken as 'dot') with " point " */
        labelText = [labelText stringByReplacingOccurrencesOfString:@"." withString:@" point "];
        return [labelText stringByAppendingString:@" degrees"];
    }
}

@end
