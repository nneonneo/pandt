//
//  MotionModelController.m
//  BlindAngles
//
//  Created by Robert Xiao on 11/5/11.
//  Copyright (c) 2011 Human-Computer Interaction Institute. All rights reserved.
//

#import "MotionModelController.h"
#include <math.h>

@implementation MotionModelController
static MotionModelController *_instance = nil;

@synthesize targetAngle, angleType;

+ (MotionModelController *)getInstance {
    if(!_instance) {
        _instance = [[MotionModelController alloc] init];
    }
    return _instance;
}

- (id)init {
    self = [super init];
    if(self) {
        motionManager = [[CMMotionManager alloc] init];
        motionQueue = [[NSOperationQueue alloc] init];
        targetAngle = 0.0;
        angleType = MotionModelAngleTypeUnknown;
        setZero = NO;
        zeroAttitude = [[CMAttitude alloc] init];
    }
    return self;
}

- (void)setZeroNow {
    setZero = YES;
}

- (void)startAngleUpdatesWithHandler:(void (^)(float))handler {
    if (angleType == MotionModelAngleTypeUnknown) {
        NSLog(@"Cannot start angle updates with unknown angle type");
        return;
    }

    motionManager.deviceMotionUpdateInterval = 0.020; // 20ms
    [motionManager startDeviceMotionUpdatesUsingReferenceFrame:CMAttitudeReferenceFrameXArbitraryZVertical toQueue:motionQueue withHandler:^(CMDeviceMotion *motionData, NSError *error) {
        if(error) {
            NSLog(@"Error %@ occurred obtaining motion data.", error);
            return;
        }

        CMAttitude *attitude = motionData.attitude;

        if(setZero) {
            zeroAttitude = attitude;
            setZero = NO;
        }

        float angle;

        switch (angleType) {
            case MotionModelAngleTypeBezel:
                angle = attitude.roll - zeroAttitude.roll;
                break;
            case MotionModelAngleTypeMiter:
                angle = attitude.yaw - zeroAttitude.yaw;
                break;
            case MotionModelAngleTypeUnknown:
                NSLog(@"Unknown angle type...");
                return;
        }

        angle = fmodf(angle, M_PI);
        /* convert to degrees */
        angle = angle * 180.0 / M_PI;
        handler(angle);
    }];
}

- (void)stopAngleUpdates {
    [motionManager stopDeviceMotionUpdates];
}

@end
