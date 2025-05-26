import cv2

# Path to the video file
video_path = 'boneco3.mp4'  # Change this to your video file path

# Open the video
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Define crop region
delta_sides = 200
delta_top = 60
ret, frame = cap.read()
ret, frame = cap.read()
reference_frame = frame.copy()
frame_height, frame_width = frame.shape[:2]
reference_gray = cv2.cvtColor(reference_frame, cv2.COLOR_BGR2GRAY)
reference_blurred = cv2.GaussianBlur(reference_gray, (11, 11), 0)
reference_edges = cv2.Canny(reference_gray, 80, 150)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (31, 31))
reference_edges = cv2.dilate(reference_edges, kernel, iterations=1)
reference_border_left = reference_edges[delta_top:frame_height, 0:delta_sides]
reference_border_right = reference_edges[delta_top:frame_height, frame_width - delta_sides:frame_width]
reference_border_top = reference_edges[0:delta_top, 0:frame_width]
reference_cropped = reference_frame[delta_top:frame_height, delta_sides:frame_width - delta_sides]


ok_frames = 0
bad_frames = 0
invasion_on = False
limit = 3000
red =reference_cropped.copy()
red[:, :] = (0, 0, 255)
cv2.imshow('Canny Edges', reference_edges)
cv2.imshow('frame', reference_cropped)
cv2.imshow('original', frame)
cv2.waitKey(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_height, frame_width = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 150, 200)
    diff = cv2.bitwise_and(edges, cv2.bitwise_not(reference_edges))

    border_left = diff[delta_top:frame_height, 0:delta_sides]
    border_right = diff[delta_top:frame_height, frame_width - delta_sides:frame_width]
    border_top = diff[0:delta_top, 0:frame_width]

    sum = border_left.sum()
    sum += border_right.sum()
    sum += border_top.sum()
    print("Sum: ", sum)
    if sum > limit:
        ok_frames = 0
        bad_frames += 1
        if bad_frames > 3 and not invasion_on:
            print("Invasion detected!")
            invasion_on = True
    else:
        ok_frames += 1
        bad_frames = 0
        if ok_frames > 3:
            if invasion_on:
                print("Invasion ended.")
                invasion_on = False
    cropped = frame[delta_top:frame_height, delta_sides:frame_width - delta_sides]

    # Display the result
    cv2.imshow('Canny Edges', diff)
    cv2.imshow('frame', red if invasion_on else cropped)
    cv2.imshow('original', frame)
    if(ok_frames):
        ok_frames = ok_frames
        ##reference_edges = cv2.dilate(edges, kernel, iterations=1)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()