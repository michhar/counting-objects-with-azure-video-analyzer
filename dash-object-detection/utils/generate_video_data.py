# coding: utf-8
import numpy as np
import tensorflow.compat.v1 as tf
import cv2
import time
import base64
import pandas as pd
from visualization_utils import (
    visualize_boxes_and_labels_on_image_array,
)  # Taken from Google Research GitHub
from mscoco_label_map import category_index

tf.disable_v2_behavior()


############################# MODIFY BELOW #############################

# Generate the base64 string of each frame, not recommended
ENCODE_B64 = False
# Prints information about training in console
VERBOSE = False
# Show video being processed in window
SHOW_PROCESS = True
# Create a video with the bounding boxes
WRITE_VIDEO_OUT = True
# Minimum score threshold for a bounding box to be recorded in data
THRESHOLD = 0.2
OUTPUT_FPS = 10.0
# Change name of video being processed
VIDEO_FILE_NAME = "../static/coke-dietcoke-sprite-3"
VIDEO_EXTENSION = ".mp4"

############################# MODIFY ABOVE #############################

# Load a (frozen) Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile("frozen_inference_graph.pb", "rb") as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name="")

# Loading the videocapture objects
cap = cv2.VideoCapture("{}{}".format(VIDEO_FILE_NAME,VIDEO_EXTENSION))
video_FourCC = cv2.VideoWriter_fourcc('a','v','c','1') # *'mp4v' for mp4?
video_fps = cap.get(cv2.CAP_PROP_FPS)
video_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

if WRITE_VIDEO_OUT:
    # Setup the video creation process
    out = cv2.VideoWriter("{}WithBoundingBoxes.mp4".format(VIDEO_FILE_NAME),
                          video_FourCC,
                          OUTPUT_FPS,
                          video_size)
    out_orig = cv2.VideoWriter("{}Original.mp4".format(VIDEO_FILE_NAME),
                               video_FourCC,
                               OUTPUT_FPS,
                               video_size)

# Start the session
with detection_graph.as_default():
    with tf.Session(graph=detection_graph) as sess:
        # Definite input and output Tensors for detection_graph
        image_tensor = detection_graph.get_tensor_by_name("image_tensor:0")
        # Each box represents a part of the image where a particular object was detected.
        detection_boxes = detection_graph.get_tensor_by_name("detection_boxes:0")
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        detection_scores = detection_graph.get_tensor_by_name("detection_scores:0")
        detection_classes = detection_graph.get_tensor_by_name("detection_classes:0")
        num_detections = detection_graph.get_tensor_by_name("num_detections:0")

        frame_base64_ls = (
            []
        )  # The list containing the frame in base64 format and their timestamp
        frame_info_ls = []  # The list containing the information about the frames

        counter = 0
        # init_time = time.time()
        while cap.isOpened():
            ret, image = cap.read()
            
            if ret:
                # Retrieve timestamp
                curr_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                # curr_frame = int(time.time()-init_time)

                # Convert image into an np array
                image_np = np.array(image)
                image_np_expanded = np.expand_dims(image_np, axis=0)

                t1 = time.time()

                # Run the algorithm, retrieve the boxes, score and classes
                (boxes, scores, classes, num) = sess.run(
                    [
                        detection_boxes,
                        detection_scores,
                        detection_classes,
                        num_detections,
                    ],
                    feed_dict={image_tensor: image_np_expanded},
                )

                t2 = time.time()

                # Remove the leading 1 dimension
                boxes = np.squeeze(boxes)
                classes = np.squeeze(classes).astype(np.int32)
                scores = np.squeeze(scores)

                # Draw the bounding boxes with information about the predictions
                visualize_boxes_and_labels_on_image_array(
                    image_np,
                    boxes,
                    classes,
                    scores,
                    category_index,
                    use_normalized_coordinates=True,
                    line_thickness=2,
                )

                # Encode the image into base64
                if ENCODE_B64:
                    retval, buffer = cv2.imencode(".png", image_np)
                    img_str = base64.b64encode(buffer)
                    image_b64 = "data:image/png;base64,{}".format(
                        img_str.decode("ascii")
                    )

                    # Append the image along with timestamp to the frame_base64_ls
                    frame_base64_ls.append([curr_frame, image_b64])

                # Update the output video
                if WRITE_VIDEO_OUT:
                    out.write(image_np)
                    out_orig.write(image)  # Writes the original image

                # Process the information about the video at that exact timestamp
                timestamp_df = pd.DataFrame(
                    [curr_frame] * int(num), columns=["frame"]

                )
                boxes_df = pd.DataFrame(boxes, columns=["y", "x", "bottom", "right"])
                classes_df = pd.DataFrame(classes, columns=["class"])
                score_df = pd.DataFrame(scores, columns=["score"])
                # Maps a np array of integer to their coco index
                coco_map = np.vectorize(lambda i: category_index[i]["name"])
                classes_str_df = pd.DataFrame(coco_map(classes), columns=["class_str"])

                # Concatenate all the information
                info_df = pd.concat(
                    [timestamp_df, boxes_df, classes_df, classes_str_df, score_df],
                    axis=1,
                )

                # Only keep the entries with a score over the threshold
                narrow_info_df = info_df[info_df["score"] > THRESHOLD]

                # Append it the list of information of all the frames
                frame_info_ls.append(narrow_info_df)

                t3 = time.time()

                counter += 1
                if VERBOSE:
                    print(f"Algorithm runtime at frame {counter}: {t2-t1:.2f}")

                if SHOW_PROCESS:
                    cv2.imshow("Object detection", image_np)

                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break

            else:
                break

        if ENCODE_B64:
            # Save the frames in base64
            frame_base64_df = pd.DataFrame(frame_base64_ls, columns=["frame", "source"])
            frame_base64_df.to_csv("video_frames_b64.csv", index=False)

        frame_info_df = pd.concat(frame_info_ls)
        frame_info_df.to_csv(f"{VIDEO_FILE_NAME}DetectionData.csv", index=False)

# Release processes
cap.release()

if WRITE_VIDEO_OUT:
    out.release()
    out_orig.release()

cv2.destroyAllWindows()
