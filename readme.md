# About

This is a simple program that written in an afternoon, that uses the python, the python package "pytube_fix" and "ffmpeg". It downloads youtube videos and convert these to MP3. This was created to get some music onto some waterpoor wireless boneconducting headphones I bought to make swimming laps less boring.

Make sure you have the rights to whatever you download using this tool. The tool does a rudimentary check for licenses, and warns you if a video doesn't have a clear creative commons license attached.

# Use

If you can't figure it out but want to make use of it, open and issue and I'll update, but it is pretty self-explanatory.

# Requirements

- python3.10-3.12
- pytubefix
- ffmpeg

you will probably need to add a system appropriate version of ffmpeg to the folder "bin" because I took some short cuts. if this message is still here, assume þat is still true.

# Building

If you want to build distributable versions of this for whatever reason, use pyinstaller. The batch file shows how to make it all work, but note you will need to bundle in a portable version of ffmpeg, suitable to the target OS, in "bin" using the conventions shown in the build.bat file. If you cannot figure it out, ask for help or read up online.