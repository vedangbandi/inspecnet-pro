
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def generate_sample_defects(base_path):
    """
    Generates dummy dataset with defects: hole, scratch, insect, fiber, gel.
    """
    classes = ['hole', 'scratch', 'insect', 'fiber', 'gel', 'good']
    if not os.path.exists(base_path):
        os.makedirs(base_path)
        
    generated_counts = {}
    
    for cls in classes:
        cls_path = os.path.join(base_path, cls)
        os.makedirs(cls_path, exist_ok=True)
        
        count = 0
        for i in range(20): # Generate 20 images per class
            # Random background: grey-ish industrial texture look
            base_color = np.random.randint(200, 240)
            img = Image.new('RGB', (224, 224), color=(base_color, base_color, base_color))
            d = ImageDraw.Draw(img)
            
            # Add some "noise" texturing
            for _ in range(500):
                xy = (random.randint(0, 224), random.randint(0, 224))
                fill = random.randint(180, 255)
                d.point(xy, fill=(fill, fill, fill))
            
            # Draw Defects
            if cls == 'hole':
                # Black circle with some blur
                x, y = random.randint(50, 170), random.randint(50, 170)
                r = random.randint(5, 15)
                d.ellipse((x-r, y-r, x+r, y+r), fill=(20, 20, 20))
                
            elif cls == 'scratch':
                # White/Grey jagged line
                x1, y1 = random.randint(20, 200), random.randint(20, 200)
                x2, y2 = x1 + random.randint(-50, 50), y1 + random.randint(-50, 50)
                width = random.randint(1, 3)
                d.line((x1, y1, x2, y2), fill=(150, 150, 150), width=width)
                
            elif cls == 'insect':
                # Brown/Black irregular blob
                x, y = random.randint(50, 170), random.randint(50, 170)
                d.polygon([(x, y), (x+5, y+2), (x+4, y+8), (x-2, y+6)], fill=(40, 20, 10))
                
            elif cls == 'fiber':
                # Long thin dark curved line
                start = (random.randint(0, 224), random.randint(0, 224))
                end = (start[0] + random.randint(-40, 40), start[1] + random.randint(40, 100))
                d.line([start, end], fill=(10, 10, 60), width=1)
                
            elif cls == 'gel':
                # Semi-transparent blob (simulated)
                # Since PIL standard draw doesn't do alpha on RGB easily without RGBA convert, 
                # we just simulate with a slightly darker circle
                x, y = random.randint(50, 170), random.randint(50, 170)
                r = random.randint(10, 30)
                d.ellipse((x-r, y-r, x+r, y+r), outline=(180, 180, 180), width=2)
                
            # Save
            img.save(os.path.join(cls_path, f"{cls}_{i}.png"))
            count += 1
            
        generated_counts[cls] = count
        
    return generated_counts
