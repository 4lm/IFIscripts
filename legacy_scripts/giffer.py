#!/usr/bin/env python
'''
Takes a video file as source and generates a sidecar gif animation.

'''
import sys
import os
import subprocess


def make_palette(source):
    '''
    analyses your source file in order to determine the colour palette.
    '''
    cmd = [
        'ffmpeg',
        '-i', source,
        '-filter_complex',
        'fps=24,scale=500:-1:flags=lanczos,palettegen',
        'palette.png'
    ]
    subprocess.call(cmd)

def make_gif(source):
    '''
    Uses the palette that is generated by make_pallete() in order to
    make a gif.
    '''
    cmd = [
        'ffmpeg',
        '-i', source,
        '-i', 'palette.png',
        '-filter_complex',
        '[0:v]fps=24,scale=500:-1:flags=lanczos[v],[v][1:v]paletteuse',
        source + '.gif'
    ]
    subprocess.call(cmd)

def main():
    '''
    Launches the other functions.
    '''
    source = sys.argv[1]
    make_palette(source)
    make_gif(source)
    os.remove('palette.png')


if __name__ == '__main__':
    main()
