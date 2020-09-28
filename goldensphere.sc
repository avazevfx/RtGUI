{
  "objects": [
    {
      "name": "s1",
      "posx": "0",
      "posy": "0",
      "posz": "1.7",
      "radius": "0.15",
      "material": "gold"
    },
    {
      "name": "keyl",
      "posx": "-2",
      "posy": "3",
      "posz": "1.1",
      "radius": "1",
      "material": "keylight"
    },
    {
      "name": "fill",
      "posx": "4",
      "posy": "0",
      "posz": "0",
      "radius": "1",
      "material": "filllight"
    },
    {
      "name": "riml",
      "posx": "2",
      "posy": "1.5",
      "posz": "4",
      "radius": "1",
      "material": "rimlight"
    },
    {
      "name": "s2",
      "posx": "0.28",
      "posy": "0",
      "posz": "1.2",
      "radius": "0.16",
      "material": "white"
    },
    {
      "name": "s3",
      "posx": "-0.28",
      "posy": "0",
      "posz": "1.2",
      "radius": "0.16",
      "material": "purple"
    }
  ],
  "materials": [
    {
      "name": "gold",
      "difx": "30",
      "dify": "30",
      "difz": "30",
      "specx": "255",
      "specy": "200",
      "specz": "0",
      "reflectivity": "0.6",
      "emisx": "0",
      "emisy": "0",
      "emisz": "0",
      "diftex": "D:/Files/Code/Ruby Raytracer/tex/cg_diffuse.png",
      "spectex": "D:/Files/Code/Ruby Raytracer/tex/cg_diffuse.png",
      "normaltex": "D:/Files/Code/Ruby Raytracer/tex/cg_normal.png",
      "normalstrength": "0.6"
    },
    {
      "name": "rimlight",
      "difx": "200",
      "dify": "200",
      "difz": "200",
      "specx": "255",
      "specy": "255",
      "specz": "255",
      "reflectivity": "0",
      "emisx": "150",
      "emisy": "150",
      "emisz": "150",
      "diftex": null,
      "spectex": null,
      "normaltex": null,
      "normalstrength": "1"
    },
    {
      "name": "filllight",
      "difx": "200",
      "dify": "200",
      "difz": "200",
      "specx": "255",
      "specy": "255",
      "specz": "255",
      "reflectivity": "0",
      "emisx": "90",
      "emisy": "90",
      "emisz": "90",
      "diftex": null,
      "spectex": null,
      "normaltex": null,
      "normalstrength": "1"
    },
    {
      "name": "keylight",
      "difx": "200",
      "dify": "200",
      "difz": "200",
      "specx": "255",
      "specy": "255",
      "specz": "255",
      "reflectivity": "0",
      "emisx": "220",
      "emisy": "220",
      "emisz": "220",
      "diftex": null,
      "spectex": null,
      "normaltex": null,
      "normalstrength": "1"
    },
    {
      "name": "white",
      "difx": "200",
      "dify": "200",
      "difz": "200",
      "specx": "255",
      "specy": "255",
      "specz": "255",
      "reflectivity": "0.1",
      "emisx": "0",
      "emisy": "0",
      "emisz": "0",
      "diftex": null,
      "spectex": null,
      "normaltex": "D:/Files/Code/Ruby Raytracer/tex/st_normal.png",
      "normalstrength": "0.07"
    },
    {
      "name": "purple",
      "difx": "127",
      "dify": "0",
      "difz": "255",
      "specx": "127",
      "specy": "0",
      "specz": "255",
      "reflectivity": "0.3",
      "emisx": "0",
      "emisy": "0",
      "emisz": "0",
      "diftex": null,
      "spectex": null,
      "normaltex": "D:/Files/Code/Ruby Raytracer/tex/rc_normal.tif",
      "normalstrength": "0.05"
    }
  ],
  "settings": {
    "width": 1920,
    "height": 1080,
    "reflection_depth": 5
  }
}