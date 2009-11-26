//
//  DrawViewController.h
//  drawnTogether
//
//  Created by Jeremy Kelley on 11/21/09.
//  Copyright 2009 Phodder. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <CoreLocation/CoreLocation.h>


@interface DrawViewController : UIViewController <CLLocationManagerDelegate> {
	UIImagePickerController *imgPicker;
	IBOutlet UILabel *dirLabel;
	
	CLLocationManager *locationManager;
}

@property (nonatomic, retain) CLLocationManager *locationManager;

@end
