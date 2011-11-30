//
//  SoundEffect.m
//  BlindAngles
//
//  Created by Sauvik Das on 11/5/11.
//  Copyright (c) 2011 __MyCompanyName__. All rights reserved.
//

#import "SoundEffect.h"

@implementation SoundEffect
+ (id)soundEffectWithContentsOfFile:(NSString *)aPath {
    if (aPath) {
        return [[SoundEffect alloc] initWithContentsOfFile:aPath];
    }
    return nil;
}

- (id)initWithContentsOfFile:(NSString *)path {
    self = [super init];
    
    if (self != nil) {
        NSURL *aFileURL = [NSURL fileURLWithPath:path isDirectory:NO];
        
        if (aFileURL != nil)  {
            SystemSoundID aSoundID;
            OSStatus error = AudioServicesCreateSystemSoundID((__bridge CFURLRef)aFileURL, &aSoundID);
            
            if (error == kAudioServicesNoError) { // success
                _soundID = aSoundID;
            } else {
                NSLog(@"Error %ld loading sound at path: %@", error, path);
                self = nil;
            }
        } else {
            NSLog(@"NSURL is nil for path: %@", path);
            self = nil;
        }
    }
    return self;
}

-(void)dealloc {
    AudioServicesDisposeSystemSoundID(_soundID);
    //[super dealloc];
}

-(void)play {
    AudioServicesPlaySystemSound(_soundID);
}

@end

