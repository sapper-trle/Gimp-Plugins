#!/usr/bin/env python

# GIMP Plug-in for Tomb Raider Level Editor .raw/.pak files

from gimpfu import *
import os
import sys

log=False
DEBUG=False

if DEBUG:
    try:
        # TODO: change filepath to suit
        sys.stderr = open('F:/python-fu-output.txt', 'a')
        sys.stdout = sys.stderr
    except:
        pass
    
def p(msg):
    if DEBUG:
        print(msg)
    else:
        gimp.message(msg)

def load_trle_logo(filename, raw_filename):
    if log:
        p(filename)
    if not os.path.exists(filename):
        p('File not found')
        return None
    data = None
    path, ext = os.path.splitext(filename)
    if ext.lower() in ['.raw']:
        with open(filename, 'rb') as f:
            data = f.read(512*256*3) # w x h x bpp
    elif ext.lower() in ['.pak']:
        import zlib
        with open(filename, 'rb') as f:
            uncomp_size = f.read(4)
            data = zlib.decompress(f.read())
    if not data:
        p('No data')
        return None
    if len(data) < 512*256*3:
        p('Not enough data read')
        return None
    if len(data) > 512*256*3:
        p('Too much data')
        return None     
    img = gimp.Image(512, 256, RGB)
    layer = gimp.Layer(img, 'Background', img.width, img.height)
    pr = layer.get_pixel_rgn(0, 0, layer.width, layer.height)
    pr[0:pr.w, 0:pr.h] = data
    img.insert_layer(layer)
    if log:
        p('Script finished')
    return img
    
def load_trle_sky(filename, raw_filename):
    if log:
        p(filename)
    if not os.path.exists(filename):
        p('File not found')
        return None
    data = None
    path, ext = os.path.splitext(filename)
    if ext.lower() in ['.raw']:
        with open(filename, 'rb') as f:
            data = f.read(256*256*3) # w x h x bpp
    if not data:
        p('No data')
        return None
    if len(data) < 256*256*3:
        p('Not enough data read')
        return None
    if len(data) > 256*256*3:
        p('Too much data')
        return None 
    img = gimp.Image(256, 256, RGB)
    layer = gimp.Layer(img, 'Background', img.width, img.height)
    pr = layer.get_pixel_rgn(0, 0, layer.width, layer.height)
    pr[0:pr.w, 0:pr.h] = data
    img.insert_layer(layer)
    if log:
        p('Script finished')
    return img
       
def register_load_handlers():
    gimp.register_load_handler('file-trle-logo-load', 'raw,pak', '')
    pdb['gimp-register-file-handler-mime']('file-trle-logo-load', 'image/trlelogo')

register(
    'file-trle-logo-load', #name
    'Load a TRLE logo (.raw/.pak) file', #description
    'Logo files are used in Tomb Raider Level Editing and appear at the start of'+
    ' the game. They are raw RGB files 512px wide by 256px high. Pure black (RGB (0,0,0))'+
    ' is transparent in game. For .raw files you must select the filetype "TRLE Logo" in the'+
    ' Open file dialog dropdown since .raw is associated with other files.',
    'sapper', #author
    'sapper', #copyright
    '2017', #year
    'TRLE Logo',
    None, #image type
    [   #input args. Format (type, name, description, default [, extra])
        (PF_STRING, 'filename', 'The name of the file to load', None),
        (PF_STRING, 'raw-filename', 'The name entered', None),
    ],
    [(PF_IMAGE, 'image', 'Output image')], #results. Format (type, name, description)
    load_trle_logo, #callback
    on_query = register_load_handlers,
    menu = "<Load>",
)  

def register_load_handlers2():
    gimp.register_load_handler('file-trle-sky-load', 'raw', '')
    pdb['gimp-register-file-handler-mime']('file-trle-sky-load', 'image/trlesky')

register(
    'file-trle-sky-load', #name
    'Load a TRLE sky (.raw) file', #description
    'Sky files are used in Tomb Raider Level Editing and appear at the top of the'+
    ' horizon skybox in game. They are raw RGB files 256px wide by 256px high.'+
    ' For .raw files you must select the filetype "TRLE Sky" in the'+
    ' Open file dialog dropdown since .raw is associated with other files.',
    'sapper', #author
    'sapper', #copyright
    '2017', #year
    'TRLE Sky',
    None, #image type
    [   #input args. Format (type, name, description, default [, extra])
        (PF_STRING, 'filename', 'The name of the file to load', None),
        (PF_STRING, 'raw-filename', 'The name entered', None),
    ],
    [(PF_IMAGE, 'image', 'Output image')], #results. Format (type, name, description)
    load_trle_sky, #callback
    on_query = register_load_handlers2,
    menu = "<Load>",
) 

if __name__=='__main__':
    main()      
        