//
//  drawnTogetherAppDelegate.h
//  drawnTogether
//
//  Created by Jeremy Kelley on 11/21/09.
//  Copyright Phodder 2009. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "DrawViewController.h"

@interface drawnTogetherAppDelegate : NSObject <UIApplicationDelegate> {
    UIWindow *window;
	UINavigationController *navController;
	
	UIImagePickerController *imgPicker;
	DrawViewController *dVC;
}

@property (nonatomic, retain) IBOutlet UIWindow *window;
@property (nonatomic, retain) UINavigationController *navController;

@end