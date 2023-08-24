import cv2
import mediapipe as mp
from ultralytics import YOLO 

yolov8 = YOLO("yolov8n.pt")

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
text_color = (255, 255, 255)  # Text color in BGR format (white in this case)
text_thickness = 1  # Thickness of the text
bbox_thickness = 2
det_confidence_threshhold = 0.5
color = (255,0,0)

#Object detection results 
results = None
#Holistic landmark results
land_mark_results = None

def vision():
    global results
    global land_mark_results
    with mp_hands.Hands(min_detection_confidence=0.5 ,min_tracking_confidence=0.5) as hands : 
        while cap.isOpened():
            ret , frame = cap.read()
            if not ret :
                continue
            #Changing the image from BGR to RGB
            image = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)

            #finding the hand landmarks 
            land_mark_results = hands.process(image)
            #show feed
            results = yolov8(frame)

            for bboxes , confidence , class_id in zip(results[0].boxes.xyxy.tolist() , results[0].boxes.conf.tolist() , results[0].boxes.cls.tolist()):
                if confidence >= det_confidence_threshhold:
                    #adding bounding box to frame 
                    cv2.rectangle(frame,(int(bboxes[0]),int(bboxes[1])),(int(bboxes[2]),int(bboxes[3])),color,bbox_thickness)
                    #adding class name with confidence
                    text = str(coco_classes[int(class_id)]) + f'{confidence:.2f}'
                    position = (int(bboxes[0]),int(bboxes[1]))
                    cv2.putText(frame, text, position, font, font_scale, text_color, text_thickness)
            if land_mark_results.multi_hand_landmarks :
                for num,hand in enumerate(land_mark_results.multi_hand_landmarks): 
                    mp_drawing.draw_landmarks(frame , hand , mp_hands.HAND_CONNECTIONS)
            cv2.imshow('Camera Feed', frame)
            if cv2.waitKey(10) & 0xFF == ord('q') :
                break
    cap.release()
    cv2.destroyAllWindows()

#vision()