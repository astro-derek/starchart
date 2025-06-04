package main

import (
	"bufio"
	"encoding/csv"
	"flag"
	"image/color"
	"log"
	"math"
	"os"
	"strconv"

	"github.com/fogleman/gg"
)

// NGCObject represents a row in the ngc.csv catalogue.
type NGCObject struct {
	Name string
	RA   float64 // hours
	Dec  float64 // degrees
	Mag  float64
}

const deg2rad = math.Pi / 180.0

func parseNGC(path string, limit float64) ([]NGCObject, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()

	r := csv.NewReader(bufio.NewReader(f))
	r.FieldsPerRecord = -1

	var res []NGCObject
	for {
		rec, err := r.Read()
		if err != nil {
			if err.Error() == "EOF" {
				break
			}
			return nil, err
		}
		if len(rec) < 17 {
			continue
		}
		name := rec[0] + rec[1]
		// RA fields 8,9,10
		rh, _ := strconv.ParseFloat(rec[8], 64)
		rm, _ := strconv.ParseFloat(rec[9], 64)
		rs, _ := strconv.ParseFloat(rec[10], 64)
		ra := rh + rm/60.0 + rs/3600.0
		// Dec fields 11 hem sign, 12,13,14
		sign := 1.0
		if rec[11] == "-" {
			sign = -1.0
		}
		dd, _ := strconv.ParseFloat(rec[12], 64)
		dm, _ := strconv.ParseFloat(rec[13], 64)
		ds, _ := strconv.ParseFloat(rec[14], 64)
		dec := sign * (dd + dm/60.0 + ds/3600.0)
		mag := 0.0
		if rec[16] != "" {
			mag, _ = strconv.ParseFloat(rec[16], 64)
		}
		if mag == 0 || mag <= limit {
			res = append(res, NGCObject{Name: name, RA: ra, Dec: dec, Mag: mag})
		}
	}
	return res, nil
}

func gnomonic(ra, dec, baseRA, baseDec float64) (float64, float64) {
	lam := ra * 15 * deg2rad
	chi := dec * deg2rad
	lam0 := baseRA * 15 * deg2rad
	chi1 := baseDec * deg2rad

	denom := math.Sin(chi1)*math.Sin(chi) + math.Cos(chi1)*math.Cos(chi)*math.Cos(lam-lam0)
	x := math.Cos(chi) * math.Sin(lam-lam0) / denom
	y := (math.Cos(chi1)*math.Sin(chi) - math.Sin(chi1)*math.Cos(chi)*math.Cos(lam-lam0)) / denom

	return -x, -y
}

func main() {
	var (
		centreRA  = flag.Float64("ra", 6, "centre right ascension (hours)")
		centreDec = flag.Float64("dec", 0, "centre declination (degrees)")
		fov       = flag.Float64("fov", 10, "field of view in degrees")
		catalogue = flag.String("catalogue", "data/ngc.csv", "catalogue csv path")
		out       = flag.String("out", "chart.png", "output image")
		limit     = flag.Float64("mag", 10, "limiting magnitude")
		width     = flag.Int("width", 800, "image width")
		height    = flag.Int("height", 800, "image height")
	)
	flag.Parse()

	objects, err := parseNGC(*catalogue, *limit)
	if err != nil {
		log.Fatal(err)
	}

	dc := gg.NewContext(*width, *height)
	dc.SetColor(color.Black)
	dc.Clear()

	scale := float64(*width) / (*fov)

	for _, obj := range objects {
		x, y := gnomonic(obj.RA, obj.Dec, *centreRA, *centreDec)
		px := x*scale + float64(*width)/2
		py := y*scale + float64(*height)/2

		if px < 0 || py < 0 || px >= float64(*width) || py >= float64(*height) {
			continue
		}

		r := 2.0
		if obj.Mag > 0 {
			r = math.Max(0.5, 6.0-obj.Mag/2)
		}
		dc.DrawCircle(px, py, r)
		dc.SetColor(color.White)
		dc.Fill()
	}

	if err := dc.SavePNG(*out); err != nil {
		log.Fatal(err)
	}
}
