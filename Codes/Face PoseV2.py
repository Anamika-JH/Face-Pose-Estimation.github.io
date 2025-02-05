import cv2
import dlib
import numpy as np
import socket
import struct

# Camera calibration results
K = np.array([[1.80353608e+03, 0.00000000e+00, 1.27629116e+03],
              [0.00000000e+00, 1.81955638e+03, 9.43034140e+02],
              [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

D = np.array([-0.01579607, 0.02011859, -0.00472382, -0.00368816, -0.05487244])

# Function to round off a floating-point number to 2 decimal places
def roundoff(var):
    return round(var, 2)

# Function to get the camera matrix
def get_camera_matrix(focal_length, center):
    return np.array([[focal_length, 0, center[0]],
                     [0, focal_length, center[1]],
                     [0, 0, 1]])

# UDP Socket Initialization
server_address = ('127.0.0.1', 54000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Open camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Unable to connect to camera")
    exit()

# Load face detection and pose estimation models (dlib)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(r"D:\3D Hologram\Face pose estimation\shape_predictor_68_face_landmarks.dat")

# Fill in camera intrinsics and distortion coefficients
focal_length = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
cam_matrix = get_camera_matrix(focal_length, (cap.get(cv2.CAP_PROP_FRAME_WIDTH) / 2, cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / 2))
dist_coeffs = D

# Fill in 3D reference points (world coordinates)
object_pts = np.array([
    (6.825897, 6.760612, 4.402142),  # left brow left corner
    (1.330353, 7.122144, 6.903745),  # left brow right corner
    (-1.330353, 7.122144, 6.903745),  # right brow left corner
    (-6.825897, 6.760612, 4.402142),  # right brow right corner
    (5.311432, 5.485328, 3.987654),  # left eye left corner
    (1.789930, 5.393625, 4.413414),  # left eye right corner
    (-1.789930, 5.393625, 4.413414),  # right eye left corner
    (-5.311432, 5.485328, 3.987654),  # right eye right corner
    (2.005628, 1.409845, 6.165652),  # nose left corner
    (-2.005628, 1.409845, 6.165652),  # nose right corner
    (2.774015, -2.080775, 5.048531),  # mouth left corner
    (-2.774015, -2.080775, 5.048531),  # mouth right corner
    (0.0, -3.116408, 6.097667),  # mouth central bottom corner
    (0.0, -7.415691, 4.070434)  # chin corner
], dtype=np.float64)

# Main loop
while True:
    # Grab a frame
    ret, temp = cap.read()
    if not ret:
        print("Unable to read frame")
        break

    # Convert the image to grayscale for dlib processing
    gray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    # Find the pose of each face
    if len(faces) > 0:
        # Track features
        shape = predictor(gray, faces[0])

        # Draw features
        for i in range(68):
            cv2.circle(temp, (shape.part(i).x, shape.part(i).y), 2, (0, 0, 255), -1)

        # Fill in 2D reference points
        image_pts = np.array([
            (shape.part(17).x, shape.part(17).y),  # left brow left corner
            (shape.part(21).x, shape.part(21).y),  # left brow right corner
            (shape.part(22).x, shape.part(22).y),  # right brow left corner
            (shape.part(26).x, shape.part(26).y),  # right brow right corner
            (shape.part(36).x, shape.part(36).y),  # left eye left corner
            (shape.part(39).x, shape.part(39).y),  # left eye right corner
            (shape.part(42).x, shape.part(42).y),  # right eye left corner
            (shape.part(45).x, shape.part(45).y),  # right eye right corner
            (shape.part(31).x, shape.part(31).y),  # nose left corner
            (shape.part(35).x, shape.part(35).y),  # nose right corner
            (shape.part(48).x, shape.part(48).y),  # mouth left corner
            (shape.part(54).x, shape.part(54).y),  # mouth right corner
            (shape.part(57).x, shape.part(57).y),  # mouth central bottom corner
            (shape.part(8).x, shape.part(8).y)   # chin corner
        ], dtype=np.float64)
        # Calculate pose
        
        if len(object_pts) >= 4 and len(image_pts) >= 4:
            _, rotation_vec, translation_vec = cv2.solvePnP(object_pts, image_pts, cam_matrix, dist_coeffs)

            # Reproject 3D points world coordinate axis to verify result pose
            reprojectsrc = np.float32([[10.0, 10.0, 10.0],
                                    [10.0, 10.0, -10.0],
                                    [10.0, -10.0, -10.0],
                                    [10.0, -10.0, 10.0],
                                    [-10.0, 10.0, 10.0],
                                    [-10.0, 10.0, -10.0],
                                    [-10.0, -10.0, -10.0],
                                    [-10.0, -10.0, 10.0]])

            # Reproject 3D points world coordinate axis to verify result pose
            reprojectdst, jacobian = cv2.projectPoints(reprojectsrc, rotation_vec, translation_vec, cam_matrix, dist_coeffs)

            
            # Draw cube
            for i in range(4):
                temp = cv2.line(temp, tuple(reprojectdst[i].ravel().astype(int)), tuple(reprojectdst[i].ravel().astype(int)), (0, 0, 255), 3)
            temp = cv2.line(temp, tuple(reprojectdst[0].ravel().astype(int)), tuple(reprojectdst[3].ravel().astype(int)), (0, 0, 255), 3)

            for i in range(4):
                temp = cv2.line(temp, tuple(reprojectdst[i + 4].ravel().astype(int)), tuple(reprojectdst[i].ravel().astype(int)), (0, 0, 255), 3)

            # Draw remaining lines to complete the cube
            temp = cv2.line(temp, tuple(reprojectdst[4].ravel().astype(int)), tuple(reprojectdst[5].ravel().astype(int)), (0, 0, 255), 3)
            temp = cv2.line(temp, tuple(reprojectdst[5].ravel().astype(int)), tuple(reprojectdst[6].ravel().astype(int)), (0, 0, 255), 3)
            temp = cv2.line(temp, tuple(reprojectdst[6].ravel().astype(int)), tuple(reprojectdst[7].ravel().astype(int)), (0, 0, 255), 3)
            temp = cv2.line(temp, tuple(reprojectdst[7].ravel().astype(int)), tuple(reprojectdst[4].ravel().astype(int)), (0, 0, 255), 3)
            temp = cv2.line(temp, tuple(reprojectdst[1].ravel().astype(int)), tuple(reprojectdst[0].ravel().astype(int)), (0, 0, 255), 3)
            temp = cv2.line(temp, tuple(reprojectdst[2].ravel().astype(int)), tuple(reprojectdst[1].ravel().astype(int)), (0, 0, 255), 3)
            temp = cv2.line(temp, tuple(reprojectdst[3].ravel().astype(int)), tuple(reprojectdst[2].ravel().astype(int)), (0, 0, 255), 3)


            # Calculate euler angle
            rotation_mat, _ = cv2.Rodrigues(rotation_vec)
            pose_mat = np.hstack((rotation_mat, translation_vec))
            _, _, _, _, _, _, euler_angle = cv2.decomposeProjectionMatrix(pose_mat)

            # # Show angle result
            # text = f"X: {roundoff(float(euler_angle[0][0]))} Y: {roundoff(float(euler_angle[1][0]))} Z: {roundoff(float(euler_angle[2][0]))}"
            # cv2.putText(temp, text, (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)

            # Display translation vector values
            text = f"X: {roundoff(float(translation_vec[0][0]))} Y: {roundoff(float(translation_vec[1][0]))} Z: {roundoff(float(translation_vec[2][0]))}"
            cv2.putText(temp, text, (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)

            # Display the frame
            cv2.imshow("demo", temp)

            # # Convert euler angles to string
            # angles_str = f"{roundoff(float(euler_angle[0][0]))};{roundoff(float(euler_angle[1][0]))};{roundoff(float(euler_angle[2][0]))}\n"
            # print(angles_str)
            # Convert translation vector values to string
            translation_str = f"{roundoff(float(translation_vec[0][0]))};{roundoff(float(translation_vec[1][0]))};{roundoff(float(translation_vec[2][0]))}\n"
            print(translation_str)

            # Send the string over UDP
            client_socket.sendto(translation_str.encode(), server_address)

        # Press 'Esc' to end
        if cv2.waitKey(1) == 27:
            break

# Close the socket
client_socket.close()

# Release video capture object and close all windows
cap.release()
cv2.destroyAllWindows()