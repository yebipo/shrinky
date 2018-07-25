#!/bin/sh
SHRINKY_MODULE_PATH=shrinky
if [ ! -d "$SHRINKY_MODULE_PATH" ]; then
  SHRINKY_MODULE_PATH=/usr/share/shrinky
fi
if [ -z $1 ]; then
  echo 'Shrinky 0.1 (dnload fork)'
  echo
  echo 'Provide the path to a C++ source file as the first argument.'
  echo
  echo 'Example:'
  echo '    shrinky examples/intro.cpp'
  echo
  exit 1
fi
FILENAME="${1:-src/intro.cpp}"
shift
SRCDIR="$(dirname $FILENAME)"
[ -f "$SRCDIR/shrinky.h" ] || touch "$SRCDIR/shrinky.h"
if [ -d "/usr/lib/arm-linux-gnueabihf/mali-egl" ]; then # Mali
  /usr/bin/python3 -m "$SHRINKY_MODULE_PATH" -v "$FILENAME" --rpath "/usr/local/lib" -lc -ldl -lgcc -lm -lEGL -lGLESv2 -lSDL2 -m dlfcn "$@"
else
  /usr/bin/python3 -m "$SHRINKY_MODULE_PATH" -v "$FILENAME" "$@"
fi
if [ $? -ne 0 ]; then
  echo "${0}: compilation failed"
  exit 1
fi
