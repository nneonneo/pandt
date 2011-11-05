//
//  MotionModelController.h
//  BlindAngles
//
//  Created by Robert Xiao on 11/5/11.
//  Copyright (c) 2011 Human-Computer Interaction Institute. All rights reserved.
//

/* Singleton class to implement angle measurement logic. */

#import <Foundation/Foundation.h>
#import <CoreMotion/CoreMotion.h>

typedef enum {
    MotionModelAngleTypeUnknown,
    MotionModelAngleTypeBezel,
    MotionModelAngleTypeMiter,
} MotionModelAngleType;

@interface MotionModelController : NSObject {
    CMMotionManager *motionManager;
    NSOperationQueue *motionQueue;

    float targetAngle;
    MotionModelAngleType angleType;

    BOOL setZero;
    CMAttitude *zeroAttitude;
}

@property (readwrite) float targetAngle;
@property (readwrite) MotionModelAngleType angleType;

+ (MotionModelController *)getInstance;

/* Set next motion update as zero point */
- (void)setZeroNow;

/* Start updates. The callback is called periodically with the new angle. */
- (void)startAngleUpdatesWithHandler:(void (^)(float))handler;
- (void)stopAngleUpdates;

@end
