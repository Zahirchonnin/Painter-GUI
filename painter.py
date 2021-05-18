import requests
import pyautogui
import re
import json
import os
import time
import shutil
import keyboard
from subprocess import Popen
from PIL import Image


class GETDATA:
    # Create func that get positions in painter class
    def get_position(self, image_src, colors, new_colors, bg_color, size, skip_draw, _range):
        
        image_src = image_src.replace('/', '\\')
        image_name = re.compile(r'.*\\(.*)\..*', re.DOTALL).findall(image_src)[-1]
        draw = Image.open(image_src) # Try to open image if it in the cwd.
        try: os.chdir('.\\data')
        except FileNotFoundError : pass

        width, height = size # Get image size

        axiyX, axiyY = pyautogui.size() # Get os size
        axiyX = axiyX - 4 # Subtract the bar size
        axiyY = axiyY - 194 # subtract the paint bar
        ratioW, ratioH = 1, 1 # Add ratio to width and height
        while width > axiyX or height > axiyY:
            if  width > axiyX:
                ratioH =  width // axiyX # Save new height ratio
                width *= ratioW # Save new width size
            
            if height > axiyY:
                ratioW = height // axiyY # Save new width ratio
                height *= ratioH # Save new height ratio

        draw = draw.resize((width, height)) # Resize the image the make it fit to paint board
        pixelPose = [bg_color] # Save pixel poses and colors

        cont = 0
        # Check if the users want to ignore the color that he entred
        for color in colors:
            
            s_d = skip_draw[cont]
            color = tuple(color)
            # Get color range
            tend = _range[cont]
            color = color[:3]

            pixelPose.append(new_colors[cont][:3])

            # Analyzing colors of pixels in image
            for x in range(width):
                for y in range(height):
                    pixelRGB = draw.getpixel((x, y)) # Get pixel color in (x, y) position
                    if type(pixelRGB) == int == type(color): # If the color is not tuple
                        if pixelRGB in range(color - tend, color + tend) and s_d == 'draw': # add color
                            pixelPose.append((x, y))
                        
                        elif pixelPose in range(color - tend, color + tend) and s_d == 'skip': # skip color
                            pixelPose.append((x, y))

                    elif type(pixelRGB) == tuple == type(color): # If the color is tuple 
                       
                        # add color if rgb of the pixel in the given range
                        add = [True for i in range(3) if pixelRGB[i] in range(color[i] - tend, color[i] + tend)]
                        if len(add) == 3 and s_d == 'draw': # add color
                            pixelPose.append((x, y))
                        
                        elif len(add) != 3 and s_d == 'skip': # skip color
                            pixelPose.append((x, y))
            
            cont += 1 # Go to the next color range
        

        if len(pixelPose) > len(colors): # If no pixels found with the given colors
            try:
                os.remove(image_name + '.json')
                os.remove(image_name + '.png')
            except FileNotFoundError:
                pass

            with open(image_name + '.json', 'w') as pixelPoseJSON:
                pixelPoseJSON.write(json.dumps(pixelPose)) # Save data to json file
                pixelPoseJSON.close()
    
    # Create drawer func
    def draw_image(self, choose, way):
        try: os.chdir('.\\data') # Try to change the dirctory
        except FileNotFoundError: pass
        # Get image that can be drawed
        
    
        pixelPoseJson = open(choose) # Open the choosen file
        pixelPose = json.loads(pixelPoseJson.read()) # add data
        pixelPoseJson.close()
        width, height = 0, 0
        for pose in pixelPose: # searching for the larges pixel poseition
            if type(pose) == int or len(pose) == 3: continue # If it a color skip
            
            if pose[0] > width: width = pose[0] # If pixel axiyX bigger then width add it as the new width
            
            if pose[1] > height: height = pose[1] # If pixel axiyY bigger then height add it as the new height
        
        board = Image.new('RGB', (width, height), tuple(pixelPose.pop(0))) # Open a board
        boardName = choose.split('.')[0] + '.png' # Get image name
        board.save(boardName) # save the board with the name
            
        
        # If user want to draw with paint
        if way:
            Popen(['C:\\Windows\\system32\\mspaint.exe', boardName])
            time.sleep(1)
            
            # This func change drawing color
            def get_color(color):
                pyautogui.PAUSE = 0.2
                pyautogui.click(colPos[0], colPos[1]) # Click color editor
                if type(color) == int: color = [color] * 3 # If color is intger make it as a list
                pyautogui.hotkey('shift', 'tab')
                pyautogui.hotkey('shift', 'tab')
                # Go to blue fild and add the rate
                pyautogui.typewrite(str(color[2]))
                pyautogui.hotkey('shift', 'tab')
                # Go to green filed and add the rate
                pyautogui.typewrite(str(color[1]))
                pyautogui.hotkey('shift', 'tab')
                # Go to red filed and add the rate
                pyautogui.typewrite(str(color[0]))
                # Save the color
                pyautogui.press('enter')
                pyautogui.PAUSE = 10 ** (-300) # Change the speed
                return color


            # Get the position of the borad in paint (doesn't work with the rtl os) and
            loc = list(pyautogui.locateOnScreen('..\\from.png')); loc[0] += 5; loc[1] += 145
            if not(loc): loc = [7, 144] # If os is ltr. this is a random positions.
            # Get the color editor position in paint
            colPos = pyautogui.locateOnScreen('..\\color.png')
            for pos in range(len(pixelPose)):
                if keyboard.is_pressed('q'): # If users want to stop drawing
                    break
                
                pos = pixelPose[pos]
                try:

                    if len(pos) == 3: get_color(pos) # If color
                    elif len(pos) == 2: pyautogui.click(pos[0] + loc[0], pos[1] + loc[1]) # If position of pixel
                except: 
                    get_color(pos) # If it int value (color with rgb with same rate)

                

            pyautogui.hotkey('ctrl', 's') # Save the image
        
        else: # If users chose draw without paint it will draw with pillow.
            color = 0
            for pos in pixelPose:

                try:
                    if len(pos) == 3: # If it a color
                        color = pos
                    
                    else: # if it a position
                        try: board.putpixel((pos[0], pos[1]), tuple(color)) # draw the pixel with the current color
                        except: pass
                
                except:
                    color = [pos] * 3 # If it a color rgb with the same rate "0 convert (0, 0, 0)"
            board.save(boardName) # Save the image
            return boardName
        