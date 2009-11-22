//
//  DrawViewController.m
//  drawnTogether
//
//  Created by Jeremy Kelley on 11/21/09.
//  Copyright 2009 Phodder. All rights reserved.
//

#import "DrawViewController.h"


@implementation DrawViewController

@synthesize locationManager;


#pragma mark setup helpers


-(void)setupCompass {
	// check if the hardware has a compass
    if (locationManager.headingAvailable == NO) {
        // No compass is available. This application cannot function without a compass, 
        // so a dialog will be displayed and no magnetic data will be measured.
        self.locationManager = nil;
        UIAlertView *noCompassAlert = [[UIAlertView alloc] initWithTitle:@"No Compass!" message:@"Your device has no compass.  You're lost." delegate:nil cancelButtonTitle:@"OK" otherButtonTitles:nil];
        [noCompassAlert show];
        [noCompassAlert release];
    } else {
        // heading service configuration
        locationManager.headingFilter = kCLHeadingFilterNone;
        
        // setup delegate callbacks
        locationManager.delegate = self;
        
        // start the compass
        [locationManager startUpdatingHeading];
    }	
}


#pragma mark UIViewController Gorp


- (id)init {
	self = [super initWithNibName:@"DrawView" bundle:nil];
	
	// initialize our loc manager, which will provide us with gps and compass
	self.locationManager = [[[CLLocationManager alloc] init] autorelease];
	
	return self;
}


// Implement viewDidLoad to do additional setup after loading the view, typically from a nib.
- (void)viewDidLoad {
    [super viewDidLoad];	
	
	// set our bg to transparent
	self.view.backgroundColor = [UIColor clearColor];
	
	// kickstart our compass
	[self setupCompass];
}


- (void)didReceiveMemoryWarning {
	// Releases the view if it doesn't have a superview.
    [super didReceiveMemoryWarning];
	
	// Release any cached data, images, etc that aren't in use.
}

- (void)viewDidUnload {
	// Release any retained subviews of the main view.
	// e.g. self.myOutlet = nil;
}


- (void)dealloc {
    [super dealloc];
}


#pragma mark compass delegates

// This delegate method is invoked when the location manager has heading data.
- (void)locationManager:(CLLocationManager *)manager didUpdateHeading:(CLHeading *)heading {

	// for now, just update the label
	dirLabel.text = [NSString stringWithFormat:@"%f", heading.magneticHeading ];
}


// This delegate method is invoked when the location managed encounters an error condition.
- (void)locationManager:(CLLocationManager *)manager didFailWithError:(NSError *)error {
    if ([error code] == kCLErrorDenied) {
        // This error indicates that the user has denied the application's request to use location services.
        [manager stopUpdatingHeading];
    } else if ([error code] == kCLErrorHeadingFailure) {
        // This error indicates that the heading could not be determined, most likely because of strong magnetic interference.
    }
}




@end
