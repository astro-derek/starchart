::chart.py -r3 -m5 -l1 -S.5 --ngc_max 6 --out r3index.png
::chart.py -r9 -m5 -l1 -S.5 --ngc_max 6 --out r9index.png
::chart.py -r15 -m5 -l1 -S.5 --ngc_max 6 --out r15index.png
::chart.py -r21 -m5 -l1 -S.5 --ngc_max 6 --out r21index.png

::chart.py -r3  -l6  --ngc_max 9 --out r3_high.png

::chart.py   --dpi 300 -r0  --mag 11 --width 33.1 --height 46.8 --factor 1 --scaleR 2 --ngc_max 8  --out r0.png --bayer_font 32 --hip_font 24 --ngc_font 24 --con_font 90 --labelLimit 6 --figure_line_width 3 --con_line_width 3 --ecliptic_line_width 4 --tick_width 2
::chart.py   --dpi 300 -r3  --mag 11 --width 33.1 --height 46.8 --factor 1 --scaleR 2 --ngc_max 8  --out r3.png --bayer_font 32 --hip_font 24 --ngc_font 24 --con_font 90 --labelLimit 6 --figure_line_width 3 --con_line_width 3 --ecliptic_line_width 4 --tick_width 2
chart.py   --dpi 300 -r6  --mag 11 --width 33.1 --height 46.8 --factor 1 --scaleR 2 --ngc_max 8  --out r6.png --bayer_font 32 --hip_font 24 --ngc_font 24 --con_font 90 --labelLimit 6 --figure_line_width 3 --con_line_width 3 --ecliptic_line_width 4 --tick_width 2
::chart.py   --dpi 300 -r9  --mag 11 --width 33.1 --height 46.8 --factor 1 --scaleR 2 --ngc_max 8  --out r9.png --bayer_font 32 --hip_font 24 --ngc_font 24 --con_font 90 --labelLimit 6 --figure_line_width 3 --con_line_width 3 --ecliptic_line_width 4 --tick_width 2
::chart.py   --dpi 300 -r18  --mag 11 --width 33.1 --height 46.8 --factor 1 --scaleR 2 --ngc_max 8  --out r18.png --bayer_font 32 --hip_font 24 --ngc_font 24 --con_font 90 --labelLimit 6 --figure_line_width 3 --con_line_width 3 --ecliptic_line_width 4 --tick_width 2
::chart.py   --dpi 300 -r12  --mag 11 --width 33.1 --height 46.8 --factor 1 --scaleR 2 --ngc_max 8  --out r12.png --bayer_font 32 --hip_font 24 --ngc_font 24 --con_font 90 --labelLimit 6 --figure_line_width 3 --con_line_width 3 --ecliptic_line_width 4 --tick_width 2
::chart.py   --dpi 300 -r15  --mag 11 --width 33.1 --height 46.8 --factor 1 --scaleR 2 --ngc_max 8  --out r15.png --bayer_font 32 --hip_font 24 --ngc_font 24 --con_font 90 --labelLimit 6 --figure_line_width 3 --con_line_width 3 --ecliptic_line_width 4 --tick_width 2
::chart.py   --dpi 300 -r21  --mag 11 --width 33.1 --height 46.8 --factor 1 --scaleR 2 --ngc_max 8  --out r21.png --bayer_font 32 --hip_font 24 --ngc_font 24 --con_font 90 --labelLimit 6 --figure_line_width 3 --con_line_width 3 --ecliptic_line_width 4 --tick_width 2



::chart.py -r15 -l6  --ngc_max 9  --out r15_high.png
::chart.py -r21 -l6  --ngc_max 9  --out r21_high.png

::chart.py    --factor .22 --type polar --dec 90 -l6 --width 33.1 --height 46.8 --scaleR 2 --ngc_max 8  --out polar.png --bayer_font 32 --hip_font 24 --ngc_font 24 --con_font 90 --labelLimit 5 --figure_line_width 3 --con_line_width 3 --ecliptic_line_width 3
::chart.py  --type gnomonic --width 33.1 --height 46.8 --ra 3.8 --dec 24 --fov 10 --mag 15 --factor 1 --scaleR 3 --ngc_max 9  --out gnomonic.png --bayer_font 24 --hip_font 20 --ngc_font 20 --con_font 90 --labelLimit 12 --figure_line_width 3 --con_line_width 3 --ecliptic_line_width 3