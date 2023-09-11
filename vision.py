import cv2
import mediapipe as mp
from ultralytics import YOLO 
import json

from dotenv import load_dotenv
load_dotenv()

#vision_port = os.getenv("VISION_PORT")
#socket sends the output of vision script
#server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_address = (socket.gethostname(),int(vision_port))
#server_socket.bind(server_address)
#server_socket.listen(1)
#print("listening to request .... ")
#client_socket, client_address = server_socket.accept()




yolov8 = YOLO("yolov8s.pt") #change to yolov8n.pt if the performance drops
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
coco_classes = [
    "Person", "Bicycle", "Car", "Motorcycle", "Airplane", "Bus", "Train", "Truck", "Boat", 
    "Traffic Light", "Fire Hydrant", "Stop Sign", "Parking Meter", "Bench", "Bird", "Cat", 
    "Dog", "Horse", "Sheep", "Cow", "Elephant", "Bear", "Zebra", "Giraffe", "Backpack", 
    "Umbrella", "Handbag", "Tie", "Suitcase", "Frisbee", "Skis", "Snowboard", "Sports Ball", 
    "Kite", "Baseball Bat", "Baseball Glove", "Skateboard", "Surfboard", "Tennis Racket", 
    "Bottle", "Wine Glass", "Cup", "Fork", "Knife", "Spoon", "Bowl", "Banana", "Apple", 
    "Sandwich", "Orange", "Broccoli", "Carrot", "Hot Dog", "Pizza", "Donut", "Cake", 
    "Chair", "Couch", "Potted Plant", "Bed", "Dining Table", "Toilet", "TV", "Laptop", 
    "Mouse", "Remote", "Keyboard", "Cell Phone", "Microwave", "Oven", "Toaster", "Sink", 
    "Refrigerator", "Book", "Clock", "Vase", "Scissors", "Teddy Bear", "Hair Dryer", "Toothbrush"
]

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
text_color = (255, 0, 239)  # Text color in BGR format (white in this case)
text_thickness = 1  # Thickness of the text
bbox_thickness = 2
det_confidence_threshhold = 0.5
color = (255,0,0)   #BGR format color of the bounding box
json_file_path = 'output.json'
'''
output = {
        'left_hand_object' : {
            'name' : None,
            'xmin' : None,
            'ymin' : None,
            'xmax' : None,
            'ymax' : None
        },
        'right_hand_object' : {
            'name' : None,
            'xmin' : None,
            'ymin' : None,
            'xmax' : None,
            'ymax' : None
        }, 
        'right_hand_poisture' : None ,
        'left_hand_poisture' : None,
        }
'''

def vision():

    with mp_hands.Hands(min_detection_confidence=0.5 ,min_tracking_confidence=0.5) as hands : 
        while cap.isOpened():
            ret , frame = cap.read()
            #mirrored input
            frame = cv2.flip(frame, 1)
            ##output of each frame
            output = {
                    'left_hand_object' : None,
                    'right_hand_object' : None , 
                    'right_hand_poisture' : None ,
                    'left_hand_poisture' : None,
                }

            if not ret :
                continue

            #cv2.imwrite('current.jpg' , frame)
            #Changing the image from BGR to RGB
            image = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)

            frame_width = frame.shape[1]
            frame_height = frame.shape[0]

            #finding the hand landmarks 
            land_mark_results = hands.process(image)
            #show feed
            results = yolov8(frame , verbose= False)
            #drawing bounding boxes
            for bboxes , confidence , class_id in zip(results[0].boxes.xyxy.tolist() , results[0].boxes.conf.tolist() , results[0].boxes.cls.tolist()):
                if confidence >= det_confidence_threshhold:
                    #adding bounding box to frame 
                    cv2.rectangle(frame,(int(bboxes[0]),int(bboxes[1])),(int(bboxes[2]),int(bboxes[3])),color,bbox_thickness)
                    #adding class name with confidence
                    text = str(coco_classes[int(class_id)]) + f'{confidence:.2f}'
                    position = (int(bboxes[0]),int(bboxes[1]))
                    cv2.putText(frame, text, position, font, font_scale, text_color, text_thickness)
            
            #drawing hand landmarks
            if land_mark_results.multi_hand_landmarks :
                for num,hand in enumerate(land_mark_results.multi_hand_landmarks): 
                    mp_drawing.draw_landmarks(frame , hand , mp_hands.HAND_CONNECTIONS)
            
            if land_mark_results.multi_hand_landmarks :
                for hand_landmarks , handedness in zip(land_mark_results.multi_hand_landmarks , land_mark_results.multi_handedness):
                    #Extracting hand landmarks 
                    handedness_label = handedness.classification[0].label                               #left / right 
                    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                    ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
                    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
                    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                    thumb_cmc = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC]
                    thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]
                    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
                    index_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                    index_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
                    index_finger_dip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP]
                    middel_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
                    middel_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
                    middel_finger_dip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP]
                    ring_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
                    ring_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]
                    ring_finger_dip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP]
                    pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]
                    pinky_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]
                    pinky_dip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP]
                    thumbs_up_guesture = (
                                        thumb_tip.y < thumb_ip.y 
                                        and thumb_ip.y< thumb_mcp.y
                                        and thumb_mcp.y < thumb_cmc.y 
                                        and thumb_cmc.y < wrist.y
                                        and thumb_tip.y < index_finger_tip.y
                                        and index_finger_tip.y < middle_finger_tip.y
                                        and middle_finger_tip.y < ring_finger_tip.y
                                        and ring_finger_tip.y < pinky_tip.y
                                        and index_finger_mcp.y < middel_finger_mcp.y
                                        and middel_finger_mcp.y < ring_finger_mcp.y
                                        and ring_finger_mcp.y < pinky_mcp.y
                                        )
                    
                    '''
                    And other conditions to detect other poistures
                    '''
                    
                    object =  None
                    bbox_of_object = None
                    if results[0].boxes.xyxy.tolist() :
                        for bboxes , confidence , class_id in zip(results[0].boxes.xyxy.tolist() , results[0].boxes.conf.tolist() , results[0].boxes.cls.tolist()):
                            num =0 
                            for landmark in hand_landmarks.landmark :
                                x = landmark.x * frame_width
                                y = landmark.y * frame_height

                                x_inrange = (x > bboxes[0] and x < bboxes[2])
                                y_inrange = (y > bboxes[1] and y < bboxes[3])

                                if y_inrange and x_inrange and confidence > det_confidence_threshhold :
                                    num += 1
                                    break
                            
                            if num > 0 and coco_classes[int(class_id)] != 'Person':
                                 object = coco_classes[int(class_id)]
                                 bbox_of_object = bboxes
        
                    if thumbs_up_guesture and handedness_label=='Left' :
                        cv2.putText(frame , 'Left ThumbsUp' , (25,25) , font ,font_scale , (0,0,0) , text_thickness)
                        output["left_hand_poisture"] = "ThumbsUp"
                        
                    if thumbs_up_guesture and handedness_label == 'Right' :
                        cv2.putText(frame , 'Right ThumbsUp' , (25,45) ,font ,font_scale , (0,0,0) , text_thickness)
                        output["right_hand_poisture"] = "ThumbsUp"
                    
                    if object and handedness_label=='Left' :
                        cv2.putText(frame , f'Left : {object}' , (25,65) ,font ,font_scale , (0,0,0) , text_thickness)
                        output["left_hand_object"] = {'name': object , 'xmin': bbox_of_object[0] , 'ymin': bbox_of_object[1] , 'xmax': bbox_of_object[2] , 'ymax': bbox_of_object[3]}

                        
                    if object and handedness_label == 'Right' :
                        cv2.putText(frame , f'Right : {object}' , (25,85) ,font ,font_scale , (0,0,0) , text_thickness)
                        output["right_hand_object"] = {'name': object , 'xmin': bbox_of_object[0] , 'ymin': bbox_of_object[1] , 'xmax': bbox_of_object[2] , 'ymax': bbox_of_object[3]}
                        

            cv2.imshow('Camera Feed', frame)
            response_json = json.dumps(output)
            with open(json_file_path , 'w') as json_file :
                json_file.write(response_json)

            
            #client_socket.send(response_json.encode('utf-8'))


            if cv2.waitKey(10) & 0xFF == ord('q') :
                break
    cap.release()
    cv2.destroyAllWindows()
    #output['exit_signal'] = True
    #response_json = json.dumps(output)
    #client_socket.send(response_json.encode('utf-8'))
    #client_socket.close()
    #server_socket.close()


vision()