import cv2

class InvasionDetector:
    def __init__(self, reference_image):
        if(reference_image is None):
            print("NO REFERENCE!")
            return
        self.reference_frame = reference_image
        self.delta_sides = 200
        self.delta_top = 60
        self.limit = 40000
        frame_height, frame_width = self.reference_frame.shape[:2]
        reference_gray = cv2.cvtColor(self.reference_frame, cv2.COLOR_BGR2GRAY)
        reference_blurred = cv2.GaussianBlur(reference_gray, (11, 11), 0)
        reference_edges = cv2.Canny(reference_gray, 80, 150)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (31, 31))
        self.reference_edges = cv2.dilate(reference_edges, kernel, iterations=1)
        self.reference_border_left = reference_edges[self.delta_top:frame_height, 0:self.delta_sides]
        self.reference_border_right = reference_edges[self.delta_top:frame_height, frame_width - self.delta_sides:frame_width]
        self.reference_border_top = reference_edges[0:self.delta_top, 0:frame_width]
        self.reference_cropped = self.reference_frame[self.delta_top:frame_height, self.delta_sides:frame_width - self.delta_sides]
        self.ok_frames = 0
        self.bad_frames = 0
        self.invasion_on = False

    def invasionCheck(self, frame):
        """
        Check if there is an invasion on the input image, compared to the reference.
        Returns  if the cropped image if an invasion is not detected, false otherwise.
        """
        frame_height, frame_width = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 150, 200)
        diff = cv2.bitwise_and(edges, cv2.bitwise_not(self.reference_edges))

        border_left = diff[self.delta_top:frame_height, 0:self.delta_sides]
        border_right = diff[self.delta_top:frame_height, frame_width - self.delta_sides:frame_width]
        border_top = diff[0:self.delta_top, 0:frame_width]
        
        cv2.imshow('edges', diff)

        sum = border_left.sum()
        sum += border_right.sum()
        sum += border_top.sum()
        #print("Sum: ", sum)
        if sum > self.limit:
            self.ok_frames = 0
            self.bad_frames += 1
            print('sum:', sum)
            if self.bad_frames >= 1 and not self.invasion_on:
                #print("Invasion detected!")
                self.invasion_on = True
        else:
            self.ok_frames += 1
            self.bad_frames = 0
            if self.ok_frames > 2 and self.invasion_on:
                self.invasion_on = False
        cropped = frame[self.delta_top:frame_height, self.delta_sides:frame_width - self.delta_sides]
        if(self.ok_frames > 2 and not self.invasion_on):
            self.updateReference(edges)
        
        if(not self.invasion_on and self.ok_frames):
            return True, cropped
        else:
            return False, False
    def updateReference(self, new_reference):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (31, 31))
        self.reference_edges = cv2.dilate(new_reference, kernel, iterations=1)

        