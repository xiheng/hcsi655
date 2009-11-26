/* found at http://gist.github.com/130045 */

@interface PLCameraController : NSObject
{
    CALayer *_cameraLayer;
    struct CameraDevice *_camera;
    struct CameraImageQueueHelper *_cameraHelper;
    id _delegate;
    UIView *_previewView;
    BOOL _isPreviewing;
    BOOL _isLocked;
    BOOL _wasPreviewingBeforeDeviceLock;
}

+ (id)sharedInstance;
- (id)init;
- (void)dealloc;
- (void)_setIsReady;
- (BOOL)isReady;
- (void)_applicationSuspended;
- (void)_applicationResumed;
- (void)_tookPicture:(struct __CoreSurfaceBuffer *)fp8;
- (void)_tookPicture:(struct CGImage *)fp8 jpegData:(struct __CFData *)fp12 imageProperties:(struct __CFDictionary *)fp16;
- (struct CameraImageQueueHelper *)_cameraHelper;
- (BOOL)_setupCamera;
- (void)_tearDownCamera;
- (void)setDelegate:(id)fp8;
- (id)delegate;
- (struct CGRect)_cameraFrame;
- (id)previewView;
- (void)startPreview;
- (void)stopPreview;
- (void)capturePhoto;

@end
