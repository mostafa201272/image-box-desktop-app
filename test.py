# [01] GUI LIB
import dearpygui.dearpygui as dpg
import array
import numpy as np
import cv2


# To access any DPG commands
dpg.create_context()

# Define the application viewport
dpg.create_viewport(
    title='Elsherbiniy Image Box', 
    max_width=1024, max_height=768,
    min_width= 1024, min_height= 768,
    width=1024, height= 768,
    x_pos=0, y_pos=0,
    resizable= True,
    always_on_top= False,
    decorated= True
    )


w,h,d = 856 ,480 ,3
raw_data = np.zeros((h,w,d), dtype=np.float32)

def update_dynamic_texture(new_frame):
    global raw_data, w, h, d

    width, height, channels, data = dpg.load_image(new_frame)
    

    h2, w2, d2 = data.shape
    raw_data[:h2, :w2, :d2] = data[:, :, :] / 255

    # print("-" * 50)
    # print(f"Data Row: {raw_data}")
    # print("=" * 50)
    # exit(0)


# Button Call Back Function
def button_call_back():
    global raw_data
    print("Video Execute")

    
    cap = cv2.VideoCapture('/home/mostafa/Desktop/1638781__ep19_cima4u.mp4')

    while cap.isOpened():
        
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        cv2.imwrite('frame.png', frame)
        if dpg.is_dearpygui_running():
            update_dynamic_texture('frame.png')
        else:
            break

        cv2.waitKey(30)

        cv2.imshow('frame', frame)
        if cv2.waitKey(30) == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()

# Define Form
with dpg.window(label="Video", width=300, height=100, pos=(0, 0), autosize=True, no_move=True, no_close=True, no_collapse=True):
    dpg.add_button(label="Start Video Streaming!", callback= button_call_back)


with dpg.texture_registry(show=True):
    # dpg.add_raw_texture(width=w, height=h, default_value=raw_data, format=dpg.mvFormat_Float_rgb, tag="texture_tag")
    dpg.add_raw_texture(width=w, height=h, default_value=raw_data, format=dpg.mvFormat_Float_rgb, tag="texture_tag")

with dpg.window(label="Tutorial"):
    dpg.add_image("texture_tag")

# Initialize the GUI
dpg.setup_dearpygui()

# Displayt the viewport
dpg.show_viewport()

# Display the GUI
dpg.start_dearpygui()

# Proper clean up of DPG
dpg.destroy_context()

