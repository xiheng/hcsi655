//
//  drawnTogetherAppDelegate.m
//  drawnTogether
//
//  Created by Jeremy Kelley on 11/21/09.
//  Copyright Phodder 2009. All rights reserved.
//

#import "drawnTogetherAppDelegate.h"
#import "DrawViewController.h"

@implementation drawnTogetherAppDelegate

@synthesize navController, window;

- (void)applicationDidFinishLaunching:(UIApplication *)application {
	
	dVC = [[DrawViewController alloc] init];
	
	imgPicker = [[UIImagePickerController alloc] init];
	imgPicker.sourceType = UIImagePickerControllerSourceTypeCamera;
	imgPicker.showsCameraControls = NO;
	imgPicker.navigationBarHidden = YES;
	imgPicker.cameraOverlayView = dVC.view;
	
	// self.navController = [[UINavigationController alloc] initWithRootViewController:imgPicker.topViewController];

	
	[window addSubview:imgPicker.view];	
}

- (void)dealloc {
    [window release];
    [super dealloc];
}


@end
