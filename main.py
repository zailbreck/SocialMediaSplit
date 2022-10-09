from pyffmpeg import FFmpeg 
import time, os
from PIL import Image, ImageFont, ImageDraw

def setWM(src, dst, wm):
    ff = FFmpeg()
    ff.options(f"-i {src} -i {wm} -filter_complex overlay=50:50 {dst}")

def splitFile(src, dir, waktu=150, ext='.mkv'):
    x = time.strftime('%H:%M:%S', time.gmtime(waktu))
    ff = FFmpeg()
    ff.options(f"-i {src} -c copy -map 0 -segment_time {x} -f segment -reset_timestamps 1 {dir}part_%02d{ext}")
    
def txt2img(text):
    length_text = len(text)
    base_length = 220 + (length_text * 12)
    img  = Image.new('RGBA', (base_length ,50), (255,255,255,1))
    fnt = ImageFont.truetype('font\performance.ttf', 20)
    d = ImageDraw.Draw(img)
    d.text((10,10), text, font=fnt, fill=(255,255,255))
    img.save('tmp/wm_tmp.png')

def checkFolder(dst):
    if not os.path.isdir(dst):
        os.mkdir(dst)
    
def setWatermark(src,dst):
    tmp = src.split("\\")
    src_len = len(tmp)-2
    base_name = f"{tmp[src_len-1]}_EPS_{tmp[src_len]}"
    base_dest = f"{dst}{tmp[src_len-1]}_WM"
    dest = f"{base_dest}\{tmp[src_len]}\\"
    
    # print(dest)
    
    # Check Folder
    checkFolder(base_dest)
    checkFolder(dest)
    

    for itm in os.listdir(src):
        name,ext = os.path.splitext(itm)
        title = f"{base_name}_{name}"
        source = src+itm
        destin = dest+itm
        print(f"Apply Watermark to -> {base_name} part {name[-2:]}")
        # Generate Image
        txt2img(title)
        
        # Apply WM
        setWM(source, destin, 'tmp\\wm_tmp.png')
    pass

def main():
    base_path = os.getcwd()
    src_path = base_path + "\src\\"
    dst_path = base_path + "\dst\\"
    project_path = os.listdir(src_path)
    
    for itm in project_path:
        checkFolder(dst_path+itm)
        lists = os.listdir(src_path + itm) # /src/Movie_Name
        for files in lists:
            # extract Name and Extension
            name,ext = os.path.splitext(files)
            if ext.lower() == ".mkv":
                print(f'Proccessing -> {files}')
                start = time.time() # Time Counter
                
                # splitting file
                src = f"{src_path}{itm}\{files}"
                dst  = f"{dst_path}{itm}\{name}\\"
                
                checkFolder(dst)
                splitFile(src, dst, 150, '.mkv')
            
                # Set Watermarkw    
                setWatermark(dst, dst_path)
                end = time.time()
                print(f'Proccessed in : {round(end - start,2)}s')
            else:
                pass
            
if __name__ == "__main__":
    main()

    
    
""" 
1. Check Every Video From Each Folder
2. Split Video Each 150 seconds
3. Make Watermark for Each Video
4. Add Watermark to each video
"""