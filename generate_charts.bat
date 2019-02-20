::chart.py -r3 -m5 -l1 -S.5 --ngc_max 6 --out r3index.png
::chart.py -r9 -m5 -l1 -S.5 --ngc_max 6 --out r9index.png
::chart.py -r15 -m5 -l1 -S.5 --ngc_max 6 --out r15index.png
::chart.py -r21 -m5 -l1 -S.5 --ngc_max 6 --out r21index.png

::chart.py -r3  -l6  --ngc_max 9 --out r3_high.png
chart.py  -r6  --mag 11 --width 33.1 --height 46.8 --factor 1 --scaleR 2 --ngc_max 9  --out r6_high.png --bayer_font 24 --hip_font 18 --ngc_font 18 --con_font 90 --labelLimit 6 --figure_line_width 3 --con_line_width 3 --ecliptic_line_width 3
::chart.py -r15 -l6  --ngc_max 9  --out r15_high.png
::chart.py -r21 -l6  --ngc_max 9  --out r21_high.png

::chart.py  --type polar --dec 90 -l6 --width 33.1 --height 46.8 --factor 1 --scaleR 1.75 --ngc_max 9  --out polar.png --bayer_font 40 --hip_font 30 --ngc_font 30 --con_font 120 --labelLimit 6 --figure_line_width 3 --con_line_width 3 --ecliptic_line_width 3
::chart.py  --type gnomonic --width 33.1 --height 46.8 --ra 3.8 --dec 24 --fov 10 --mag 15 --factor 1 --scaleR 3 --ngc_max 9  --out gnomonic.png --bayer_font 24 --hip_font 20 --ngc_font 20 --con_font 90 --labelLimit 12 --figure_line_width 3 --con_line_width 3 --ecliptic_line_width 3