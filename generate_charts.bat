::chart.py -r0 -m5 -l1 -S.5 --ngc_max 6 --out r0index.png
::chart.py -r6 -m5 -l1 -S.5 --ngc_max 6 --out r6index.png
::chart.py -r12 -m5 -l1 -S.5 --ngc_max 6 --out r12index.png
::chart.py -r18 -m5 -l1 -S.5 --ngc_max 6 --out r18index.png

::chart.py   --dpi 300 -r0  --mag 12 --width 33.1 --height 46.8 --factor 1 --scaleR 2 --ngc_max 8  --out r0.png --bayer_font 32 --hip_font 24 --ngc_font 24  --labelLimit 6 --figure_line_width 3 --con_line_width 3 --ecliptic_line_width 4 --tick_width 2
chart.py   --dpi 300 -r6  --mag 12 --width 33.1 --height 46.8 --factor 1 --scaleR 2 --ngc_max 8  --out r6.png --bayer_font 32 --hip_font 24 --ngc_font 24 --labelLimit 6 --figure_line_width 3 --con_line_width 3 --ecliptic_line_width 4 --tick_width 2
::chart.py   --dpi 300 -r12  --mag 12 --width 33.1 --height 46.8 --factor 1 --scaleR 2 --ngc_max 8  --out r12.png --bayer_font 32 --hip_font 24 --ngc_font 24  --labelLimit 6 --figure_line_width 3 --con_line_width 3 --ecliptic_line_width 4 --tick_width 2
::chart.py   --dpi 300 -r18  --mag 12 --width 33.1 --height 46.8 --factor 1 --scaleR 2 --ngc_max 8  --out r18.png --bayer_font 32 --hip_font 24 --ngc_font 24 --labelLimit 6 --figure_line_width 3 --con_line_width 3 --ecliptic_line_width 4 --tick_width 2

::chart.py --dpi 300 --type polar --dec 90 --factor .5 --mag 12 --width 33.1 --height 46.8 --scaleR 2 --ngc_max 8 --out north.png --bayer_font 32 --hip_font 24 --ngc_font 24 --labelLimit 6 --figure_line_width 3 --con_line_width 3 --ecliptic_line_width 4 --tick_width 2
::chart.py --dpi 300 --type polar --dec -90 --factor .5 --mag 12 --width 33.1 --height 46.8 --scaleR 2 --ngc_max 8 --out south.png --bayer_font 32 --hip_font 24 --ngc_font 24 --labelLimit 6 --figure_line_width 3 --con_line_width 3 --ecliptic_line_width 4 --tick_width 2

::chart.py    --factor .22 --type polar --dec 90 -l6 --width 33.1 --height 46.8 --scaleR 2 --ngc_max 8  --out polar.png --bayer_font 32 --hip_font 24 --ngc_font 24 --con_font 90 --labelLimit 5 --figure_line_width 3 --con_line_width 3 --ecliptic_line_width 3
::chart.py  --type gnomonic --width 33.1 --height 46.8 --ra 3.8 --dec 24 --fov 10 --mag 15 --factor 1 --scaleR 3 --ngc_max 9  --out gnomonic.png --bayer_font 24 --hip_font 20 --ngc_font 20 --con_font 90 --labelLimit 12 --figure_line_width 3 --con_line_width 3 --ecliptic_line_width 3