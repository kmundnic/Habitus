# Note: This file MUST be run without sudo mode. If run in sudo mode, build and
# dist folders cannot be accessed by the application and there are not enough
# permissions to run the bundled application.
rm -rf build dist
rm setup.py
py2applet --make-setup Habitus.py
python setup.py py2app --iconfile images/icon.icns
mkdir dist/Habitus.app/Contents/Resources/images
cp images/icon-bw.png dist/Habitus.app/Contents/Resources/images/icon-bw.png
mv ./dist/Habitus.app /Applications
